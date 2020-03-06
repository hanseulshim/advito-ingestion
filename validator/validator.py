import pandas as pd
from datetime import datetime

from db.db import HotelSession, AdvitoSession
from db.advito_models import AdvitoApplicationTemplateColumn, Currency


class Validator:
    # TODO: Add other validations here
    validators = [
        # 'unmasked_credit_card_data_validation',
        # 'source_currency_code_validation',
        'incorrect_characters_validation',
        # 'incorrect_dates_validation',
    ]

    def __init__(self):
        self.hotel_session = HotelSession()
        self.advito_session = AdvitoSession()
        self.validation_err = {
           'unmaskedCreditCardData': list(),
           'sourceCurrencyCode': list(),
           'incorrectCharacters': list(),
           'incorrectDates': list()
        }

    def __del__(self):
        self.hotel_session.close()
        self.advito_session.close()

    def validate(self, ingest_job_id, file_path):
        validation_passed = False
        msg = None
        df = pd.read_excel(file_path, dtype=str)

        for validator in self.validators:
            validation_passed, msg = getattr(self, validator)(df)
            print('{} - {} - {}'.format(
                validator,
                'passed' if validation_passed else 'failed',
                msg))

            # TODO: Write result to ingest job when specified
        return validation_passed, msg

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
            lambda row: row.astype(str).str.contains(r'\d{15}', regex=True).any(),
            axis=1)
        unmasked_data_rows = mask[mask == True].index.tolist()
        if unmasked_data_rows:
            msg = 'Potential Unmasked Credit Card Number found in:<br/>{}'.format(
                '<br/>'.join(['- Line {}'.format(line) for line in unmasked_data_rows])
            )
            ret = (False, msg)
        else:
            ret = (True, '')
        return ret

    def incorrect_dates_validation(self, data):
        """

        :param data:    pd.Dataframe
        :return:
        """
        print('Date Format Validation')
        df = data.copy()
        df_columns = df.columns.tolist()
        # get columns to check from db
        columns_to_check = self._get_date_columns()
        columns = [col for col in columns_to_check if col in df_columns]
        print('Columns to check: {}'.format(columns))

        err_msg_list = list()
        for column in columns:
            s = df[column].dropna().apply(self._string_to_date)
            s = s[s == False]
            if not s.empty:
                err_msg_list.append('{}: {}'.format(
                    column,
                    ', '.join([str(index) for index in s.index.tolist()])))
        if err_msg_list:
            err_msg = 'Dates with bad format found:<br/>{}'.format(
                '<br/>'.join(err_msg_list))
            ret = (False, err_msg)
        else:
            ret = (True, '')
        return ret

    def source_currency_code_validation(self, data):
        """

        :param data:    pd.Dataframe
        :return:
        """
        print('Corrency Code Validation')
        df = data.copy()
        df_columns = df.columns.tolist()
        # get columns to check from db
        columns_to_check = self._get_currency_columns()
        columns = [col for col in columns_to_check if col in df_columns]
        print('Columns to check: {}'.format(columns))

        db_ccs = self._get_currency_codes()
        err_msg_list = list()
        for column in columns:
            # empty rows
            empty_rows = df[column].isna()
            empty_rows = empty_rows[empty_rows == True]
            if not empty_rows.empty:
                err_msg_list.append('Empty rows in {}: {}'.format(
                    column,
                    ', '.join([str(index) for index in empty_rows.index.tolist()])))

            # bad currencies
            df_ccs = df[column].dropna().unique()
            bad_ccs = [cc for cc in df_ccs if cc not in db_ccs]
            if bad_ccs:
                err_msg_list.append('Bad currency codes found in {}: {}'.format(
                    column, ', '.join(bad_ccs)))

        if err_msg_list:
            err_msg = 'Empty or bad currencies found:<br/>{}'.format(
                '<br/>'.join(err_msg_list))
            ret = (False, err_msg)
        else:
            ret = (True, '')
        return ret

    def incorrect_characters_validation(self, data):
        """

        :param data:    pd.Dataframe
        :return:
        """
        print('Special Chars Validation')

        def clean_data(field):
            if field:
                field = field.strip().replace('-', '').replace(' ', '')
            return field

        def is_allowed(x):
            import re
            print(x)
            pattern = re.compile(r"""^[\w\s\\,.:;?`&$()/|\-_'"]+$""")
            match_obj = pattern.match(x)
            print(match_obj)
            return True if match_obj else False

        df = data.copy()
        err_msg_list = list()
        for column in df.columns.tolist():
            print(column)
            s = df[column].astype(str).apply(clean_data)
            s = s.apply(is_allowed)
            print(s)
            not_allowed = s[s == False]
            if not not_allowed.empty:
                for index in not_allowed.index.to_list():
                    err_msg_list.append('Column {} Row {}'.format(column, index))

        if err_msg_list:
            err_msg = 'Incorrect characters found:<br/>{}'.format(
                '<br/>'.join(err_msg_list))
            ret = (False, err_msg)
        else:
            ret = (True, '')
        return ret

    @staticmethod
    def _string_to_date(date_string, date_format='%Y-%b-%d %H:%M:%S'):
        try:
            ret = datetime.strptime(date_string, date_format)
        except ValueError:
            ret = False
        return ret

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
    Validator().validate(ingest_job_id='123456789', file_path='ValidationTest.xlsx')
    # Validator().validate(ingest_job_id='123456789', file_path='https://hotel-api-downloads.s3.us-east-2.amazonaws.com/ValidationTest.xlsx')
