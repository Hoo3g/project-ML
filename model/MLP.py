import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

import joblib

data = pd.read_csv('D:\\VS_Code\\Python\\machine_learning\\project_ML\\Machine-Learning\\Pre_treatment\\ObesityDataSet_raw_and_data_sinthetic.csv')
continuous_columns = ['Age', 'Height', 'Weight', 'NCP', 'CH2O', 'FAF', 'TUE', 'FCVC']

# Khởi tạo bộ chuẩn hóa
scaler = StandardScaler()

# Chuẩn hóa các trường liên tục
data[continuous_columns] = scaler.fit_transform(data[continuous_columns])
X = data.iloc[:, :-1]
y = data.iloc[:, -1]
X = pd.get_dummies(X, columns=['Gender', 'CAEC', 'CALC', 'MTRANS'])
X = X.replace({'yes': 1, 'no': 0})
X = X.replace({True: 1, False: 0})
pca = PCA(n_components=16)
X_pca = pca.fit_transform(X)


X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.2, random_state=42)

mlp = MLPClassifier(hidden_layer_sizes=(100,), max_iter=300, random_state=42)
mlp.fit(X_train, y_train)

joblib.dump(mlp, 'MLP.pkl')

y_pred = mlp.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
