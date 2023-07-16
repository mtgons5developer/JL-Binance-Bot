# Importing necessary libraries
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Loading the iris dataset
iris = datasets.load_iris()
# print(iris.data)
# print(iris.target)

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.3, random_state=42)

# Creating a k-nearest neighbor classifier with k=3
knn = KNeighborsClassifier(n_neighbors=3)

# Fitting the model with the training data
knn.fit(X_train, y_train)

# Predicting the classes of the testing data
y_pred = knn.predict(X_test)
print(y_pred)

# Calculating the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)

# Printing the accuracy of the model
print('Accuracy: {:.2f}%'.format(accuracy*100))
