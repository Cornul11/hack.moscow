import torch
import torch.nn as nn
import pickle
from .assistant import Shop


class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()

        self.lstm = nn.LSTM(input_size, hidden_size, 1)
        self.hidden2out = nn.Linear(hidden_size, output_size)

    def forward(self, inp):
        lstm_out, _ = self.lstm(inp)
        out = self.hidden2out(lstm_out)
        return out


class LongTermRecommendations(object):
    MODEL_PATH = '../StaticData/model.torch'
    SHOPS_IMPRINTS = '../StaticData/shop_imprints.pickle_bk'

    def __init__(self):
        self.model = RNN(300, 32, 300)
        self.model.load_state_dict(torch.load(self.MODEL_PATH))
        self.model.eval()
        self.shop_vecs = {}
        self.set_shop_vectors()

    def find_closest(self, vec):
        distances = []
        for shop, vec2 in shop_vecs.items():
            distances.append((((vec - vec2) ** 2).sum(), shop))
        return sorted(distances)[1]

    def set_shop_vectors(self):
        shops_imprints = pickle.load(open(self.SHOPS_IMPRINTS, 'rb'))
        for shop_imprint, shop in shops_imprints:
            self.shop_vecs[shop.name] = shop_imprint

    def predict(self, src_tensor):
        self.model.eval()
        output = self.model(src_tensor.view(src_tensor.size(2), 1, -1))
        return self.find_closest(output[0, 0].detach().numpy())

    def inputTensor(self, vecs):
        return torch.tensor(vecs[:-1]).reshape(300, 1, -1)

    def recommend(self, history):
        vec = self.inputTensor(history)
        return self.predict(vec)
