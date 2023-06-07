import streamlit as st
import subprocess
import joblib
import os
import requests
import time
import json
import webbrowser
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd

st.title("MLOps Pipeline")

# Step 1: MongoDB Connection
st.header("Step 1: MongoDB Connection")
mongo_uri = st.text_input("MongoDB URI", help="Enter the connection URI for your MongoDB database")
database_name = st.text_input("Database Name", help="Enter the name of the database")
collection_name = st.text_input("Collection Name", help="Enter the name of the collection")


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
        df = df.drop('_id', axis=1)

        st.table(df.head(10))

        mongo_params = {
            "Client": mongo_uri,
            "db": database_name,
            "collection": collection_name
        }
        with open("mongo_params.json", 'w') as json_file:
            json.dump(mongo_params, json_file)


        # Define the options for the dropdown
        options = ["Classification", "Regression"]
        selected_option = st.selectbox("Select an option", options)
        target_variable = st.text_input("Target Variable", help="Enter the name of target variable in double quotes")
        split_percent = st.number_input("Test_Train Split", min_value=0, max_value=100, step=5, value=20)
        automl_params = {
            "task": selected_option,
            "target": target_variable,
            "test_size": split_percent
        }
        with open("automl_params.json", 'w') as json_file:
            json.dump(automl_params, json_file)

        if st.button("Train Model"):
        # Step 3: Run train.py script
            subprocess.run(["python", "C:/Users/ayesha.amjad/Documents/GitHub/BigDataProject/MLOPS/Project/automl/train.py", mongo_uri, database_name, collection_name])

            st.success("Model trained and saved successfully!")
        if st.button("Open Grafana Dahboard"):
            #subprocess.run(["python", "C:/Users/ayesha.amjad/Documents/GitHub/BigDataProject/MLOPS/Project/connect.py"])
            open_dashboard
            

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
        st.warning("Please complete Steps 1 and 2 before proceeding to Steps 3 and 4.")

def open_dashboard():
    dasboard_url = "http://localhost:4000/d/d85a1061-f41e-463e-afb6-efd6c20bbd21/performance-dasboard?orgId=1&from=1686135644877&to=1686157244877"
    webbrowser.open_new_tab(dasboard_url)


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
