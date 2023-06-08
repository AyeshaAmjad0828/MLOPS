# pip install flask
from flask import Flask, request, jsonify
import pickle
import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder



# Load the best model from the file or cloud storage
model_path =r'C:\Users\ayesha.amjad\Documents\GitHub\BigDataProject\MLOPS\Project\model\bestmodel.pkl'

with open(model_path, 'rb') as file:
    model = pickle.load(file)


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

# with open("C:/Users/ayesha.amjad/Documents/GitHub/BigDataProject/MLOPS/Project/churntest.json", "r") as json_file:
#     churn_test = json.load(json_file)



app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    data_test = pd.DataFrame(data)
    #Dropping _id column
    data_test['_id'] = data_test['_id'].astype(str)
    data_test = data_test.drop('_id', axis=1)

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
    df_pred = pd.DataFrame(predictions, columns=["Predicted_Y"])

    json_pred = df_pred.to_json(orient='records')


    # Return the predictions as a JSON response
    return jsonify({'predictions': json_pred})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
