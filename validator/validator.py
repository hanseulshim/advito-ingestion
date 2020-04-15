import traceback
import pandas as pd
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound

from db.db import HotelSession, AdvitoSession
from db.advito_models import AdvitoApplicationTemplateColumn, Currency, JobIngestion


class Validator:
    # TODO: Add other validations here
    validators = {
        'incorrect_characters_validation': 'incorrectCharacters',
        'incorrect_dates_validation': 'incorrectDates',
        'source_currency_code_validation': 'sourceCurrencyCode',
        'unmasked_credit_card_data_validation': 'unmaskedCreditCardData',
    }

    def __init__(self):
        self.hotel_session = HotelSession()
        self.advito_session = AdvitoSession()
        self.validation_errors = {
           'incorrectCharacters': list(),
           'incorrectDates': list(),
           'sourceCurrencyCode': list(),
           'unmaskedCreditCardData': list(),
        }

    def __del__(self):
        self.hotel_session.close()
        self.advito_session.close()

    def validate(self, job_ingestion_id, file_path):
        try:
            job = (
                self.advito_session.query(JobIngestion)
                .filter(JobIngestion.id == job_ingestion_id)
                .one()
            )

            # generate how to read excel file from job_ingestion
            df = pd.read_excel(file_path, dtype=str)

            progress_step = 100 / len(self.validators)
            validation_passed = True
            for i, (validator, output) in enumerate(self.validators.items()):
                validation_passed, validation_error = getattr(self, validator)(df)
                if validation_error:
                    validation_passed = False
                    self.validation_errors[output].extend(validation_error)
                # TODO: update job_note with progress 0-100
                job_progress_percentage = str(int((i + 1) * progress_step))
                job.job_note = job_progress_percentage
                self.advito_session.commit()
            print(self.validation_errors)
            # update job
            from datetime import datetime
            import json
            dt = datetime.now()
            job.is_complete = True
            job.processing_end_timestamp = dt
            job.processing_dur_sec = (dt - job.processing_start_timestamp).total_seconds()
            if validation_passed:
                job.job_status = 'done'
                job.job_note = None
            else:
                job.job_status = 'error'
                job.job_note = json.dumps(self.validation_errors)
            self.advito_session.commit()
        except NoResultFound:
            print('Job ingestion id {} not found'.format(job_ingestion_id))
            validation_passed = False
        # general exception
        except Exception as e:
            print(e)
            traceback.print_exc()

            validation_passed = False
        return validation_passed

    @staticmethod
    def incorrect_characters_validation(data):
        """

        :param data:    pd.Dataframe
        :return:
        """

        def clean_data(field):
            if field:
                field = field.strip().replace('-', '').replace(' ', '')
            return field

        def is_allowed(x):
            import re
            pattern = re.compile(r"""^[a-zA-Z0-9À-ž\s\\,.:;!?`&$()/|\-_'"]+$""")
            match_obj = pattern.match(x)
            return True if match_obj else False

        print('Special Chars Validation')
        df = data.copy()
        err_list = list()
        for column in df.columns.tolist():
            s = df[column].astype(str).apply(clean_data).apply(is_allowed)
            s = s[s == False]
            if not s.empty:
                err_list.extend(
                    'Row {}, Column {}'.format(str(index + 2), column)
                    for index in s.index.tolist())
        return (False, err_list) if err_list else (True, '')

    def incorrect_dates_validation(self, data):
        """

        :param data:    pd.Dataframe
        :return:
        """
        def _string_to_date(date_string, date_format='%Y-%m-%d %H:%M:%S'):
            try:
                ret = datetime.strptime(date_string, date_format)
            except ValueError:
                ret = False
            return ret

        print('Date Format Validation')
        df = data.copy()
        df_columns = df.columns.tolist()
        # get columns to check from db
        columns_to_check = self._get_date_columns()
        columns = [col for col in columns_to_check if col in df_columns]
        print('\tColumns to check: {}'.format(columns))

        err_list = list()
        for column in columns:
            # # empty dates
            # s = df[column].isna()
            # s = s[s == True]
            # if not s.empty:
            #     err_msg_list.append('{}: {}'.format(
            #         column,
            #         ', '.join([str(index + 2) for index in s.index.tolist()])))

            # bad date format
            s = df[column].dropna().apply(_string_to_date)
            s = s[s == False]
            if not s.empty:
                err_list.extend(
                    'Row {}, Column {}'.format(str(index + 2), column)
                    for index in s.index.tolist())
        return (False, err_list) if err_list else (True, None)

    def source_currency_code_validation(self, data):
        """

        :param data:    pd.Dataframe
        :return:
        """
        print('Currency Code Validation')
        df = data.copy()
        df_columns = df.columns.tolist()
        # get columns to check from db
        columns_to_check = self._get_currency_columns()
        columns = [col for col in columns_to_check if col in df_columns]
        print('\tColumns to check: {}'.format(columns))

        db_ccs = self._get_currency_codes()
        err_list = list()
        for column in columns:
            # empty rows
            empty_rows = df[column].isna()
            empty_rows = empty_rows[empty_rows == True]
            if not empty_rows.empty:
                err_list.extend(
                    'Row {}, Column {}'.format(str(index + 2), column)
                    for index in empty_rows.index.tolist())

            # bad currencies
            s = df[column].dropna().apply(
                lambda x: True if x in db_ccs else False)
            s = s[s == False]
            if not s.empty:
                err_list.extend(
                    'Row {}, Column {}'.format(str(index + 2), column)
                    for index in s.index.tolist())
        return (False, err_list) if err_list else (True, None)

    @staticmethod
    def unmasked_credit_card_data_validation(data):
        """

        :param data:    pd.Dataframe
        :return:
        """

        def clean_data(field):
            if field:
                field = field.strip().replace('-', '').replace(' ', '')
            return field

        df = data.copy()
        for column in df.columns.tolist():
            df[column] = df[column].astype(str).apply(clean_data)
        mask = df.apply(
            lambda row: row.astype(str).str.contains(r'\d{15}', regex=True),
            axis=1)
        err_list = list()
        for column in mask.columns.tolist():
            s = mask[column]
            s = s[s == True]
            if not s.empty:
                err_list.extend(
                    'Row {}, Column {}'.format(str(index + 2), column)
                    for index in s.index.tolist())
        return (False, err_list) if err_list else (True, None)

    @staticmethod
    def _get_currency_columns():
        # there is no way to extract columns from db by some specification
        return ['CurrCode',
                'Report Currency',
                'Source Currency Code',
                'Transaction Currency']

    def _get_date_columns(self):
        columns = (
            self.advito_session.query(AdvitoApplicationTemplateColumn.column_name)
            .filter(AdvitoApplicationTemplateColumn.data_type == 'date')
            .distinct()
            .all()
        )
        return [column[0] for column in columns]

    def _get_currency_codes(self):
        currency_codes = (
            self.advito_session.query(Currency.currency_code)
            .all()
        )
        return [cc[0] for cc in currency_codes]


if __name__ == '__main__':
    # Validator().validate(ingest_job_id='123456789', file_path='ValidationTest.xlsx')
    # Validator().validate(ingest_job_id='123456789', file_path='https://hotel-api-downloads.s3.us-east-2.amazonaws.com/ValidationTest.xlsx')
    Validator().validate(job_ingestion_id='164', file_path='AgencyHotel_ValidationTest.xlsx')

