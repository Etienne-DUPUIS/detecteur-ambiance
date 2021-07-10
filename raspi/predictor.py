from sklearn.neighbors import KNeighborsClassifier
import numpy as np


def knn_predict(samples, dataset, target):
    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(dataset, target)
    return neigh.predict(samples)


X = np.array([[0, 2, 5],
              [1, 5, 3],
              [2, 2, 4],
              [3, 5, 2]])
y = [0, 1, 5, 2]

print(knn_predict([[2, 5 ,3], [2,2,4]], X, y))