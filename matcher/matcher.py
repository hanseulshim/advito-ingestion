import pandas as pd
from sqlalchemy import func, or_

from db.db import HotelSession
from db.hotel_models import HotelProperty
from db.advito_models import GeoCountry, GeoState

from fuzzywuzzy import fuzz, process


class Matcher:
    def __init__(self):
        self.hotel_session = HotelSession()

    def __del__(self):
        self.hotel_session.close()

    def match(self, ingest_job_id, file_path, sheet_name=None):
        self.hotel_session = HotelSession()
        df = pd.read_excel(
            file_path, nrows=8, sheet_name=sheet_name, dtype=str)
        tmp = df.apply(lambda row: self._match(row), axis=1)
        print(tmp)

    def __match_ids(self, row):
        """
        Return (number of matched ids, msg)
        number_of_matched_ids: -1 if error else 0-4
        msg: error message if error else hotel_property_id
        """
        # create ids dict
        ids_dict = {
            'id_amadeus': row['Amadeus Property ID'],
            'id_apollo': row['Apollo Property ID'],
            'id_sabre': row['Sabre Property ID'],
            'id_worldspan': row['WorldSpan Property ID']
        }
        # build query dict needed for scenario where some keys are missing
        query_dict = {key: value for key, value in ids_dict.items()
                      if not pd.isna(value)}
        if not query_dict:
            print('There are no values for IDs specified')
            ret = (0, None)
        else:
            objs = (
                self.hotel_session.query(HotelProperty)
                    .filter(or_(
                        *[getattr(HotelProperty, key) == value
                          for key, value in ids_dict.items()
                          if not pd.isna(value)]))
                    .all()
            )
            # none of the records are matched
            if len(objs) == 0:
                ret = (0, None)
            # only one record is matched
            if len(objs) == 1:
                hp_obj = objs[0]
                # get number of matched ids
                ids_matched_no = 0
                for key, value in ids_dict.items():
                    if value == getattr(hp_obj, key):
                        ids_matched_no += 1
                ret = (ids_matched_no, hp_obj.id)
            # more than one record is matched
            elif len(objs) > 1:
                # figure one which ids are making issues
                matched_ids = dict()
                for key, value in ids_dict.items():
                    object_ids = list()
                    # check which key is found in which objects
                    for obj in objs:
                        if value == getattr(obj, key):
                            object_ids.append(str(obj.id))
                    matched_ids[key] = object_ids
                msg = (
                    'Keys present for more than one record in hotel_property: '
                    '{}'.format('; '.join(
                        ['{} {} present in hotel_property_ids {}'.format(
                            key,
                            value,
                            ', '.join(matched_ids[key])
                                if matched_ids[key]
                                else None)
                         for key, value in ids_dict.items()]
                    )))
                ret = (-1, msg)
            else:
                ret = (0, None)
        print('Number of matched IDs: {}, HotelPropertyID/error_message: '
              '{}'.format(*ret))
        return ret

    @staticmethod
    def __fuzzy_match(var, choices, limit=50):
        print('\nFuzzy Match: {}'.format(var))
        ret = list()

        ratio = process.extract(var, choices, scorer=fuzz.ratio, limit=limit)
        print('Ratio')
        ret.extend(ratio)
        for item in ratio:
            print(item)

        partial_ratio = process.extract(var, choices, scorer=fuzz.partial_ratio, limit=limit)
        ret.extend(partial_ratio)
        print('Partial Ratio')
        for item in partial_ratio:
            print(item)

        token_set_ratio = process.extract(var, choices, scorer=fuzz.token_set_ratio, limit=limit)
        ret.extend(token_set_ratio)
        print('Token Set Ratio')
        for item in token_set_ratio:
            print(item)

        return ret

    def _match(self, row):
        print('\n# # # # #\nRow: {} Property Name: {}'.format(
            row.name, row['Hotel Name']))
        matched_id = None
        ids_matched_no, msg = self.__match_ids(row)
        return
        # 1st condition -> 2 or more IDs matched
        if ids_matched_no >= 2:
            print('First Condition Satisfied')
            matched_id = msg
        # continue with algorithm for ids_matched in 0 or 1
        else:
            # check if error happened
            if ids_matched_no == -1:
                print('Matching ID error: {}. Proceed with Matching'.format(msg))
            # match hotel_name which is needed for 2nd, 3rd and 4th condition
            # check if there is hotel_property with exact name which will
            # satisfy 2nd condition -> 1 ID and 75% hotel_name
            # in order to avoid losing time in fuzzy search
            hp_hn_match_objs = (
                self.hotel_session.query(HotelProperty)
                .filter(HotelProperty.property_name == row['Hotel Name'])
                .all()
            )

            if len(hp_hn_match_objs) == 1 and ids_matched_no == 1:
                print('Second condition satisfied. '
                      'Hotel Name 100% match found in hotel_property '
                      'along with one ID')
                matched_id = hp_hn_match_objs[0].id
            # use Fuzzy to match hotel_name
            else:
                print('Hotel Name 100% match not found, proceed with fuzzy '
                      'match')
                # hotel name match
                hp_property_names = pd.read_sql(
                    self.hotel_session.query(HotelProperty.id,
                                             HotelProperty.property_name)
                        .statement,
                    self.hotel_session.bind).set_index('id')
                hotel_name_matches = self.__fuzzy_match(
                    row['Hotel Name'], hp_property_names['property_name'])

                # 2nd condition -> 1 ID and 75% hotel_name
                if matched_id is None:
                    matched_id = self.__2nd_condition(
                        hotel_name_matches=hotel_name_matches,
                        amadeus_id=row['Amadeus Property ID'],
                        apollo_id=row['Apollo Property ID'],
                        sabre_id=row['Sabre Property ID'],
                        worldspan_id=row['WorldSpan Property ID']
                    )

                # # 3rd condition -> 100% hotel_name, city, state and country code
                # if matched_id is None:
                #     matched_id = self.__3rd_condition(
                #         hotel_name_matches=hotel_name_matches,
                #         city_name=row['City Name'],
                #         country_code=row['Country Code'],
                #         state_code=row['State Code']
                #     )

                # 4th condition -> 90% hotel_name, 90% clean_phone
                if matched_id is None:
                    matched_id = self.__4nd_condition(hotel_name_matches, row['Phone Number'])
                print(matched_id)

        return matched_id

    def __2nd_condition(self,
                        hotel_name_matches,
                        amadeus_id,
                        apollo_id,
                        sabre_id,
                        worldspan_id):
        """
        2nd condition -> 1 ID and 75% hotel_name
        :param amadeus_id:
        :param apollo_id:
        :param sabre_id:
        :param worldspan_id:
        :param hotel_name_matches:
        :return:
        """
        print('\n2nd Condition')
        matched_id = None
        score_threshold = 75
        # filter hotel name match ids based on score_threshold
        hn_match_ids = set(
            [hp_id for hp_hotel_name, score, hp_id in hotel_name_matches
             if score >= score_threshold])
        # cross match on hp_match_ids_set and matched_ids
        hp_objs = (
            self.hotel_session.query(HotelProperty)
            .filter(HotelProperty.id.in_(hn_match_ids))
            .filter(
                (HotelProperty.id_amadeus == amadeus_id)
                | (HotelProperty.id_apollo == apollo_id)
                | (HotelProperty.id_sabre == sabre_id)
                | (HotelProperty.id_worldspan == worldspan_id))
            .all()
        )
        if len(hp_objs) == 1:
            matched_id = hp_objs[0].id
            print('Second Condition Satisfied, match_id {}'.format(matched_id))
        return matched_id

    def __3rd_condition(self, hotel_name_matches, city_name, country_code, state_code):
        """
        3rd condition -> 100% hotel_name, city, state and country code
        :param hotel_name_matches:
        :param city_name:
        :param country_code:
        :param state_code:
        :return:
        """
        print('\n3rd Condition')
        matched_id = None
        score_threshold = 100
        # filter hotel name match ids based on score_threshold
        hn_match_ids = set(
            [hp_id for hp_hotel_name, score, hp_id in hotel_name_matches
             if score >= score_threshold])
        # build query based on params
        query = (
            self.hotel_session.query(HotelProperty)
            .filter(HotelProperty.id.in_(hn_match_ids))
        )
        if city_name:
            query = query.filter(func.lower(HotelProperty.city) == city_name.lower())
        if country_code:
            query = (
                query
                .join(GeoCountry,
                      GeoCountry.id == HotelProperty.geo_country_id)
                .filter(
                    (GeoCountry.country_code_2char == country_code)
                    | (GeoCountry.country_code_3char == country_code)
                    | (GeoCountry.country_code_numeric == country_code))
            )
        if state_code:
            query = (
                query
                .join(GeoState,
                      GeoState.id == HotelProperty.geo_state_id)
                .filter(GeoState.state_code == state_code)
            )
        hp_objs = query.all()
        print(hp_objs)

        if len(hp_objs) == 1:
            matched_id = hp_objs[0].id
            print('Third Condition Satisfied, match_id {}'.format(matched_id))
        return matched_id

    def __4nd_condition(self, hotel_name_matches, phone_number):
        """
        4th condition -> 90% hotel_name, 90% clean_phone
        :param hotel_name_matches:
        :param phone_number:
        :return:    None or hotel_property_id
        """
        print('\n4th Condition')
        matched_id = None
        hotel_name_score_threshold = 90
        phone_number_score_threshold = 90
        if phone_number:
            # clean phone
            phone = (
                phone_number
                .strip()
                .replace('/', '')
                .replace('-', '')
                .replace(' ', '')
            )
            # phone number match
            hp_phone_numbers = pd.read_sql(
                self.hotel_session.query(HotelProperty.id,
                                         HotelProperty.phone_primary)
                    .statement,
                self.hotel_session.bind).set_index('id')
            phone_number_matches = self.__fuzzy_match(
                phone, hp_phone_numbers['phone_primary'].astype(str))
            # filter phone number match ids based on score_threshold
            pn_match_ids = set(
                [hp_id for hp_phone_number, score, hp_id in phone_number_matches
                 if score >= phone_number_score_threshold])
            # filter hotel name match ids based on score_threshold
            hn_match_ids = set(
                [hp_id for hp_hotel_name, score, hp_id in hotel_name_matches
                 if score >= hotel_name_score_threshold])
            # find intersection
            hp_objs = hn_match_ids.intersection(pn_match_ids)
            if len(hp_objs) == 1:
                matched_id = list(hp_objs)[0]
                print('Fourth Condition Satisfied, match_id {}'.format(matched_id))
            return matched_id


if __name__ == '__main__':
    Matcher().match(ingest_job_id='123456789',
                    file_path='MatchingTest.xlsx',
                    sheet_name='Transaction Template')
