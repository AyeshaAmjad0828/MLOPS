import streamlit as st
import subprocess
import joblib
import os
import requests

st.title("MLOps Pipeline")
# Step 1: MongoDB Connection
st.header("Step 1: MongoDB Connection")
mongo_uri = st.text_input("MongoDB URI")
database_name = st.text_input("Database Name")
collection_name = st.text_input("Collection Name")

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
        subprocess.run(["python", "C:/Users/ayesha.amjad/Documents/GitHub/BigDataProject/MLOPS/Project/webserver/server.py"])

        st.success("Flask API deployed successfully!")

        # Step 5: Model Prediction
        st.header("Step 4: Model Prediction")

        uploaded_file = st.file_uploader("Upload JSON file", type="json")

        if uploaded_file is not None:
            if st.button("Generate Predictions"):
                # Step 6: Make prediction using the deployed API
                file_content = uploaded_file.read().decode("utf-8")

                try:
                    # Step 6a: Send HTTP POST request to the deployed API
                    response = requests.post("http://localhost:5000/predict", json=file_content)

                    if response.status_code == 200:
                        predictions = response.json()
                        st.success("Predictions: {}".format(predictions))
                    else:
                        st.error("Failed to get predictions. Please try again.")

                except Exception as e:
                    st.error("Error occurred during prediction: {}".format(str(e)))
else:
    st.warning("Please complete Steps 1 and 2 before proceeding to Steps 4 and 5.")
