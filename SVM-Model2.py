import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler, LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

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

# Perform feature selection using SelectKBest with f_classif as the scoring function
selector = SelectKBest(score_func=f_classif, k=15)
X_selected = selector.fit_transform(X, y)

# Plot the scores of the features
scores = selector.scores_
plt.bar(range(X.shape[1]), scores)
plt.xticks(range(X.shape[1]), X.columns, rotation=90)
plt.xlabel("Features")
plt.ylabel("F-value")
plt.show()

# Print the top 15 features
scores = selector.scores_
feature_scores = pd.DataFrame({'Feature': X.columns, 'Score': scores})
feature_scores = feature_scores.sort_values('Score', ascending=False)
top_15_features = feature_scores.head(15)['Feature']
print("Top 15 features:")
for feature in top_15_features:
    print(feature)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)

# SMOTE for balancing the classes
sm = SMOTE(random_state=42)
X_train, y_train = sm.fit_resample(X_train, y_train)

# Define the SVM classifier with 'rbf' kernel and regularization parameter 'C'
svm = SVC(kernel='rbf', C=1)

# Set up a parameter grid to tune the hyperparameters using GridSearchCV
param_grid = {'gamma': [0.1, 1, 10], 'kernel': ['linear', 'rbf', 'poly'], 'C': [0.1, 1, 10]}

# Perform hyperparameter tuning using GridSearchCV and 5-fold cross-validation
grid_search = GridSearchCV(svm, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Print the best hyperparameters and the corresponding accuracy score
print("Best hyperparameters: ", grid_search.best_params_)
print("Accuracy score: ", grid_search.best_score_)

# Evaluate the performance of the SVM classifier on the test set
clf = grid_search.best_estimator_
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)
print("Test set accuracy: ", accuracy)


# Make predictions on the testing set
print(X_test)
y_pred = clf.predict(X_test)
print(y_pred)
y_pred2 = clf.predict([[4, 1, 2, 2, 4, 3, 5, 1, 4, 1, 0, 0, 1, 0, 1]]) #Maintained
y_pred3 = clf.predict([[4, 4, 4, 3, 4, 3, 2, 4, 4, 0, 1, 0, 1, 1, 0]]) #Not maintained
print(y_pred2)
print(y_pred3)

# Confusion matrix and classification report
cm = confusion_matrix(y_test, y_pred)
print("Confusion matrix:\n", cm)
print("Classification report:\n", classification_report(y_test, y_pred))

pickle.dump(clf, open("model.pkl", "wb"))