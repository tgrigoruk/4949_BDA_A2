import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


DATA_PATH = "./static/data/"
BINARIES_PATH = "./static/binaries/"

TARGET = "satisfaction"


df_test = pd.read_csv(DATA_PATH + "test.csv", index_col=0, header=0)
df_train = pd.read_csv(DATA_PATH + "train.csv", index_col=0, header=0)


def prepare_data(df):
    # replace 'satisfaction' with 0 and 1
    df[TARGET] = df[TARGET].map({"neutral or dissatisfied": 0, "satisfied": 1})

    # create dummy variables for categorical columns
    string_columns = df.select_dtypes(include=["object"]).columns.to_list()
    df = pd.get_dummies(df, columns=string_columns, dtype=int)

    # create bin for Age group
    age_label = "Age_40-60"
    age_bin = pd.cut(
        df["Age"], bins=[0, 38, 60, 100], labels=["under 40", age_label, "over 60"]
    )
    dummy_df = pd.get_dummies(age_bin, columns=["AgeBin"], dtype=int)
    df = pd.concat(([df, dummy_df[age_label]]), axis=1)

    return df


df_train = prepare_data(df_train)
df_test = prepare_data(df_test)

SIGNIFICANT_FEATURES = [
    "Class_Business",
    "Type of Travel_Personal Travel",
    "Age_40-60",
    "Seat comfort",
    "Leg room service",
    "Inflight entertainment",
    "Inflight wifi service",
    "Online boarding",
    "On-board service",
]

X_train = df_train[SIGNIFICANT_FEATURES]
y_train = df_train[TARGET]
X_test = df_test[SIGNIFICANT_FEATURES]
y_test = df_test[TARGET]

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
joblib.dump(scaler, BINARIES_PATH + "scaler.joblib")

model_rf = RandomForestClassifier(n_estimators=100)
model_rf.fit(X_train, y_train)

joblib.dump(model_rf, BINARIES_PATH + "model_rf.joblib")
