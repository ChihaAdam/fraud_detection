from sklearn.tree import DecisionTreeClassifier


def decision_tree_model():
    # Arbre de décision : pas besoin de normalisation
    return DecisionTreeClassifier(max_depth=5, random_state=42)

