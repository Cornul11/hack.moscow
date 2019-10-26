import configparser
import pickle
import pandas as pd
import here_sdk
from venues_static import VENUE_BB, VENUE_IDS


class VenuesDownloader:
    CONFIG_FP = 'config.conf'
    VENUE_CSV = '../StaticData/venues.csv'
    SHOP_CSV = '../StaticData/shops.csv'

    def __init__(self):
        creds = self._load_credentials()
        self.app_id = creds['here.api']['app_id']
        self.app_code = creds['here.api']['app_code']
        self.signature = None
        self.policy = None
        self.key_pair_id = None
        # self._set_signature()
        self._set_signature_shadowed()

    def _load_credentials(self):
        config = configparser.ConfigParser()
        config.read(self.CONFIG_FP)
        return config

    def _set_signature(self):
        signature_creds = here_sdk.get_signature(self.app_id, self.app_code)
        signature_tokens = signature_creds['SignatureTokens']
        self.signature = signature_tokens['Signature']
        self.policy = signature_tokens['Policy']
        self.key_pair_id = signature_tokens['Key-Pair-Id']

    def _set_signature_shadowed(self):
        self.signature = 'Orl-O0WFIrtGLJRWgxDSfvSR57CTaUbnCbzb~mr3h2Ww1Z-1VCFDeVGRmefLHi9Mhqwom8oNHmDd5ZBIO1GoktLjSZwYp8nivOw4KNtMdIferqFjfzh8Tsg~NC~nbqwAkpC0d1SpEobCOeyQlPUuA-wHFVxoeTdSltTfaAE3iT7MT6n-OJytxU3jWxSkQ0SZIopte-VEjLya43LpzSrFc3EogEHXQJaXCDqwvRESzYAEYslqfTOQOl4yabfZ3HA6my~ppndSKHTgkA1DS-Lsc-rJ7LGbcEZawMdG9EbtLxRiQwcvb3Ffy9zVvRuCAmOBdYSmy7ptxq9TAMDYFccg5A__'
        self.policy = 'eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHAqOi8vc3RhdGljLSoudmVudWUubWFwcy5hcGkuaGVyZS5jb20vKj9hcHBfaWQ9T21ZV0lValdtNEpIN3hwRW0zVFomYXBwX2NvZGU9c0Z4amV5bEVZVjlQWDY0UFRwX3RIUSIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTU3MjE0MDA2OX0sIklwQWRkcmVzcyI6eyJBV1M6U291cmNlSXAiOiIwLjAuMC4wLzAifSwiRGF0ZUdyZWF0ZXJUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE1NDA1MTc2Njl9fX1dfQ__'
        self.key_pair_id = 'APKAJYHWIIHIUVYKYWZA'

    def dump_venues_indexes(self):
        venues = here_sdk.get_all_venues(self.app_id, self.app_code, self.signature, self.policy, self.key_pair_id)
        pickle.dump(venues, open('venues.pickle', 'wb'))

    def dump_venue(self, filepath = 'venue.pickle'):
        venue = here_sdk.discovery_venue(self.app_id, self.app_code, VENUE_BB['ORYAD'])
        pickle.dump(venue, open(filepath, 'wb'))

    def dump_to_tables(self, venue_info, shops, append = False):
        if not append:
            df_venue = pd.DataFrame([venue_info])
            df_shops = pd.DataFrame(shops)
        else:
            df_venue = pd.read_csv(self.VENUE_CSV)
            df_venue.append([venue_info])
            df_shops = pd.read_csv(self.SHOP_CSV)
            df_shops.append(shops)
        df_venue.to_csv(self.VENUE_CSV, index=False)
        df_shops.to_csv(self.SHOP_CSV, index=False)

    def extract_appropriate_name(self, names):
        return names.get('RST', names.get('ENG', names.get('RUS')))

    def collect_venue_info(self, venue_id, append = False):
        venue = here_sdk.get_full_model(self.app_id, self.app_code, self.signature, self.policy, self.key_pair_id, venue_id)
        names = venue['content']['names']

        venue_info = {
            'venue_id': venue_id,
            'id': venue['gml:id'],
            'owner_id': venue['ownerID'],
            'address': venue['address'],
            'groundLevel': venue['groundLevel'],
            'category': venue['content']['category']['id'],
            'phone_number': venue['content']['phoneNumber'],
            'email': venue['content']['website'],
            'name': self.extract_appropriate_name(names),
            'bb': venue['bb'],  # not csv
            'centroid': venue['centroid']  # not csv
        }
        shops = []
        for idx, level in enumerate(venue['levels']):
            for area in level['outerAreas']:
                for space in area['spaces']:
                    if 'content' in space:
                        space_names = space['content']['names']
                        shop = {
                            'venue_id': venue_id,
                            'id': space.get('gml:id'),
                            'category': space['content']['category']['id'],
                            'phone_number': space['content'].get('phoneNumber'),
                            'email': space['content'].get('email'),
                            'name': self.extract_appropriate_name(space_names),
                            'isClosed': space['isClosed'],
                            'bb': space['bb'],
                            'centroid': space['centroid'],
                            'searchTags': '|'.join(space['content'].get('searchTags', []))
                        }
                        shops.append(shop)
        self.dump_to_tables(venue_info, shops, append)


if __name__ == '__main__':
    venues_downloader = VenuesDownloader()
    venues_downloader.collect_venue_info(VENUE_IDS['ORYAD'])
