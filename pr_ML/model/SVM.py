import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

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

le = LabelEncoder()
y_encoded = le.fit_transform(y)
# X_temp, X_test, y_temp, y_test = train_test_split(X, y_encoded, test_size=0.3, random_state=42)

svm_clf = SVC(kernel='linear', C=50)
svm_clf.fit(X, y_encoded)

joblib.dump(svm_clf, 'SVM.pkl')

y_pred = svm_clf.predict(X)
accuracy = accuracy_score(y_encoded, y_pred)

print(accuracy)

