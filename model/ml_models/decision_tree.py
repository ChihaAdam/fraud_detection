from sklearn.tree import DecisionTreeClassifier


def decision_tree_model():
    return DecisionTreeClassifier(max_depth=5, random_state=42)

