"""Create a sample housing dataset and train the house price model."""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression


PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "house_price_model.pkl"


def create_sample_dataset() -> pd.DataFrame:
    """Build a reproducible dataset with prices expressed in lakhs."""
    rows = []
    for area in (800, 1000, 1200, 1500, 1800, 2000, 2200, 2500, 2800, 3200):
        for bedrooms in (1, 2, 3, 4, 5):
            for age in (0, 5, 10, 15, 20, 25):
                # This simple pricing rule makes the generated sample learnable.
                price = 11.63 + (0.02 * area) + (2 * bedrooms) - (0.5 * age)
                rows.append(
                    {
                        "area": area,
                        "bedrooms": bedrooms,
                        "age": age,
                        "price": price,
                    }
                )
    return pd.DataFrame(rows)


def train_and_save_model() -> None:
    """Fit linear regression and save the complete pipeline artifact."""
    dataset = create_sample_dataset()
    features = dataset[["area", "bedrooms", "age"]]
    target = dataset["price"]

    model = LinearRegression()
    model.fit(features, target)
    joblib.dump(model, MODEL_PATH)
    print("Model trained on {} sample homes.".format(len(dataset)))
    print("Saved trained model to: {}".format(MODEL_PATH))


if __name__ == "__main__":
    train_and_save_model()
