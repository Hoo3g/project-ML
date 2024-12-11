from flask import Flask, request, jsonify, render_template
import joblib  # Để tải mô hình đã lưu
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

app = Flask(__name__)

# Tải mô hình đã huấn luyện
MODEL_PATH = "model/MLP.pkl"  # Thay bằng đường dẫn đến file mô hình
model = joblib.load(MODEL_PATH)

@app.route('/')
def home():
    return render_template("index.html")  # Tệp HTML của bạn được đặt trong thư mục "templates"

@app.route('/predict', methods=['POST'])
def predict():
    # Lấy dữ liệu từ form
    data = request.form.to_dict()

    # Chuyển đổi dữ liệu vào đúng định dạng DataFrame
    input_data = pd.DataFrame({
        "Gender": [data.get("user-gender")],  # Nam hoặc Nữ
        "Age": [int(data.get("age"))],  # Dữ liệu tuổi (số)
        "Height": [float(data.get("height")) / 100],  # Chuyển chiều cao từ cm sang m
        "Weight": [float(data.get("weight"))],  # Cân nặng (kg)
        
        # Các trường phân loại nhị phân: 'Có' hoặc 'Không'
        "family_history_with_overweight": ["yes" if "SWO" in request.form.getlist("prefer") else "no"], 
        "FAVC": ["yes" if "FAVC" in request.form.getlist("prefer") else "no"], 
        "SMOKE": ["yes" if "SMOKE" in request.form.getlist("prefer") else "no"],
        "SCC": ["yes" if "SCC" in request.form.getlist("prefer") else "no"],

        # FCVC, NCP, CAEC là các trường phân loại có giá trị rời rạc
        "FCVC": [data.get("FCVC")],  # 'Không bao giờ', 'Thỉnh thoảng', 'Luôn luôn'
        "NCP": [data.get("NCP")],  # 'Khoảng 1-2', '3', 'Nhiều hơn 3'
        "CAEC": [data.get("CAEC")],  # 'Không', 'Thỉnh thoảng', 'Thường xuyên', 'Luôn luôn'

        # CH2O: Sử dụng giá trị số thực cho lượng nước tiêu thụ
        "CH2O": [data.get("water")],  # 'Ít hơn 1 lít', '1-2 lít', 'Nhiều hơn 2 lít'

        # FAF: Hoạt động thể chất
        "FAF": [data.get("FAF")],  # '0', '1-2 ngày', '2-4 ngày', 'Nhiều hơn'

        # TUE: Thời gian sử dụng thiết bị điện tử
        "TUE": [data.get("TUE")],  # '0-2 giờ', '3-5 giờ', 'Nhiều hơn 5 giờ'

        # CALC: Uống rượu
        "CALC": [data.get("CALC")],  # 'Không', 'Thỉnh thoảng', 'Thường xuyên', 'Luôn luôn'

        # MTRANS: Phương tiện di chuyển
        "MTRANS": [data.get("MTRANS")]  # 'Ôtô', 'Xe máy', 'Xe đạp', 'Phương tiện công cộng', 'Đi bộ'
    })

    continuous_columns = ['Age', 'Height', 'Weight', 'NCP', 'CH2O', 'FAF', 'TUE', 'FCVC']
    print(data)
  # Khởi tạo bộ chuẩn hóa
    scaler = StandardScaler()

    # Chuẩn hóa các trường liên tục
    input_data[continuous_columns] = scaler.fit_transform(input_data[continuous_columns])
    X = input_data
    X = pd.get_dummies(X, columns=['Gender', 'CAEC', 'CALC', 'MTRANS'])
    X = X.replace({'yes': 1, 'no': 0})
    X = X.replace({True: 1, False: 0})
    # print(X)
    # pca = PCA(n_components=14)
    # X_pca = pca.fit_transform(X)

    # Tiến hành dự đoán và trả về kết quả (giả sử có mô hình đã huấn luyện)
    prediction = model.predict(X)  # model là mô hình đã huấn luyện trước đó
    result = prediction[0]
    print(result)
    # Trả kết quả dự đoán về giao diện người dùng
     # Trả kết quả dưới dạng JSON
    return jsonify({"result": f"Ước tính mức độ béo phì: {result}"})
    
if __name__ == '__main__':
    app.run(debug=True)
