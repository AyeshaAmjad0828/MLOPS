#pip install streamlit
import streamlit as st
from pymongo import MongoClient
import requests
import json
import subprocess
import os
import joblib

def main():
    st.title("MLOps Pipeline")


    # MongoDB Connection
    st.header("MongoDB Connection")

    # Get MongoDB connection details from the user
    mongo_uri = st.text_input("MongoDB URI", help="Enter the connection URI for your MongoDB database")
    database_name = st.text_input("Database Name", help="Enter the name of the database")
    collection_name = st.text_input("Collection Name", help="Enter the name of the collection")

    # Check if the user provided the necessary details
    if mongo_uri and database_name and collection_name:
        # Connect to the MongoDB database
        try:
            client = MongoClient(mongo_uri)
            db = client[database_name]
            collection = db[collection_name]
            st.success("Connected to MongoDB collection: {}.{}".format(database_name, collection_name))

            st.header("Train Model")
             # Add a button to initiate model training
            if st.button("Train Model"):
                # Execute the train.py script as a subprocess
                subprocess.run(["py", "train.py"])

                st.success("Model trained and saved successfully!")           

            # Add a file uploader for JSON files
                st.header("Generate Predictions")
                
                uploaded_file = st.file_uploader("Upload JSON file", type="json")
                
                # Check if a file was uploaded
                if uploaded_file is not None:
                    file_content = uploaded_file.read().decode("utf-8")      # Read the file content
                    try:
                        input_data = json.loads(file_content)                   # Convert the file content to JSON

                        if st.button("Predict"):                  # Add a button to submit the data
                        # Make an HTTP POST request to the web server
                            response = make_prediction(input_data)

                        # Display the prediction result
                            if response is not None:
                                st.success("Prediction: {}".format(response["predictions"]))

                    except json.JSONDecodeError:
                        st.error("Invalid JSON file. Please upload a valid JSON file.")

        except Exception as e:
            st.error("Error occurred during MongoDB connection: {}".format(str(e)))


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
