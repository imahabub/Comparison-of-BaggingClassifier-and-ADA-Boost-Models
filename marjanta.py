# -*- coding: utf-8 -*-
"""Marjanta.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mlSvxAlnoJ3QkddpBOkgBwhxUk0lLhCo
"""

#Importing python library
import pandas as pn
# Import basic library
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
# Dataset pre-processing
from sklearn.preprocessing import StandardScaler, LabelEncoder
# Splitting dataset
from sklearn.model_selection import train_test_split
#Bagging classifier model
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier
#ADABoost classifier model
from sklearn.ensemble import AdaBoostClassifier
#Evaluating the relevant parameters
from sklearn.metrics import accuracy_score, log_loss, classification_report, confusion_matrix

Marjanta= pn.read_csv ("/content/MARJANTA_DATA_CW3 (S).csv", encoding="latin-1") #CSV file import
Marjanta.head(3)

#dataset information
Marjanta.info()

#Missing value identification
Marjanta.isnull().sum()

duplicate_values_dataset = Marjanta[Marjanta.duplicated()] #Identification of duplicate values
print("Duplicate values:") # Priniting duplicate values
duplicate_values_dataset

Marjanta.fillna(method ='bfill', inplace=True) #Misisng values fillup

"""Exploratory Data Analysis"""

fig1 = px.histogram(Marjanta, x='Continent', color='Satisfied', barmode='group',
                   title='Continentwise passenger satisfaction',
                   labels={'Continent': 'Continent', 'count': 'Number of Passengers'})
fig1.update_layout(xaxis_title='Continent', yaxis_title='Count', bargap=0.3)
fig1.show()

Marjanta.describe() #description of the data set

qw1=sns.countplot(x ='Online boarding', hue= 'Satisfied',data = Marjanta, palette='Reds')  #ratings of Online Boarding
for label in qw1.containers:
    qw1.bar_label(label)
plt.title('Rating of Online Boarding based on satisfaction')
plt.xlabel('Online boarding Rating')
plt.ylabel('Count')
plt.legend(title='Satisfied')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

gh1=sns.countplot(x ='Satisfied', hue= 'Checkin service',data = Marjanta, palette='Blues')  #Checkin sedrvices based on customer satisfaction
for label in gh1.containers:
    gh1.bar_label(label)
plt.title('Checkin services ratings based on passenger satisfaction')
plt.xlabel('Rating of checkin services')
plt.ylabel('Count')
plt.legend(title='Satisfied')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

#Data pre-processing
from sklearn.preprocessing import StandardScaler, LabelEncoder
label_encoder_dataset1 = {}
category_column_details1 = ['Gender', 'Satisfied', 'Age Band', 'Type of Travel', 'Class', 'Destination', 'Continent']
for column in category_column_details1:
    label_encoder_detail1 = LabelEncoder()
    Marjanta[column] = label_encoder_detail1.fit_transform(Marjanta[column])
    label_encoder_dataset1[column] = label_encoder_detail1

#Heatmap creation
plt.figure(figsize=(10, 10))
sns.heatmap(Marjanta.corr(), annot=True, cmap='spring')
plt.show()

#Deleting unnecessary data
X = Marjanta.drop(['Ref', 'id', 'Satisfied', 'Age'], axis=1)
#target column
y = Marjanta['Satisfied']
#Data set split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=42)

"""ADABoost Classifier"""

#ADABoost classifier model
ADABoost1 = AdaBoostClassifier(n_estimators=100,
                         learning_rate=0.0015)
ADABoost1.fit(X_train, y_train)

y_predict_ADABoost1 = ADABoost1.predict(X_test)

#Accuracy score
accuracy1 = accuracy_score(y_test, y_predict_ADABoost1)
print("Accuracy of the model:", accuracy1)

print("Classification report of ADABoost:")
print(classification_report(y_test, y_predict_ADABoost1))

#Loss function calculation
ADABoost_loss= log_loss(y_test, y_predict_ADABoost1)
print(f'Log Loss value of ADABoost model: {ADABoost_loss:.3f}')

#Confusion matrix
ADABoost_conf_matrix = confusion_matrix(y_test, y_predict_ADABoost1)
plt.figure(figsize=(3, 3))
sns.heatmap(ADABoost_conf_matrix, annot=True,
            fmt='g', cmap= 'plasma')
plt.xlabel('Prediction value-ADABoost model',fontsize=6)
plt.ylabel('Actual value-ADABoost model',fontsize=6)
plt.title('Confusion Matrix-ADABoost classifier model',fontsize=8)
plt.show()

"""Bagging Classifier Model"""

#Bagging Classifier
base_model1 = DecisionTreeClassifier()
bagging_model1 = BaggingClassifier(base_estimator=base_model1, n_estimators=10)
classifiers = bagging_model1.fit(X_train, y_train)

#Results prediction
y_pred = classifiers.predict(X_test)

#Accuracy calculation
accuracy2 = accuracy_score(y_test, y_pred)
print("Accuracy- Bagging Classifier:", accuracy2)

#Classification report
print("Classification report-Bagging classifier model:")
print(classification_report(y_test, y_pred))

#Loss function calculation
Bagging_loss= log_loss(y_test, y_pred)
print(f'Log Loss value-Bagging classifier model: {Bagging_loss:.3f}')

#Confusion matrix
bag_conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(3, 3))
sns.heatmap(bag_conf_matrix, annot=True,
            fmt='g', cmap= 'plasma')
plt.xlabel('Prediction value-Bagging model',fontsize=8)
plt.ylabel('Actual value-Bagging model',fontsize=8)
plt.title('Confusion Matrix-Bagging classifier model',fontsize=8)
plt.show()