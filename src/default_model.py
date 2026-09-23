from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

def get_logistic_regression_feature_importance(model):
    preprocessor = model.named_steps["preprocessor"]
    classifier = model.named_steps["classifier"]

    feature_names = preprocessor.get_feature_names_out()
    coefficients = classifier.coef_[0]

    importance_df = pd.DataFrame(
        {
            "feature": feature_names,
            "coefficient": coefficients,
            "abs_coefficient": abs(coefficients),
        }
    )

    importance_df = importance_df.sort_values("abs_coefficient", ascending=False)

    return importance_df
def train_default_random_forest(model_df):
    feature_columns = [
        "age_borrower",
        "gender_borrower",
        "marital_status_borrower",
        "education_level_borrower",
        "employment_type_borrower",
        "region_borrower",
        "sector_borrower",
        "monthly_income_npr_borrower",
        "credit_score_borrower",
        "dependents",
        "home_owner",
        "product_type",
        "loan_amount_npr",
        "interest_rate_pct",
        "term_months",
        "collateral_type",
    ]

    X = model_df[feature_columns].copy()
    y = model_df["defaulted_flag"].copy()

    categorical_features = [
        "gender_borrower",
        "marital_status_borrower",
        "education_level_borrower",
        "employment_type_borrower",
        "region_borrower",
        "sector_borrower",
        "home_owner",
        "product_type",
        "collateral_type",
    ]

    numeric_features = [
        "age_borrower",
        "monthly_income_npr_borrower",
        "credit_score_borrower",
        "dependents",
        "loan_amount_npr",
        "interest_rate_pct",
        "term_months",
    ]

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=300,
                    max_depth=10,
                    min_samples_split=10,
                    min_samples_leaf=5,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42,
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1_score": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
    }

    return model, metrics

def get_high_risk_predictions(prediction_df, top_n=20):
    high_risk_df = prediction_df.sort_values(
        "predicted_probability",
        ascending=False,
    ).head(top_n)

    return high_risk_df

def add_risk_band(prediction_df):
    df = prediction_df.copy()

    def classify_risk(prob):
        if prob >= 0.50:
            return "High"
        elif prob >= 0.20:
            return "Medium"
        else:
            return "Low"

    df["risk_band"] = df["predicted_probability"].apply(classify_risk)
    return df

def train_default_logistic_regression(model_df):
    feature_columns = [
        "age_borrower",
        "gender_borrower",
        "marital_status_borrower",
        "education_level_borrower",
        "employment_type_borrower",
        "region_borrower",
        "sector_borrower",
        "monthly_income_npr_borrower",
        "credit_score_borrower",
        "dependents",
        "home_owner",
        "product_type",
        "loan_amount_npr",
        "interest_rate_pct",
        "term_months",
        "collateral_type",
    ]

    X = model_df[feature_columns].copy()
    y = model_df["defaulted_flag"].copy()

    categorical_features = [
        "gender_borrower",
        "marital_status_borrower",
        "education_level_borrower",
        "employment_type_borrower",
        "region_borrower",
        "sector_borrower",
        "home_owner",
        "product_type",
        "collateral_type",
    ]

    numeric_features = [
        "age_borrower",
        "monthly_income_npr_borrower",
        "credit_score_borrower",
        "dependents",
        "loan_amount_npr",
        "interest_rate_pct",
        "term_months",
    ]

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42,
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1_score": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
    }

    prediction_df = X_test.copy()
    prediction_df["actual_default"] = y_test.values
    prediction_df["predicted_default"] = y_pred
    prediction_df["predicted_probability"] = y_proba

    return model, metrics, prediction_df