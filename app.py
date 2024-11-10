import streamlit as st
from transformers import pipeline

# Set up the app title
st.title("Career and Study Path Recommendations")

# Introduction text for the user
st.write(
    """
    This app helps you find personalized career and study path recommendations based on your profile.
    Fill out the form below and click 'Get Recommendations' to receive tailored advice.
    """
)

# User input form (keeping your original UI design)
with st.form(key='user_input_form'):
    # Collect user information
    age = st.text_input("Age")
    gender = st.text_input("Gender")
    country = st.text_input("Country")
    qualification = st.text_input("Highest Qualification")
    academic_interest = st.radio("Academic Interest", ["STEM", "Humanities", "Arts", "Business", "Other"])
    aspirations = st.selectbox("Do you want to work locally or internationally?", ["Locally", "Internationally", "Both"])
    hobbies = st.text_area("Hobbies (e.g., music, sports, reading)")
    skills = st.text_area("Skills (e.g., programming, communication, leadership)")
    languages = st.text_area("Languages you speak")

    # Submit button
    submit_button = st.form_submit_button(label="Get Recommendations")

# If the form is submitted, generate recommendations
if submit_button:
    # Display the user's profile summary
    st.write("### Summary of Inputs")
    st.write(f"**Age**: {age}")
    st.write(f"**Gender**: {gender}")
    st.write(f"**Country**: {country}")
    st.write(f"**Highest Qualification**: {qualification}")
    st.write(f"**Academic Interest**: {academic_interest}")
    st.write(f"**Career Aspiration**: {aspirations}")
    st.write(f"**Hobbies**: {hobbies}")
    st.write(f"**Skills**: {skills}")
    st.write(f"**Languages**: {languages}")

    # Construct a more detailed prompt to send to the model
    prompt = f"""
    You are a career advisor. Based on the following profile, recommend specific career paths or study paths:
    
    Age: {age}
    Gender: {gender}
    Country: {country}
    Highest Qualification: {qualification}
    Academic Interest: {academic_interest}
    Career Aspiration: {aspirations}
    Hobbies: {hobbies}
    Skills: {skills}
    Languages: {languages}
    
    Please provide detailed career and study recommendations. Include suggestions for relevant degrees, certifications, job roles, and possible career growth. Focus on practical and realistic advice.
    """

    # Load the google/byt5-small model using Hugging Face pipeline
    pipe = pipeline("text2text-generation", model="google/byt5-small")

    # Generate the response from the model
    try:
        result = pipe(prompt, max_length=200, num_return_sequences=1)
        st.write("### Career and Study Path Recommendations")
        st.write(result[0]['generated_text'])
    except Exception as e:
        st.error(f"Failed to get recommendations from the model. Error: {str(e)}")
