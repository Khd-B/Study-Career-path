import streamlit as st
import requests

# Load Hugging Face API token from Streamlit secrets
hf_token = st.secrets["HF_TOKEN"]

# Hugging Face API URL for GPT2 model (you can change this if you want to use another model)
api_url = "https://api-inference.huggingface.co/models/openai/gpt2"  # You can replace this with another model if needed

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
hobbies = st.text_area("Hobbies")
skills = st.text_area("Skills")
languages = st.text_area("Languages")

# Create a button to get recommendations
if st.button("Get Career Recommendations"):
    # Preprocess input and format it into a structured prompt
    input_data = f"""
    Suggest a career and study path for someone with the following profile:
    - Age: {age}
    - Gender: {gender}
    - Country: {country}
    - Qualification: {qualification}
    - Academic Interest: {academic_interest}
    - Career Aspiration: {aspirations}
    - Hobbies: {hobbies}
    - Skills: {skills}
    - Languages: {languages}
    """

    # Send the request to the Hugging Face API
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json={"inputs": input_data}
        )

        # Check the response from the API
        if response.status_code == 200:
            recommendations = response.json()  # Assuming the API returns recommendations in a readable format
            st.write("### Career Recommendations")
            st.write(recommendations['generated_text'])  # Display the generated text from the model
        else:
            # Log the error if something went wrong with the API call
            st.error(f"Failed to get recommendations from the model. Status code: {response.status_code}")
            st.error(f"Response: {response.text}")  # Log the full response text for debugging

    except Exception as e:
        # Handle exceptions and log the error
        st.error(f"An error occurred while making the API request: {e}")
