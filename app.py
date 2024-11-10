import streamlit as st
import requests

# Load Hugging Face API token from Streamlit secrets
hf_token = st.secrets["huggingface_token"]

# Hugging Face API URL for GPT2 model (or other model if you change it)
api_url = "https://api-inference.huggingface.co/models/openai/gpt2"  # Update this URL if needed

# Define headers for the API request
headers = {
    "Authorization": f"Bearer {hf_token}"
}

# Title of the app
st.title("Your Study & Career Path Buddy")

# Collect user inputs from the app
age = st.text_input("Age")
gender = st.text_input("Gender")
country = st.text_input("Country")
qualification = st.text_input("Highest Qualification")
academic_interest = st.radio("Academic Interest", ["STEM", "Humanities", "Arts", "Business"])
aspirations = st.selectbox("Do you want to work locally or internationally?", ["Locally", "Internationally", "Both"])

# Create a button to get recommendations
if st.button("Get Career Recommendations"):
    # Prepare the user data to send to the Hugging Face model
    input_data = f"Age: {age}, Gender: {gender}, Country: {country}, Qualification: {qualification}, Academic Interest: {academic_interest}, Aspirations: {aspirations}"

    # Send the request to the Hugging Face API
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json={"inputs": input_data}
        )

        # Check the response from the API
        if response.status_code == 200:
            recommendations = response.json()  # Assuming the API returns recommendations
            st.write("### Career Recommendations")
            st.write(recommendations)
        else:
            # Log the error if something went wrong with the API call
            st.error(f"Failed to get recommendations from the model. Status code: {response.status_code}")
            st.error(f"Response: {response.text}")  # Log the full response text for debugging

    except Exception as e:
        # Handle exceptions and log the error
        st.error(f"An error occurred while making the API request: {e}")
