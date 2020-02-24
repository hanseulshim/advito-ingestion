import pandas as pd


class Validator:
    # TODO: Add other validations here
    validators = [
        'credit_card_validation',
    ]

    @classmethod
    def validate(cls, ingest_job_id, file_path):
        validation_passed = False
        msg = None
        df = pd.read_excel(file_path, dtype=str)

        for validator in cls.validators:
            validation_passed, msg = getattr(cls, validator)(df)
            print('{} {} {}'.format(validator,
                                    'passed' if validation_passed else 'failed',
                                    msg))

            # TODO: Write result to ingest job when specified
        return validation_passed, msg

    @staticmethod
    def credit_card_validation(data):
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
            msg = 'Potential Unmasked Credit Card Number found in:\n{}'.format(
                '\n'.join(['- Line {}'.format(line) for line in unmasked_data_rows])
            )
            ret = (False, msg)
        else:
            ret = (True, )
        return ret


if __name__ == '__main__':
    # Validator.validate(ingest_job_id='123456789', file_path='ValidationTest.xlsx')
    Validator.validate(ingest_job_id='123456789', file_path='https://hotel-api-downloads.s3.us-east-2.amazonaws.com/ValidationTest.xlsx')
