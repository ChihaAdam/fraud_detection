from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def svm_model():
    # SVM : normalisation obligatoire
    return make_pipeline(StandardScaler(), SVC(kernel="rbf"))


