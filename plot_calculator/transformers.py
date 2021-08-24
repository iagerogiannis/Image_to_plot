import numpy as np
import pandas as pd


class GeneralizedTransformer:

    def __init__(self):
        self.ax = None
        self.ay = None

    def calibrate(self, px, py):

        def calculate(p, q, r):

            p = np.array(p)
            q = np.array(q)
            r = np.array(r)

            pq = q - p
            pr = r - p

            abc = np.cross(pq, pr)

            d = - np.dot(abc, p)

            return np.array([- abc[0] / abc[2], - abc[1] / abc[2], - d / abc[2]])

        self.ax = calculate(*px)
        self.ay = calculate(*py)

    def x(self, x, y):
        return np.dot(self.ax, np.array([x, y, 1]))

    def y(self, x, y):
        return np.dot(self.ay, np.array([x, y, 1]))

    def coordinates(self, x, y):
        return [self.x(x, y), self.y(x, y)]

    def transform(self, df):
        transformed = []
        for index, row in df.iterrows():
            transformed.append(self.coordinates(row['X'], row['Y']))
        transformed = np.array(transformed).T.tolist()
        return pd.DataFrame({"X": transformed[0],
                             "Y": transformed[1]})


class OrthoTransformer(GeneralizedTransformer):

    def __init__(self):
        super().__init__()

    def calibrate(self, px, py):
        super().calibrate(px + [[px[0][0], px[0][1] + 1., px[0][2]]], py + [[py[0][0] + 1., py[0][1], py[0][2]]])

    def x(self, x, **kwargs):
        return super().x(x, 1.)

    def y(self, y, **kwargs):
        return super().y(1., y)

    def coordinates(self, x, y):
        return [self.x(x), self.y(y)]
