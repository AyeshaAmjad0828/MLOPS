# pip install flask
from flask import Flask, request, jsonify
from flaml import AutoML
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder



# Load the best model from the file or cloud storage
model_path =r'C:\Users\ayesha.amjad\Documents\GitHub\BigDataProject\MLOPS\Project\model\bestmodel.pkl'

with open(model_path, 'rb') as file:
    model = pickle.load(file)


#df_test=pd.read_csv(r'C:\Users\ayesha.amjad\Downloads\test.csv')
#preprocessing
# df_test[['CreditScore', 'Age', 'Tenure', 'NumOfProducts', 'HasCrCard', 'IsActiveMember']] = df_test[['CreditScore', 'Age', 'Tenure', 'NumOfProducts', 'HasCrCard', 'IsActiveMember']].astype(int)
# df_test[['Balance', 'EstimatedSalary']] = df_test[['Balance', 'EstimatedSalary']].astype(float)

# le = LabelEncoder()
# for column in df_test.columns:
#     if df_test[column].dtype == object:
#         df_test[column] = le.fit_transform(df_test[column])

#predictions1 = model.predict(df_test)
#automl = AutoML()
#automl.load_model(model)

#Test API
#app = Flask(__name__)
#@app.route("/")
#def hello():
#    return "Welcome to machine learning model APIs!"
#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=5000)




app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    data_test = pd.DataFrame(data)

    # Perform necessary preprocessing on the data
    constant_columns = [col for col in data_test.columns if data_test[col].nunique() == 1]
    data_test = data_test.drop(constant_columns, axis=1)


    #identify and drop sequential columns
    sequential_columns = []
    for col in data_test.columns:
        if data_test[col].dtype in [np.int64, np.int32, np.float64]:
            differences = np.diff(data_test[col])
            if np.all(differences == differences[0]):
                sequential_columns.append(col)

    data_test = data_test.drop(sequential_columns, axis=1)

    data_test = data_test.replace(r'^\s*$', pd.NA, regex=True)
    numeric_cols = data_test.select_dtypes(include=np.number).columns
    categorical_cols = data_test.select_dtypes(include=np.object).columns
    data_test[numeric_cols] = data_test[numeric_cols].fillna(data_test[numeric_cols].mean())
    data_test[categorical_cols] = data_test[categorical_cols].fillna(data_test[categorical_cols].mode().iloc[0])

    le = LabelEncoder()
    for column in data_test.columns:
        if data_test[column].dtype == object:
            data_test[column] = le.fit_transform(data_test[column])

   
    # Make predictions using the best model
    predictions = model.predict(data_test)
    df_pred = pd.DataFrame(predictions)
    json_pred = df_pred.to_json(orient='records')

    # Return the predictions as a JSON response
    return jsonify({'predictions': json_pred})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
