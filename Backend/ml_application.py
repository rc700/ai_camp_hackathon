import matplotlib.pyplot as plt
import pandas as pd

from __future__ import print_function

from pandas.plotting import scatter_matrix
from pandas.plotting import andrews_curves

from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn import metrics

# read the data - set index (counter) to the first column
data = pd.read_csv("iris_data.csv", index_col=0)

print(data)
print(data.values)
print(data.shape)
print(data.head())
print(data.tail())
print("* iris types:", data["Species"].unique(), sep="\n")
data.describe()
print(data.groupby('Species').size())

# Visualise


data.hist()
plt.show()

# can see correlation between two sets of features
scatter_matrix(data)
plt.show()

andrews_curves(data, 'Species')
plt.show()

# Split into training + Testing


values = data.values

# gets the feature values - gets all types sliced from structure in range of column 0 to 4
X = values[:,0:4]
# Gets the labels - gets tuple sliced from structure, column 4 only
Y = values[:,4]

# print(values[:5])
# print(X[:5])
# print(Y[:5])
# print(data[:5])

validation_size = 0.20
seed = 7
X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y, test_size=validation_size, random_state=seed)

# print(X_validation[:5])
# print(Y_validation[:5])

# Build the model - svm (students should not use on vm)


classifier = SGDClassifier()
classifier.fit(X_train, Y_train)

# Predict the results

predicted = classifier.predict(X_validation)
print(predicted)

# Get Results


#manual
num_correct = 0
for i in range(0, len(Y_validation)):
    if Y_validation[i] == predicted[i]:
        num_correct = num_correct + 1

print("Accuracy:\n%s" % str(float(num_correct) / float(len(Y_validation))))

# use report
print("Accuracy:\n%s" % metrics.accuracy_score(Y_validation, predicted))
print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(Y_validation, predicted)))
print("Confusion matrix:\n%s" % metrics.confusion_matrix(Y_validation, predicted))