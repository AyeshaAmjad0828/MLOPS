#pip install streamlit
import streamlit as st
import requests
import json

def main():
    st.title("MLOps Pipeline - Model Prediction")

    # Add a file uploader for JSON files
    uploaded_file = st.file_uploader("Upload JSON file", type="json")

    # Check if a file was uploaded
    if uploaded_file is not None:
        # Read the file content
        file_content = uploaded_file.read().decode("utf-8")
        try:
            # Convert the file content to JSON
            input_data = json.loads(file_content)

            # Add a button to submit the data
            if st.button("Predict"):
                # Make an HTTP POST request to the web server
                response = make_prediction(input_data)

                # Display the prediction result
                if response is not None:
                    st.success("Prediction: {}".format(response["predictions"]))

        except json.JSONDecodeError:
            st.error("Invalid JSON file. Please upload a valid JSON file.")


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
