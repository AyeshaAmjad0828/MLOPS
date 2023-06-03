# pip install flask
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flaml import AutoML
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder


# Connect to the MongoDB container
client = MongoClient('mongodb://localhost:27017')
db = client['Customers']
collection = db['churtest']
cursor = collection.find()
data = list(cursor)
df_test = pd.DataFrame(data)

# Load the best model from the file or cloud storage
model_path =r'C:\Users\ayesha.amjad\Documents\GitHub\BigDataProject\MLOPS\Project\model\bestmodel.pkl'

with open(model_path, 'rb') as file:
    model = pickle.load(file)

#df_test=pd.read_csv(r'C:\Users\ayesha.amjad\Downloads\test.csv')
df_test[['CreditScore', 'Age', 'Tenure', 'NumOfProducts', 'HasCrCard', 'IsActiveMember']] = df_test[['CreditScore', 'Age', 'Tenure', 'NumOfProducts', 'HasCrCard', 'IsActiveMember']].astype(int)
df_test[['Balance', 'EstimatedSalary']] = df_test[['Balance', 'EstimatedSalary']].astype(float)

le = LabelEncoder()
for column in df_test.columns:
    if df_test[column].dtype == object:
        df_test[column] = le.fit_transform(df_test[column])

#predictions1 = model.predict(df_test)

#automl = AutoML()
#automl.load_model(model)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Perform necessary preprocessing on the data

    # Make predictions using the best model
    predictions = model.predict(df_test)

    # Return the predictions as a JSON response
    return jsonify({'predictions': predictions})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
