import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "slippage_model.pkl")

class SlippageModel:
    def __init__(self):
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
        else:
            # Dummy model with no training yet
            self.model = LinearRegression()
            self.model.coef_ = np.array([0.001])  # example coefficient
            self.model.intercept_ = 0

    def predict(self, quantity_usd):
        """
        Predict slippage based on quantity in USD.
        """
        X = np.array(quantity_usd).reshape(-1, 1)
        slippage = self.model.predict(X)
        return slippage[0]

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        joblib.dump(self.model, MODEL_PATH)
