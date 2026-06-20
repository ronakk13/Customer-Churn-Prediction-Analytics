import pandas as pd
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from lightgbm import LGBMClassifier
from imblearn.over_sampling import SMOTE


def load_data():
    df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")
    return df

def preprocess_data(df):
    df = df.drop(columns=["customerID"])

    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].fillna(df['TotalCharges'].mean())

    df['gender'] = df['gender'].map({"Male":1,"Female":0})

    df['MultipleLines'] = df['MultipleLines'].replace({'No phone service': 'No'})

    for column in df.select_dtypes(include="object").columns:
        if set(df[column].unique()) == {"Yes","No","No internet service"}:
            df[column] = df[column].replace({'No internet service': 'No'})

    for column in df.select_dtypes(include="object").columns:
        if set(df[column].unique()) == {"Yes","No"}:
            df[column] = df[column].map({"Yes":1,"No":0})

    df['TotalServices'] = df[['MultipleLines', 'OnlineSecurity', 'OnlineBackup', 
                        'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']].sum(axis=1)

    df['RiskScore'] = (
        (df['Contract'] == 'Month-to-month').astype(int) +
        (df['PaymentMethod'] == 'Electronic check').astype(int) +
        (df['InternetService'] == 'Fiber optic').astype(int) +
        (df['SeniorCitizen'] == 1).astype(int) + 
        (df['tenure']<=15).astype(int)
    )

    df = pd.get_dummies(df, columns=['InternetService', 'Contract', 'PaymentMethod'], dtype=int)

    return df


def train_model(X_train,y_train):

    smote = SMOTE(random_state=42)
    X_train_sm , y_train_sm = smote.fit_resample(X_train,y_train)

    model = LGBMClassifier(random_state=42,n_jobs=-1)

    param_dist = {
        "learning_rate" : [0.01,0.03,0.05,0.07],
        "n_estimators"  : [180,200,250,300,350],
        "min_child_samples" : [20,30,35,40,45],
        "num_leaves" : [50,60,70,80,85],
        "max_depth" : [15,20,25,-1]
    }

    random_search = RandomizedSearchCV(
        estimator=model,
        param_distributions=param_dist,
        n_iter=40,
        cv=5,
        scoring="f1",
        random_state=42,
        n_jobs=-1
    )

    random_search.fit(X_train_sm, y_train_sm)

    return random_search.best_estimator_


def model_evaluation(model,X_test,y_test,feature_names):

    y_prob = model.predict_proba(X_test)[:,1]
    threshold = 0.30
    y_pred = (y_prob >= threshold).astype(int)

    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))

    print("Accuracy :", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred))
    print("Recall   :", recall_score(y_test, y_pred))
    print("F1 Score :", f1_score(y_test, y_pred))
    print("ROC AUC  :", roc_auc_score(y_test, y_prob))

    # Confusion Matrix Display

    ConfusionMatrixDisplay.from_predictions(
        y_test,
        y_pred,
        display_labels=["No Churn","Churn"],
        cmap="Blues",
        colorbar=False
    )

    plt.title("Customer Churn Prediction - Confusion Matrix")
    plt.xlabel("Predicted Class")
    plt.ylabel("Actual Class")

    plt.tight_layout()
    plt.show()

    # Feature Importance Visualization

    feature_imp = pd.DataFrame({
        "feature" : feature_names,
        "Importance" : model.feature_importances_
    }).sort_values(by="Importance",ascending=False)

    print("\nTop Features")
    print(feature_imp.head(15))

    plt.figure(figsize=(10,6))
    plt.barh(
        feature_imp.head(10)["feature"],
        feature_imp.head(10)["Importance"]
    )
    plt.title("Top 10 Feature Importance")
    plt.tight_layout()
    plt.show()


def main():
    
    df = load_data()

    df = preprocess_data(df)

    X = df.drop(columns=['Churn'])
    y = df['Churn']

    X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

    model = train_model(X_train,y_train)

    joblib.dump(
    {
        "model": model,
        "features": list(X.columns)
    },
    "customer_churn_model.pkl"
    )

    saved_obj = joblib.load(
    "customer_churn_model.pkl"
    )

    model = saved_obj["model"]
    features = saved_obj["features"]

    model_evaluation(
        model,
        X_test,
        y_test,
        X.columns
    )
    


if __name__ == "__main__":
    main() 