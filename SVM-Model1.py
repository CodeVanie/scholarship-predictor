import pickle

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler, LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Set pandas display options
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Load dataset
df = pd.read_csv('scholarsdata.csv')

# Define ordinal encoding for selected categorical columns
ordinalnums = {"YearLevel": {"4th year": 4, "3rd year": 3, "2nd year": 2, "1st year": 1},
               "FatherEduc": {"Graduate School": 4, "Undergraduate": 3, "Secondary education": 2, "Primary education": 1, "None": 0},
               "MotherEduc": {"Graduate school": 4, "Undergraduate": 3, "Secondary education": 2, "Primary education": 1, "None": 0},
               "FamIncome": {"More than 55000": 5, "40000 - 55000": 4, "25000 - 40000": 3, "12000 - 25000": 2, "Less than 12000": 1},
               "TravelTime": {"More than 1 hour": 4, "30 minutes to 1 hour": 3, "15 to 30 minutes": 2, "Less than 15 minutes": 1},
               "StudyHours": {"More than 10 hours": 4, "5 - 10 hours": 3, "2 - 5 hours": 2, "Less than 2 hours": 1},
               "ScholarshipType": {"President's lister": 5, "VPAA lister": 4, "Dean's lister": 3, "With Highest Honors": 2, "With High Honors": 1}}

# Replace categorical values with ordinal encoding using the defined mapping
ord_df = df.replace(ordinalnums)

# Encode target variable using LabelEncoder
ord_df[['MaintainedScholarship']] = ord_df[['MaintainedScholarship']].apply(LabelEncoder().fit_transform)

# Split dataset into features (X) and target (y)
X = ord_df.drop(['MaintainedScholarship'], axis=1)
y = ord_df['MaintainedScholarship']

# Create OneHotEncoder object and fit_transform on the categorical columns
ohe = OneHotEncoder(sparse=False)
cat_cols = X.select_dtypes(include='object').columns
ohe_df = pd.DataFrame(ohe.fit_transform(df[cat_cols]))
ohe_df.columns = ohe.get_feature_names_out(cat_cols)

# Drop the original categorical columns and concatenate the one-hot encoded columns
X = X.drop(cat_cols, axis=1)
X = pd.concat([X, ohe_df], axis=1)


# Normalization
scaler = StandardScaler()
X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# SMOTE for balancing the classes
sm = SMOTE(random_state=42)
X_train, y_train = sm.fit_resample(X_train, y_train)

# Train an SVM model
clf = SVC(kernel='linear')
clf.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = clf.predict(X_test)
print(X_test)
print("Test Predict: ", clf.predict([[22, 4, 1, 2, 2, 4, 4, 3, 3, 1, 1, 1, 4, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1]]))

# Evaluate the performance of the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Confusion matrix and classification report
cm = confusion_matrix(y_test, y_pred)
print("Confusion matrix:\n", cm)
print("Classification report:\n", classification_report(y_test, y_pred))

pickle.dump(clf, open("model.pkl", "wb"))