import streamlit as st
import subprocess
import joblib
import os
import requests
import json
from pymongo import MongoClient
import pandas as pd

st.title("MLOps Pipeline")

# Step 1: MongoDB Connection
st.header("Step 1: MongoDB Connection")
mongo_uri = st.text_input("MongoDB URI", help="Enter the connection URI for your MongoDB database")
database_name = st.text_input("Database Name", help="Enter the name of the database")
collection_name = st.text_input("Collection Name", help="Enter the name of the collection")

# test connecting to the MongoDB container
#client = MongoClient('mongodb://localhost:27017')
#db = client['Customers']
#collection = db['ChurnData']
#cursor = collection.find()
#data = list(cursor)
#df = pd.DataFrame(data)

#st.table(df.head(10))

def main():
# Step 2: Model Training
    st.header("Step 2: Model Training")

# Check if the user provided MongoDB connection details
    if mongo_uri and database_name and collection_name:
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]
        cursor = collection.find()
        data = list(cursor)
        df = pd.DataFrame(data)

        st.table(df.head(10))


        # Define the options for the dropdown
        options = ["Classification", "Regression"]
        selected_option = st.selectbox("Select an option", options)
        st.text_input("Target Variable", help="Enter the name of target variable in double quotes")

        if st.button("Train Model"):
        # Step 3: Run train.py script
            subprocess.run(["python", "C:/Users/ayesha.amjad/Documents/GitHub/BigDataProject/MLOPS/Project/automl/train.py", mongo_uri, database_name, collection_name])

            st.success("Model trained and saved successfully!")
            if os.path.exists("C:/Users/ayesha.amjad/Documents/GitHub/BigDataProject/MLOPS/Project/model/roc_auc_curve.png"):
                image = "C:/Users/ayesha.amjad/Documents/GitHub/BigDataProject/MLOPS/Project/model/roc_auc_curve.png"
                st.image(image, caption="ROC-AUC Curve")

# Step 4: Deploy Flask API
    st.header("Step 3: Deploy Trained Model - Flask API")

    if os.path.exists("C:/Users/ayesha.amjad/Documents/GitHub/BigDataProject/MLOPS/Project/model/bestmodel.pkl"):
        if st.button("Deploy API"):
        # Step 4a: Run webserver.py script to deploy Flask API
            subprocess.Popen(["python", "C:/Users/ayesha.amjad/Documents/GitHub/BigDataProject/MLOPS/Project/webserver/server.py"])

            st.success("Flask API deployed successfully!")

        # Step 5: Model Prediction
    st.header("Step 4: Model Prediction")
    uploaded_file = st.file_uploader("Upload JSON file", type="json")

            #check if the file was uploaded
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        try:
            input_data = json.loads(file_content)
                    
            #Button to generate predictions
            if st.button("Generate Predictions"):
                response = make_prediction(input_data)

                #Display prediction results
                if response is not None:
                    st.success("Prediction: {}".format(response["predictions"]))

        except:
            st.error("Invalid JSON file. Please upload a valid JSON file.")
    else:
        st.warning("Please complete Steps 1 and 2 before proceeding to Steps 4 and 5.")


def make_prediction(data):
    try:
        # Define the endpoint URL
        url = "http://localhost:5000/predict"

        # Convert the input data to JSON format
        data_json = json.dumps(data)

        # Set the headers for the request
        headers = {"Content-Type": "application/json"}

        # Make the HTTP POST request
        response = requests.post(url, data=data_json, headers=headers)

        # Return the JSON response
        return response.json()

    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        st.error("Error occurred during prediction: {}".format(e))
if __name__ == "__main__":
    main()
