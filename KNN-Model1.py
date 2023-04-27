import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler, LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.neighbors import KNeighborsClassifier
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

# perform KNN classification using cross-validation
knn = KNeighborsClassifier()
scores = cross_val_score(knn, X_train, y_train, cv=10)
print("Cross-validation scores: {}".format(scores))
print("Average score: {}".format(sum(scores)/len(scores)))

# Fit the KNN model on the training data
knn.fit(X_train, y_train)

# Evaluate the performance of the KNN model on the testing data
y_pred = knn.predict(X_test)

# Calculate the probabilities of each class for each row in the testing set
y_proba = knn.predict_proba(X_test)

#loop through each row and calculate the accuracy of prediction
for i in range(len(X_test)):
    # get the predicted class and probability estimates for each class
    predicted_class = y_pred[i]
    class_probabilities = y_proba[i]

    # calculate the accuracy of prediction per row
    row_accuracy = round(class_probabilities[predicted_class] * 100, 2)

    # print the results
    print("Row {} - Predicted class: {}, Likeness percentage: {}%".format(i + 1, predicted_class, row_accuracy))
    
# Make predictions on the testing set
# custom test input (maintained)
custom_test_input = [[4, 1, 2, 2, 4, 3, 5, 1, 4, 1, 0, 0, 1, 0, 1]]

# Make predictions and probability estimates on the custom test input
custom_y_pred = knn.predict(custom_test_input)
custom_y_proba = knn.predict_proba(custom_test_input)

# Calculate the accuracy of prediction per row
custom_row_accuracy = round(custom_y_proba[0][custom_y_pred[0]] * 100, 2)

# Print the results
print("Maintained - Predicted class: {}, Likeness percentage: {}%".format(custom_y_pred[0], custom_row_accuracy))

# custom test input (maintained)
custom_test_input = [[1, 4, 3, 2, 4, 1, 1, 5, 1, 1, 0, 0, 0, 1, 0]]

# Make predictions and probability estimates on the custom test input
custom_y_pred = knn.predict(custom_test_input)
custom_y_proba = knn.predict_proba(custom_test_input)

# Calculate the accuracy of prediction per row
custom_row_accuracy = round(custom_y_proba[0][custom_y_pred[0]] * 100, 2)

# Print the results
print("Not Maintained - Predicted class: {}, Likeness percentage: {}%".format(custom_y_pred[0], custom_row_accuracy))

# Confusion matrix and classification report
cm = confusion_matrix(y_test, y_pred)
print("Confusion matrix:\n", cm)
print("Classification report:\n", classification_report(y_test, y_pred))

print("Predictions: ", y_pred)
print("True Labels: ", y_test)

pickle.dump(knn, open("model.pkl", "wb"))