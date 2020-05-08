import io
import time
import traceback
from datetime import datetime

import boto3
import pandas as pd
from sqlalchemy.orm.exc import NoResultFound

from db.advito_models import (AdvitoApplicationTemplate,
                              AdvitoApplicationTemplateColumn,
                              AdvitoApplicationTemplateSource, Currency,
                              JobIngestion)
from db.db import AdvitoSession, HotelSession


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

    def validate(self, job_ingestion_id, bucket_origin, bucket_dest, environment, advito_application_id):
    # def validate(self, job_ingestion_id):
        
        try:
            # 0. Get job, template and column information
            job = (
                self.advito_session.query(JobIngestion)
                .filter(JobIngestion.id == job_ingestion_id)
                .one()
            )
            validation_passed = True
            validation_run = True

            aws_id = 'AKIATCJAOULBYSVCTBM4'
            aws_secret = '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'
            object_key = job.file_name
            s3 = boto3.client('s3', aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)
            lambda_client = boto3.client('lambda', aws_access_key_id=aws_id, aws_secret_access_key=aws_secret, region_name='us-east-2')
            obj = s3.get_object(Bucket=bucket_origin, Key=object_key)
            data = obj['Body'].read()
            
            print('Running validation for id: ' + str(job.id))
            start_read_time = time.time()
            df = pd.read_excel(io.BytesIO(data), encoding='utf-8',)
            end_read_time = time.time() - start_read_time
            start_validate_time = time.time()
            # df = pd.read_excel('error.xlsx', encoding='utf-8')

            progress_step = 100 / len(self.validators)
            for i, (validator, output) in enumerate(self.validators.items()):
                validation_run, validation_error = getattr(self, validator)(df)
                if validation_error:
                    validation_passed = False
                    self.validation_errors[output].extend(validation_error)
                # TODO: update job_note with progress 0-100
                job_progress_percentage = str(int((i + 1) * progress_step))
                job.job_note = job_progress_percentage
                self.advito_session.commit()
                
            # update job
            print(f"\n\n{self.validation_errors}\n\n")
            from datetime import datetime
            import json
            dt = datetime.now()
            job.is_complete = True
            row_count = len(df.index)
            row_const = 150
            job.count_rows = row_count
            job.processing_end_timestamp = dt
            job.processing_dur_sec = (dt - job.processing_start_timestamp).total_seconds()
            if validation_passed:
                job.job_status = 'done'
                job.job_note = None
                # If the environment is production then copy the file into new bucket
                row_range = int(row_count / row_const) + (row_count % row_const > 0)
                for x in range(row_range):
                    current_range = x * row_const
                    if environment == 'PROD':
                        new_key = 'upload/' + object_key
                        s3.copy_object(Bucket=bucket_dest, CopySource=bucket_origin + '/' + object_key, Key=new_key)
                        s3.delete_object(Bucket=bucket_dest, Key=object_key)
                        job.file_name = new_key
                    if advito_application_id == 1:
                        function_name = 'advito-ingestion-dev-ingest-hotel-template'
                        if environment == 'PROD':
                            function_name = 'advito-ingestion-production-ingest-hotel-template'
                        if environment == 'STAGING':
                            function_name = 'advito-ingestion-staging-ingest-hotel-template'
                        # print(json.dumps(df.iloc[current_range:current_range + row_const - 1].to_json(orient='records')))
                        end = current_range + len(df.iloc[current_range:current_range + row_const])
                        # print('Invoking for rows: ', current_range, end)
                        lambda_client.invoke(
                            FunctionName=function_name,
                            InvocationType='Event',
                            Payload=json.dumps({'jobIngestionId': job_ingestion_id, 'data': df.iloc[current_range:current_range + row_const].to_json(orient='records'), 'start': current_range, 'end': end})
                        )
            else:
                job.job_status = 'error'
                job.job_note = json.dumps(self.validation_errors)
            print(f"--- {end_read_time / 60} minutes to read file ---")
            print(f"--- {(time.time() - start_validate_time) / 60} minutes to validate file ---")
            print(f"---  of size {job.file_size / 1000 / 1000}MB and {job.count_rows} rows ---")
            self.advito_session.commit()
        except NoResultFound:
            print('Job ingestion id {} not found'.format(job_ingestion_id))
            if job.id > 0:
                job.is_complete = True
                job.job_status = 'server-error'
                job.job_note = 'Job ingestion id {} not found'.format(job_ingestion_id)
                self.advito_session.commit()
            validation_passed = False
        # general exception
        except Exception as e:
            print(e)
            if job.id > 0:
                job.is_complete = True
                job.job_status = 'server-error'
                job.job_note = str(e)
                self.advito_session.commit()
            traceback.print_exc()

            validation_passed = False
        return validation_passed

    @staticmethod
    def incorrect_characters_validation(data):
        """

        :param data:    pd.Dataframe
        :return:
        """

        def is_allowed(x):
            import re
            pattern = re.compile(r"""^[a-zA-Z0-9À-ž\s\\,.:;!?*@#`&$()/|\-_+'"]+$""") # [ING87] Aded *, but also #@, and +
            match_obj = pattern.match(x)
            return True if match_obj else False

        print('Special Chars Validation')
        df = data.copy()
        err_list = list()
        for column in df.columns.tolist():
            s = df[column].astype(str).apply(is_allowed)
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
                ret = datetime.strptime(str(date_string), date_format)
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
                lambda x: True if x.lower() in db_ccs else False)
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
            lambda row: row.astype(str).str.contains(r'^\d{15,16}$', regex=True),  # OPS1: Added ^$ anchors 
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
                'Currency Code',
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
        return [cc[0].lower() for cc in currency_codes]


if __name__ == '__main__':
    Validator().validate(job_ingestion_id='18537', bucket_origin='advito-ingestion-templates', bucket_dest='advito-ingestion-templates', environment='DEV', advito_application_id=1)
    # Validator().validate(job_ingestion_id='18408')
