import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm
import pickle
import logging
import random
import time


class Shop(object):
    def __init__(self, row):
        self.name = row['name']
        self.category = row['category'].replace('-', ' ')
        self.description = Shop.process_search_tags(row).replace('|', ', ')
        self.location = row['centroid']
        self.level = row['level']
        self.level_descr = row['level_description']

    def form_json(self):
        return {
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'location': self.location,
            'level': self.level,
            'level_description': self.level_descr
        }

    @staticmethod
    def process_search_tags(row):
        search_tags = row['searchTags']
        search_tags = search_tags if isinstance(search_tags, str) else ''
        return search_tags


class Assistant(object):
    SHOP_CSV = '../StaticData/shops.csv'
    W2V = '../StaticData/glove.840B.300d.txt'
    SHOP_IMPRINTS = '../StaticData/shop_imprints.pickle'

    def _dump_shop_imprints(self):
        pickle.dump(self.shops_imprints, open(self.SHOP_IMPRINTS, 'wb'))

    def _load_shop_imprints(self):
        self.shops_imprints = pickle.load(open(self.SHOP_IMPRINTS, 'rb'))

    def __init__(self, update_shops=True):
        self._w2v_size = 300
        self.shops_imprints = []
        self.shops_features = {}
        self._load_word2vec_model()
        self._get_shops_imprints(update_shops)

    def _get_shops_imprints(self, update_shops):
        if update_shops:
            self._update_shops_imprints()
            self._dump_shop_imprints()
        else:
            self._load_shop_imprints()
        self._get_shops_features()

    def _get_shops_features(self):
        for shop_imprint, shop in self.shops_imprints:
            self.shops_features[shop.name] = shop_imprint

    def _load_word2vec_model(self):
        debug = False
        start_time = time.time()

        def get_coefs(word, *arr):
            return word, np.asarray(arr, dtype='float32')

        if not debug:
            with open(self.W2V) as f:
                self._word2vec = dict(get_coefs(*line.strip().split(' ')) for line in f)
        else:
            with open(self.W2V) as f:
                res = []
                for line in f:
                    res.append(get_coefs(*line.strip().split(' ')))
                    if len(res) > 10000:
                        break
                self._word2vec = dict(res)

        elapsed_time = time.time() - start_time
        logging.error('_load_word2vec_model; word2vec loaded, size: {}, time: {}'.format(len(self._word2vec), elapsed_time))

    def _get_vector(self, words):
        if isinstance(words, str):
            return self._word2vec.get(words.lower(), np.zeros(self._w2v_size, dtype='float32'))
        return np.sum([self._get_vector(word) for word in words], axis=0) / len(words)

    def _extract_shops_key_vectors(self, row):
        search_tags = Shop.process_search_tags(row)

        result = [self._get_vector(elem) for elem in search_tags.split('|')]
        result += [self._get_vector(row['category'].split('-'))]
        return result

    def _update_shops_imprints(self):
        shops = pd.read_csv(self.SHOP_CSV)
        for _, row in shops.iterrows():
            key_vectors = self._extract_shops_key_vectors(row)
            for key_vector in key_vectors:
                self.shops_imprints.append((key_vector, Shop(row)))

    # content is a list of strings
    def form_user_imprint(self, content, fav_shops):
        # easter egg :)
        content = ['coffee'] if len(content) == 0 else content
        start_time = time.time()
        results = np.sum(
            [self._get_vector(word) for word in content] +
            [self.shops_features[shop] for shop in fav_shops], axis=0
        ) / (len(content) + len(fav_shops))
        elapsed_time = time.time() - start_time
        logging.error('form_user_imprint; time: {}'.format(elapsed_time))
        return results

    def _compute_closeness(self, rhs, lhs):
        randomize_delta = 0.001
        denominator = norm(rhs) * norm(lhs)
        if denominator < 0.001:  # to make it more interesting
            return -1.0 + random.uniform(0, randomize_delta)
        cos_sim = dot(rhs, lhs) / denominator
        return cos_sim

    def _compute_shops_closeness(self, user_imprint):
        closeness = []
        for shop_imprint, shop in self.shops_imprints:
            closeness.append((self._compute_closeness(shop_imprint, user_imprint), shop))
        closeness.sort(key=lambda x: -x[0])
        return closeness

    # user_imprint is a vector from word2vec
    # return json to send
    def make_recommendation(self, user_imprint, banned_shops=None, count=3):
        start_time = time.time()
        assert count > 0
        banned_shops_set = set(banned_shops) if banned_shops is not None else {}
        resulted_shops = {}
        closeness = self._compute_shops_closeness(user_imprint)
        for distance, shop_candidate in closeness:
            if shop_candidate.name in resulted_shops:
                continue
            # remove banned shops
            elif shop_candidate.name in banned_shops_set:
                continue
            else:
                resulted_shops[shop_candidate.name] = shop_candidate
                if len(resulted_shops) >= count:
                    break
        elapsed_time = time.time() - start_time
        logging.error('make_recommendation; time: {}'.format(elapsed_time))
        return [shop.form_json() for shop in resulted_shops.values()]

    def make_search(self, user_imprint, question, count=3):
        words = question.lower().split(' ')
        qvector = self._get_vector(words)
        return self.make_recommendation(qvector, banned_shops=[], count=count)


if __name__ == '__main__':
    assistant = Assistant()

    content = ['pasta', 'football', 'hat', 'pomade']
    user_imprint = assistant.form_user_imprint(content, [])
    results = assistant.make_recommendation(user_imprint, count=4)
    for result in results:
        print(result)
