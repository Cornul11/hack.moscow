import pandas as pd
from ast import literal_eval


class ShopSearcher(object):
    SHOP_CSV = '../StaticData/shops.csv'

    def __init__(self):
        self.df = None
        self._load_shop_locations()

    def _load_shop_locations(self):
        self.df = pd.read_csv(self.SHOP_CSV)[['venue_id', 'name', 'centroid']]
        self.df[['lat', 'lon']] = pd.DataFrame([literal_eval(x) for x in self.df.centroid.values], index=self.df.index, columns=['1', '2'])

    def get_closest(self, venue_id, lat, lon, count):
        result = self.df[self.df['venue_id'] == venue_id][['lat', 'lon', 'name']]
        result['mse'] = (self.df['lat'] - lat)**2 + (self.df['lon'] - lon)**2
        closest = result.sort_values(by='mse')['name'].iloc[:count]
        return closest.tolist()


if __name__ == '__main__':
    shop_searcher = ShopSearcher()
    results = shop_searcher.get_closest('DM_20518', 55.75561790448445, 37.61440535517105, count=3)
    print(results)
