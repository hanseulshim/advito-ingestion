import io
import re
import time
import traceback
from datetime import datetime

import boto3
import pandas as pd
from sqlalchemy.orm.exc import NoResultFound

from db.advito_models import (AdvitoApplicationTemplate,
                              AdvitoApplicationTemplateColumn,
                              AdvitoApplicationTemplateSource, Currency,
                              GeoState, JobIngestion, JobIngestionHotel)
from db.db import AdvitoSession, HotelSession


class Validator:
   
    validators = {
        'required_field_validation': 'missingRequired',
        'incorrect_characters_validation': 'incorrectCharacters',
        'incorrect_dates_validation': 'incorrectDates',
        'source_currency_code_validation': 'sourceCurrencyCode',
        'unmasked_credit_card_data_validation': 'unmaskedCreditCardData',
        'state_validation': 'stateValidation',
        'data_type_validation': 'dataType',
        'city_phone_validation': 'invalidCityName',
        'checkout_date_validation': 'invalidCheckout',
        'spend_validation': 'invalidSpend'
    }

    def __init__(self):
        self.hotel_session = HotelSession()
        self.advito_session = AdvitoSession()
        self.required = list()
        self.types = {}
        self.validation_errors = {
           'incorrectTemplate': list(),
           'fileExists': list(),
           'missingRequired': list(),
           'incorrectCharacters': list(),
           'incorrectDates': list(),
           'sourceCurrencyCode': list(),
           'unmaskedCreditCardData': list(),
           'stateShouldBeBlank': list(),
           'stateMissing': list(),
           'stateInvalid': list(),
           'dataType': list(),
           'invalidCityName': list(),
           'invalidCheckout': list(),
           'invalidSpend': list()
        }
        self.job = None

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
            print('Running validation for id: ' + str(job.id))
            self.job = job
            validation_passed = True
            validation_run = True

            aws_id = 'AKIATCJAOULBYSVCTBM4'
            aws_secret = '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'
            object_key = job.file_name
            s3 = boto3.client('s3', aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)
            lambda_client = boto3.client('lambda', aws_access_key_id=aws_id, aws_secret_access_key=aws_secret, region_name='us-east-2')
            obj = s3.get_object(Bucket=bucket_origin, Key=object_key)
            data = obj['Body'].read()
            
            start_read_time = time.time()
            df = pd.read_excel(io.BytesIO(data), encoding='utf-8')
            df.columns = map(str.lower, df.columns)
            end_read_time = time.time() - start_read_time
            start_validate_time = time.time()

            # 1. Before main validation loop, check if a duplicate was already loaded?
            validation_passed, err_list = self.duplicate_file_check()
            if not validation_passed:
                self.validation_errors['fileExists'] = err_list
            else:
                # 2. Not a duplicate. See if the template was valid.
                validation_passed, err_list, required, types = self.incorrect_template_format(df)
                if not validation_passed:
                    self.validation_errors['incorrectTemplate'] = err_list
                else:
                    # Only run main loop if we have the right template
                    self.required = required
                    self.types = types

                    progress_step = 100 / len(self.validators)
                    for i, (validator, output) in enumerate(self.validators.items()):
                        validation_run, validation_error = getattr(self, validator)(df)
                        if validation_error:
                            validation_passed = False
                            if validator == 'state_validation':
                                for key in validation_error:
                                    if validation_error[key]:
                                        self.validation_errors[key].extend(validation_error[key])
                            else:
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
            row_const = 100
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
                        # print(json.dumps(df.iloc[current_range:current_range + row_const - 1].to_json(orient='records', date_format='iso')))
                        end = current_range + len(df.iloc[current_range:current_range + row_const])
                        # print('Invoking for rows: ', current_range, end)
                        if row_count == end:
                            print('Insert complete for job ingestion: ', job.id)
                        # print('job_ingestion_id', job_ingestion_id)
                        lambda_client.invoke(
                            FunctionName=function_name,
                            InvocationType='Event',
                            Payload=json.dumps({'jobIngestionId': job.id, 'data': df.iloc[current_range:current_range + row_const].to_json(orient='records', date_format='iso'), 'start': current_range, 'end': end, 'final': row_count == end})
                        )
                self.advito_session.add(JobIngestionHotel(job_ingestion_id = job.id, is_dpm = False, is_sourcing = False))
            else:
                print('There was an error in job ingestion id: ', job.id)
                job.job_status = 'error'
                job.job_note = json.dumps(self.validation_errors)
            # print(f"--- {end_read_time / 60} minutes to read file ---")
            # print(f"--- {(time.time() - start_validate_time) / 60} minutes to validate file ---")
            # print(f"---  of size {job.file_size / 1000 / 1000}MB and {job.count_rows} rows ---")
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

    def city_phone_validation(self, data):
        print("City Phone Validation")
        df = data.copy()
        df_columns = df.columns.tolist()
        err_list = list()

        city_columns = self._get_columns_by_stage_name('city_name')
        for column in city_columns:
            if column in df_columns:
                s = df[column].dropna().apply(self._check_city)
                s = s[s == False]
                if not s.empty:
                    err_list.extend(
                        'Row {}, Column {}'.format(str(index + 2), column.title())
                        for index in s.index.tolist()) 

        return (False, err_list) if err_list else (True, None)

    def checkout_date_validation(self, data):
        print("Checkout Date Validation")
        df = data.copy()
        df_columns = df.columns.tolist()
        err_list = list()

        checkout_columns = self._get_columns_by_stage_name('check_out_date')
        for column in checkout_columns:
            if column in df_columns:
                s = df[column].dropna()
                row_count = len(s)

                s = s.apply(self._check_checkout_date, args=([self.job.data_end_date]))
                s = s[s == False]
                if not s.empty:
                    err_list.extend(
                        'Row {}, Column {}'.format(str(index + 2), column.title())
                        for index in s.index.tolist())

        return (False, err_list) if err_list else (True, None)

    def data_type_validation(self, data):
        print("Data Type Validation")
        df = data.copy()
        df_columns = df.columns.tolist()
        err_list = list()

        for column in df_columns:
            data_type = self.types[column]
            if data_type in ['float8', 'numeric']:
                print(f"\t{column} - {data_type}")
                s = df[column].dropna().apply(self._check_numeric)
                s = s[s == False]
                if not s.empty:
                    err_list.extend(
                        'Row {}, Column {}: NUMBER expected'.format(str(index + 2), column.title())
                        for index in s.index.tolist())
            
            elif data_type.lower() == 'boolean':
                print(f"\t{column} - {data_type}")
                s = df[column].dropna().apply(self._check_boolean)
                s = s[s == False]
                if not s.empty:
                    err_list.extend(
                        'Row {}, Column {}: y/n expected'.format(str(index + 2), column.title())
                        for index in s.index.tolist())
        
        return (False, err_list) if err_list else (True, None)

    def duplicate_file_check(self):
        # See if another file exists with:
        #   - client_id
        #   - data_start_date
        #   - data_end_date
        #   - advito_application_template_source_id
        existing_job = (
            self.advito_session.query(JobIngestion)
            .filter(JobIngestion.client_id == self.job.client_id)
            .filter(JobIngestion.data_start_date == self.job.data_start_date)
            .filter(JobIngestion.data_end_date == self.job.data_end_date)
            .filter(JobIngestion.advito_application_template_source_id == self.job.advito_application_template_source_id)
            .filter(JobIngestion.job_status != 'backout')
            .filter(JobIngestion.job_status != 'error')
            .filter(JobIngestion.job_status != 'server-error')
            .filter(JobIngestion.job_status != 'deleted')
            .filter(JobIngestion.id != self.job.id)
            .first()
        )
        if existing_job:
            return False, ['File has already been Ingested. Backout the current version to load a new one.']
        else:
            return True, None

    def incorrect_template_format(self, data):
        err_list = list()
        index = 1
        columns, required, types = self._get_all_columns(self.job.advito_application_template_source_id)

        # print(columns)
        # print(required)
        # print(types)

        df = data.copy()
        df_columns = df.columns.tolist()

        for expected, found in zip(columns, df_columns):
            if found.lower().strip() != expected:
                err_list.append(f"In Column {self._get_excel_column_label(index)}: Expected '{expected.title()}', found '{found.title()}'")
            index += 1

        if not err_list:
            # No errors for what's there, make sure there are the
            # same number of columns
            if len(columns) != len(df_columns):
                err_list.append(f"{len(columns)} expected in Template, {len(df_columns)} found.")
        
        if err_list:
            return False, err_list, None, None  # If errors, don't need other dicts; no processing will happen
        else:
            return True, None, required, types

    @staticmethod
    def incorrect_characters_validation(data):
        """

        :param data:    pd.Dataframe
        :return:
        """
        def is_allowed(x):
            pattern = re.compile(r"""^[a-zA-Z0-9À-ž\s\\,.:;!?*@#`&$()/|\-_+'"\u2014‐−–]+$""") # [ING87] Aded *, but also #@, and + add checks for all dashes. \u2014 is em-dash character
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
                    'Row {}, Column {}'.format(str(index + 2), column.title())
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
        columns = [col.lower() for col in columns_to_check if col.lower() in df_columns]
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
                    'Row {}, Column {}'.format(str(index + 2), column.title())
                    for index in s.index.tolist())
        return (False, err_list) if err_list else (True, None)

    def required_field_validation(self, data):
        print("Required Field Validation")
        df = data.copy()
        df_columns = df.columns.tolist()
        err_list = list()

        # State "required" fields have additional logic & are handled separately
        state_columns, country_columns, country_code_columns = self._get_state_columns()
        required = [field for field in self.required if field not in state_columns]

        # True blanks
        for req_column in required:
            empty_rows = df[req_column].isna()
            empty_rows = empty_rows[empty_rows == True]
            if not empty_rows.empty:
                err_list.extend(
                    'Row {}, Column {}'.format(str(index + 2), req_column.title())
                    for index in empty_rows.index.tolist())

        # Whitespace blanks
        for req_column in required:
            space_rows = list(map(lambda x: str(x).isspace(), df[req_column]))
            space_rows = [index for index, blank in enumerate(space_rows) if blank]
            if space_rows:
                err_list.extend(
                    'Row {}, Column {}'.format(str(index + 2), req_column.title())
                    for index in space_rows)

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
        columns_to_check, columns_required = self._get_currency_columns()
        columns = [col.lower() for col in columns_to_check if col.lower() in df_columns]
        columns_required = [col.lower() for col in columns_required if col.lower() in df_columns]
        print('\tColumns to check: {}'.format(columns))
        print(f"\tColumns required: {columns_required}")
        db_ccs = self._get_currency_codes()
        err_list = list()
           
        # Empty Row check only for Required currecny fields
        for column in columns_required:
            empty_rows = df[column].isna()
            empty_rows = empty_rows[empty_rows == True]
            if not empty_rows.empty:
                err_list.extend(
                    'Row {}, Column {}'.format(str(index + 2), column.title())
                    for index in empty_rows.index.tolist())
        
        # Bad Currencies for all columns with values
        for column in columns:
            s = df[column].dropna().apply(
                lambda x: True if str(x).lower() in db_ccs else False)
            s = s[s == False]
            if not s.empty:
                err_list.extend(
                    'Row {}, Column {}'.format(str(index + 2), column.title())
                    for index in s.index.tolist())

        return (False, err_list) if err_list else (True, None)

    def spend_validation(self, data):
        print('Spend Validation')
        df = data.copy()
        df_columns = df.columns.tolist()
        err_list = list()

        spend_columns = self._get_columns_by_stage_name('room_spend')
        for column in spend_columns:
            if column in df_columns:
                s = df[column].dropna().apply(self._check_spend)
                s = s[s == False]
                if not s.empty:
                    err_list.extend(
                        'Row {}, Column {}'.format(str(index + 2), column.title())
                        for index in s.index.tolist()) 

        return (False, err_list) if err_list else (True, None)

    def state_validation(self, data):
        print('State Validation')
        # Three error scenarios
        err_missing_state = list()
        err_invalid_state = list()
        err_shouldnt_be_here = list()

        us_countries = ['united states', 'us']
        ca_countries = ['canada', 'ca']
        required_state_countries = us_countries + ca_countries
        
        df = data.copy()
        df_columns = df.columns.tolist()
        state_columns, country_columns, country_code_columns = self._get_state_columns()
        # Only consider state columns that appear in this DF
        for column_list in [state_columns, country_columns, country_code_columns]:
            for column in column_list:
                if column not in df_columns:
                    column_list.remove(column)
        print('\tColumns to check: [\'{}\', \'{}\', \'{}\']'.format(state_columns[0], country_columns[0], country_code_columns[0]))
        
        # Should end up with a single column for each
        column_state, column_country, column_country_code = state_columns[0], country_columns[0], country_code_columns[0]
        canada_list, us_list = self._get_state_codes()

        # UPDATE: 2020-06-12: No validation error for non-US/Canada countries with State values
        #         Leaving the error category so FE won't need to change, but always blank
        for ind in df.index:
            if pd.isna(df[column_state][ind]):
                # 1. Blank value. Is that okay?
                if (str(df[column_country][ind]).lower() in required_state_countries
                        or str(df[column_country_code][ind]).lower() in required_state_countries):
                    err_missing_state.append(f"Row {ind+2}, {column_state.title()}")
            else:
                # 2. Not a Blank value. Is that okay?
                if (str(df[column_country][ind]).lower() in required_state_countries
                    or str(df[column_country_code][ind]) in required_state_countries):
                    # 3. Should have a value, is it correct?
                    if df[column_country][ind].lower() in us_countries:
                        if df[column_state][ind].lower() not in us_list:
                            err_invalid_state.append(f"Row {ind+2}, {column_state.title()}")
                    else:
                       if df[column_state][ind].lower() not in canada_list:
                            err_invalid_state.append(f"Row {ind+2}, {column_state.title()}") 

        if err_shouldnt_be_here or err_missing_state or err_invalid_state:
            return(False, {
                            'stateShouldBeBlank': err_shouldnt_be_here, 
                            'stateMissing': err_missing_state,
                            'stateInvalid': err_invalid_state
                            })
        else:
            return(True, None)

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
    def _check_boolean(bool_check):
        bools = ['y', 'n', 'yes', 'no']
        ret = True if str(bool_check).lower() in bools else False

        return ret

    @staticmethod
    def _check_checkout_date(checkout, date_end):
        MAX_DAYS = 30
        okay = True
        try:
            checkout_date = datetime.strptime(str(checkout), '%Y-%m-%d %H:%M:%S')
            days_delta = abs((checkout_date.date() - date_end).days)
            okay = False if days_delta > MAX_DAYS else True
        except ValueError:
            # If value isn't a datetime it will be caught in date validation section
            pass
        return okay

    @staticmethod
    def _check_city(city_check):
        match = False
        if city_check:
            pattern = re.compile(r'[a-zA-Z]')
            match = pattern.match(str(city_check))
        
        return True if match else False

    @staticmethod
    def _check_numeric(num_check):
        try:
            num = float(str(num_check))
            ret = True
        except ValueError:
            ret = False
        return ret

    @staticmethod
    def _check_spend(spend):
        okay = True
        try:
            num = float(str(spend))
            okay = False if num < 1 else True
        except ValueError:
            # Data type errors will be flagged elsewhere
            pass
        return okay

    def _get_all_columns(self, source_id):
        columns_required = []
        columns_type = {}
        try:
            source = (
                self.advito_session.query(AdvitoApplicationTemplateSource)
                    .filter(AdvitoApplicationTemplateSource.id == source_id)
                    .one()
            )
            template_columns = (
                self.advito_session.query(AdvitoApplicationTemplateColumn)
                    .filter(AdvitoApplicationTemplateColumn.advito_application_template_id == source.advito_application_template_id)
                    .order_by(AdvitoApplicationTemplateColumn.column_order)
                    .all()
            )
            columns = [column.column_name.lower() for column in template_columns]
            for column in template_columns:
                if column.is_required:
                    columns_required.append(column.column_name.lower())
                columns_type[column.column_name.lower()] = column.data_type.lower()

        except Exception as e:
            columns = [str(e)]

        return columns, columns_required, columns_type

    def _get_columns_by_stage_name(self, stage_column_name):
        results = []
        columns = (
            self.advito_session.query(AdvitoApplicationTemplateColumn.column_name)
            .filter(AdvitoApplicationTemplateColumn.stage_column_name == stage_column_name)
            .distinct()
            .all()
        )
        for column in columns:
            if column[0].lower() not in results:
                results.append(column[0].lower())
        return results

    def _get_currency_codes(self):
        currency_codes = (
            self.advito_session.query(Currency.currency_code)
            .all()
        )
        return [cc[0].lower() for cc in currency_codes]

    def _get_currency_columns(self):
        currency = []
        currency_required = []

        currency_columns = (
            self.advito_session.query(AdvitoApplicationTemplateColumn.column_name)
            .filter(AdvitoApplicationTemplateColumn.tag == 'currency')
            .distinct()
            .all()
        )
        currency = [column[0].lower() for column in currency_columns]

        currency_required = (
            self.advito_session.query(AdvitoApplicationTemplateColumn.column_name)
            .filter(AdvitoApplicationTemplateColumn.tag == 'currency')
            .filter(AdvitoApplicationTemplateColumn.is_required == True)
            .distinct()
            .all()
        )
        currency_required = [column[0].lower() for column in currency_required]

        return currency, currency_required

    @staticmethod
    def _get_excel_column_label(column_index):
        EXCEL_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        header = []

        while column_index:
            column_index, rem = divmod(column_index-1, 26)
            header[:0] = EXCEL_LETTERS[rem]
    
        return ''.join(header)

    def _get_state_codes(self):
        state_code_list = []
        geo_country_ids = [34, 203]     # 34: CA, 203: US

        for geo_country_id in geo_country_ids:
            states = (
                self.advito_session.query(GeoState)
                .filter(GeoState.geo_country_id == geo_country_id)
                .all()
            )
            state_code_list.append([state.state_code.lower() for state in states])

        return state_code_list[0], state_code_list[1]

    def _get_state_columns(self):
        column_dict = {}
        tags = ['hotel state', 'hotel country', 'hotel country code']

        for tag in tags:
            columns = (
                self.advito_session.query(AdvitoApplicationTemplateColumn.column_name)
                .filter(AdvitoApplicationTemplateColumn.tag == tag)
                .distinct()
                .all()
            )
            column_dict[tag] = [column[0].lower() for column in columns]
        
        return column_dict['hotel state'], column_dict['hotel country'], column_dict['hotel country code']

    def _get_date_columns(self):
        columns = (
            self.advito_session.query(AdvitoApplicationTemplateColumn.column_name)
            .filter(AdvitoApplicationTemplateColumn.data_type == 'date')
            .distinct()
            .all()
        )
        return [column[0].lower() for column in columns]

if __name__ == '__main__':
    Validator().validate(job_ingestion_id='18828', bucket_origin='advito-ingestion-templates', bucket_dest='advito-ingestion-templates', environment='DEV', advito_application_id=1)
