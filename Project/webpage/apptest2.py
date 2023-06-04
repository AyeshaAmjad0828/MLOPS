import streamlit as st
import subprocess
import joblib
import os
import requests
import json

st.title("MLOps Pipeline")

# Step 1: MongoDB Connection
st.header("Step 1: MongoDB Connection")
mongo_uri = st.text_input("MongoDB URI")
database_name = st.text_input("Database Name")
collection_name = st.text_input("Collection Name")



def main():
# Step 2: Model Training
    st.header("Step 2: Model Training")

# Check if the user provided MongoDB connection details
    if mongo_uri and database_name and collection_name:
        if st.button("Train Model"):
        # Step 3: Run train.py script
            subprocess.run(["python", "C:/Users/ayesha.amjad/Documents/GitHub/BigDataProject/MLOPS/Project/automl/train.py", mongo_uri, database_name, collection_name])

            st.success("Model trained and saved successfully!")

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
