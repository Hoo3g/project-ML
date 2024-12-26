from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

app = Flask(__name__)

MODEL_PATH = "pr_ML/model/SVM.pkl"
COLUMNS_PATH = "pr_ML/model/columns.pkl"

model = joblib.load(MODEL_PATH)
columns = joblib.load(COLUMNS_PATH)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])

def predict():
    data = request.form.to_dict()

    input_data = pd.DataFrame({
        "Gender": [data.get("user-gender")],  
        "Age": [int(data.get("age"))],  
        "Height": [float(data.get("height")) / 100], 
        "Weight": [float(data.get("weight"))], 
        
        "family_history_with_overweight": ["yes" if "SWO" in request.form.getlist("prefer") else "no"], 
        "FAVC": ["yes" if "FAVC" in request.form.getlist("prefer") else "no"], 
        "SMOKE": ["yes" if "SMOKE" in request.form.getlist("prefer") else "no"],
        "SCC": ["yes" if "SCC" in request.form.getlist("prefer") else "no"],

        "FCVC": [data.get("FCVC")],
        "NCP": [data.get("NCP")],
        "CAEC": [data.get("CAEC")], 

        "CH2O": [data.get("water")],  
        #Hoạt động thể chất
        "FAF": [data.get("FAF")],

        #Thời gian sử dụng thiết bị điện tử
        "TUE": [data.get("TUE")],

        #Uống rượu
        "CALC": [data.get("CALC")],  

        #Phương tiện di chuyển
        "MTRANS": [data.get("MTRANS")]
    })

    print(data)
  
    X = input_data
    X = pd.get_dummies(X, columns=['Gender', 'CAEC', 'CALC', 'MTRANS'])
    X = X.replace({'yes': 1, 'no': 0})
    X = X.replace({True: 1, False: 0})

    X = X.reindex(columns=columns, fill_value=0)
    print(X)

    result_mapping = {
        0: "Thiếu cân",
        1: "Cân nặng bình thường",
        2: "Béo phì mức I",
        3: "Béo phì mức II",
        4: "Béo phì mức III",
        5: "Thừa cân mức I",
        6: "Thừa cân mức II"
    }
    
    prediction = model.predict(X)
    result = prediction[0]

    result = result_mapping.get(result, "Unknown")
    
    return jsonify({"result": f"{result}"})
    
import os
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
