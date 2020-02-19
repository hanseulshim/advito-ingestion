import pandas as pd


class Validator:
    # TODO: Add other validations here
    validators = [
        'credit_card_validation',
    ]

    @classmethod
    def validate(cls, ingest_job_id, file_path):
        df = pd.read_excel(file_path)

        for validator in cls.validators:
            validation = getattr(cls, validator)(df)
            print('{} {}'.format(validator,
                                 'passed' if validation else 'failed'))

            # TODO: Write result to ingest job when specified
            if validation is False:
                break

    @staticmethod
    def credit_card_validation(df):
        mask = df.apply(
            lambda row: row.astype(str).str.contains(r'\d{15}', regex=True).any(),
            axis=1)
        # TODO: Remove print and Return tuple (Result, df with errors)
        if mask.any():
            print(df[mask])
        return False if mask.any() else True


if __name__ == '__main__':
    Validator.validate(ingest_job_id='123456789', file_path='Sample Data CC_V3.xlsx')
