#pip install streamlit
import streamlit as st
import requests
import json
def main():
    st.title("MLOps Pipeline - Model Prediction")

    # Add input fields for data
    input_data = st.text_area("Enter input data (in JSON format)")

    # Add a button to submit the data
    if st.button("Predict"):
        # Make an HTTP POST request to the web server
        response = make_prediction(input_data)

        # Display the prediction result
        if response is not None:
            st.success("Prediction: {}".format(response["predictions"]))
def make_prediction(data):
    try:
        # Define the endpoint URL
        url = "http://localhost:8000/predict"

        # Convert the input data to JSON format
        data_json = json.dumps(data)

        # Set the headers for the request
        headers = {"Content-Type": "application/json"}

        # Make the HTTP POST request
        response = requests.post(url, data=data_json, headers=headers)

        # Return the JSON response
        return response.json()

    except requests.exceptions.RequestException as e:
        st.error("Error occurred during prediction: {}".format(e))
if __name__ == "__main__":
    main()
