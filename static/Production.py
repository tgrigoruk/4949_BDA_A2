import pandas as pd
import joblib
import torch
import numpy as np

TEST_DATA_PATH = "./A2/data/"
BINARIES_PATH = "./A2/binaries/"
PREDICTIONS_PATH = "./A2/predictions/"
TARGET = "satisfaction"

# LOAD TEST DATA
data = pd.read_csv(TEST_DATA_PATH + "test.csv", index_col=0, header=0)
# drop target column immediately
data.drop([TARGET], axis=1, inplace=True)

scaler = joblib.load(BINARIES_PATH + "scaler.joblib")


# PREPARE DATA
def prepare_data(df):
    df = pd.get_dummies(df, columns=["Class", "Type of Travel"], dtype=int)

    age_label = "Age_40-60"
    age_bin = pd.cut(df["Age"], bins=[38, 60], labels=[age_label])
    dummy_df = pd.get_dummies(age_bin, columns=["AgeBin"], dtype=int)
    df = pd.concat(([df, dummy_df[age_label]]), axis=1)

    significant_features = scaler.feature_names_in_.tolist()
    return df[significant_features]


data_prepared = prepare_data(data)
data_scaled = scaler.transform(data_prepared)
data_tensor = torch.from_numpy(data_scaled.astype(np.float32))

# LOAD BINARIES
models = {
    "Random Forest model": joblib.load(BINARIES_PATH + "model_rf.joblib"),
    "Neural Network model": joblib.load(BINARIES_PATH + "model_nn.joblib"),
    "Stacked model": joblib.load(BINARIES_PATH + "model_stacked.joblib"),
}

# MAKE PREDICTIONS
for model_name, model in models.items():
    predictions = model.predict(data_tensor)
    filename = PREDICTIONS_PATH + model_name + " predictions.csv"
    pd.DataFrame(predictions).to_csv(filename, index=False, header=["satisfaction"])
