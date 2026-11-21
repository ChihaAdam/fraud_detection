from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


def logistic_regression_model():
    return make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))



