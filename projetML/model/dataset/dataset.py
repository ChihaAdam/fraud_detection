import pandas as pd
from imblearn.under_sampling import NearMiss


classes = {
    "A": {0: 492, 1: 492},
    "B": {0: 492*2, 1: 492},
    "C": {0: 492*3, 1: 492},
    "D": {0: 492*4, 1: 492},
    "E": {0: 492*5, 1: 492},
}


def generate_under_sampling_with_nearmiss(X,y,cls):
    nm = NearMiss(
        sampling_strategy=classes[cls],
        version=1,
        n_neighbors=3
    )

    X_resampled, y_resampled = nm.fit_resample(X, y)

    df_resampled = pd.concat([X_resampled, y_resampled], axis=1)
    df_resampled = df_resampled.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    df_resampled.to_csv(f"./creditcard_nearmiss_{cls}.csv", index=False)

    print("dimension originale: ", df.shape)
    print("dimension aprés nearmiss", df_resampled.shape)

    print("\navant:")
    print(y.value_counts())

    print("\naprés:")
    print(y_resampled.value_counts())


if __name__ == "__main__":
    df = pd.read_csv('./creditcard.csv')

    X = df.drop(columns=['Class'])
    y = df['Class']
    for cls in ["A", "B", "C", "D", "E"]:
        generate_under_sampling_with_nearmiss(X,y,cls)
