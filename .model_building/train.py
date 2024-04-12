import pandas as pd

PATH = "./.model_building/data/"

df_test = pd.read_csv(PATH + "test.csv", index_col=0, header=0)
df_train = pd.read_csv(PATH + "train.csv", index_col=0, header=0)

# concatenate the dataframes
df = pd.concat([df_train, df_test], axis=0, ignore_index=True)

# replace missing values with the mean, convert to int

df["Arrival Delay in Minutes"].fillna(
    df["Arrival Delay in Minutes"].mean(), inplace=True
)
df["Arrival Delay in Minutes"] = df["Arrival Delay in Minutes"].astype(int)
df.drop("id", axis=1, inplace=True)

# replace 'satisfaction' with 0 and 1
df["satisfaction"] = df["satisfaction"].map(
    {"neutral or dissatisfied": 0, "satisfied": 1}
)

# create dummy variables
string_columns = df.select_dtypes(include=["object"]).columns.to_list()
df = pd.get_dummies(df, columns=string_columns, drop_first=True, dtype=int)

df.info()

# exploratorey data analysis
from viz import *


# print_df(df)
# plot_heatmap(df, save=True)
hot_features = [
    "Online boarding",
    "Inflight entertainment",
    "Seat comfort",
]

# show_scatter_matrix(df, "Flight Distance", "satisfaction")
# show_boxplot(df, "Flight Distance")

# show_histogram(df, "Online boarding", save=False)

# show_multiple_boxplots(df, cols, save=True)

# multiple_plots(df, cols, plot=sns.histplot, title="histogram", save=True)
# pair_plot(df[[TARGET, *cols]])


# exit()

X = df.drop("satisfaction", axis=1)
y = df["satisfaction"]

# split the data
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# train the model

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

model = LogisticRegression(fit_intercept=True, solver="liblinear")
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))


def evaluate_model(y_test, y_pred, title="Model"):
    confusion_matrix = pd.crosstab(
        y_test, y_pred, rownames=["Actual"], colnames=["Predicted"]
    )
    print(confusion_matrix)
    print(f"\n*** {title} - Classification Report ***\n")
    print(classification_report(y_test, y_pred, zero_division=1))
