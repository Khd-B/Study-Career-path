import streamlit as st
from transformers import pipeline

# Load the Hugging Face pipeline for text generation (GPT-2 model)
generator = pipeline("text-generation", model="gpt2")

# Title of the app
st.title("Your Study & Career Path Buddy")

# Collect user inputs
age = st.text_input("Age")
gender = st.text_input("Gender")
country = st.text_input("Country")
qualification = st.text_input("Highest Qualification")
academic_interest = st.radio("Academic Interest", ["STEM", "Humanities", "Arts", "Business", "Other"])
aspirations = st.selectbox("Do you want to work locally or internationally?", ["Locally", "Internationally", "Both"])
hobbies = st.text_area("Hobbies (e.g., music, sports, reading)")
skills = st.text_area("Skills (e.g., programming, communication, leadership)")
languages = st.text_area("Languages you speak")

# Combine the user's input into a structured prompt for the model
if st.button("Get Career Recommendations"):
    # Create a more structured and clear prompt for the model
    prompt = f"""
    You are a career and education advisor. Suggest career and study paths for someone with the following profile:
    - Age: {age}
    - Gender: {gender}
    - Country: {country}
    - Highest Qualification: {qualification}
    - Academic Interest: {academic_interest}
    - Career Aspiration: {aspirations}
    - Hobbies: {hobbies}
    - Skills: {skills}
    - Languages: {languages}

    Provide a clear and concise response. Recommend suitable career or study paths, the required educational background, and potential career growth.
    Do not include personal information or irrelevant details like timelines, deadlines, or additional conversation.
    """

    # Generate the recommendation from GPT-2 model
    result = generator(prompt, max_length=200, num_return_sequences=1)
    recommendations = result[0]['generated_text']

    # Display the recommendations
    st.write("### Career and Study Path Recommendations")
    st.write(recommendations)
