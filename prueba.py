from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

# Cargar dataset ejemplo Iris
iris = load_iris()
X = iris.data
y = iris.target
feature_names = iris.feature_names
class_names = iris.target_names

# Entrenar un árbol de decisión
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

# Visualizar el árbol
plt.figure(figsize=(15,10))  # tamaño de figura
plot_tree(model, feature_names=feature_names, class_names=class_names, filled=True, rounded=True)
plt.show()
