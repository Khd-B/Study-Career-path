import streamlit as st
from transformers import pipeline

# Load the Hugging Face pipeline with a GPT model for text generation
generator = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")

# Define a function to generate career advice
def get_career_recommendations(age, gender, country, qualification, academic_interest, career_aspiration, hobbies, skills, languages):
    prompt = f"""
    You are a career and education advisor. Suggest career and study paths for someone with the following profile:
    
    Age: {age}
    Gender: {gender}
    Country: {country}
    Highest Qualification: {qualification}
    Academic Interest: {academic_interest}
    Career Aspiration: {career_aspiration}
    Hobbies: {hobbies}
    Skills: {skills}
    Languages: {languages}

    Please provide a clear and concise response with career or study recommendations, educational background, and potential career growth.
    """

    # Use the Hugging Face model to generate recommendations
    result = generator(prompt, max_length=250, num_return_sequences=1, temperature=0.7)
    return result[0]['generated_text']

# Streamlit interface
st.title("Career and Study Path Recommendations")

# User inputs
age = st.number_input("Age", min_value=18, max_value=100)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
country = st.text_input("Country")
qualification = st.text_input("Highest Qualification")
academic_interest = st.text_input("Academic Interest")
career_aspiration = st.text_input("Career Aspiration")
hobbies = st.text_input("Hobbies")
skills = st.text_input("Skills")
languages = st.text_input("Languages")

# Button to get recommendations
if st.button("Get Recommendations"):
    result = get_career_recommendations(age, gender, country, qualification, academic_interest, career_aspiration, hobbies, skills, languages)
    st.subheader("Career and Study Path Recommendations")
    st.write(result)
