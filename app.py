import streamlit as st
import requests
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Title of the app
st.title("Your Study & Career Path Buddy")

# Introduction
st.write("Welcome! This app will help guide you in choosing your study and career path based on your background, skills, and preferences.")

# Access Hugging Face token from Streamlit Secrets
hf_token = st.secrets["huggingface_token"]

# Initialize session state for form inputs if they do not exist
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'age' not in st.session_state:
    st.session_state.age = ""
if 'gender' not in st.session_state:
    st.session_state.gender = ""
if 'country' not in st.session_state:
    st.session_state.country = ""
if 'qualification' not in st.session_state:
    st.session_state.qualification = ""
if 'academic_interest' not in st.session_state:
    st.session_state.academic_interest = "STEM (Science, Technology, Engineering, Mathematics)"
if 'aspirations' not in st.session_state:
    st.session_state.aspirations = "Locally"
if 'hobbies' not in st.session_state:
    st.session_state.hobbies = ""
if 'skills' not in st.session_state:
    st.session_state.skills = ""
if 'languages' not in st.session_state:
    st.session_state.languages = ""

# Function to navigate to the next step
def go_to_next_step():
    st.session_state.step += 1

# Personal Information Section
if st.session_state.step == 1:
    st.header("Personal Information")
    with st.form(key='personal_info_form'):
        col1, col2 = st.columns([1, 1])

        # Personal details in two columns (Age and Gender in one row)
        with col1:
            st.session_state.age = st.text_input("Age", st.session_state.age)
        with col2:
            st.session_state.gender = st.text_input("Gender", st.session_state.gender)

        col3, col4 = st.columns([1, 1])
        
        # Country and Qualification in a single row (two columns)
        with col3:
            st.session_state.country = st.text_input("Country", st.session_state.country)
        with col4:
            st.session_state.qualification = st.text_input("Highest Qualification", st.session_state.qualification)

        # Submit button for personal info form
        submit_button_1 = st.form_submit_button("Next: Interests")
    
    # If the form is submitted, go to the next step
    if submit_button_1:
        go_to_next_step()

# Interests Section
if st.session_state.step == 2:
    st.header("Your Interests")
    with st.form(key='interests_form'):
        # Asking about academic interests
        st.session_state.academic_interest = st.radio(
            "Which academic field interests you the most?",
            options=["STEM (Science, Technology, Engineering, Mathematics)", 
                     "Humanities (Literature, History, Philosophy)", 
                     "Arts (Design, Music, Fine Arts)", 
                     "Business and Economics", 
                     "Other"],
            index=["STEM (Science, Technology, Engineering, Mathematics)", 
                   "Humanities (Literature, History, Philosophy)", 
                   "Arts (Design, Music, Fine Arts)", 
                   "Business and Economics", 
                   "Other"].index(st.session_state.academic_interest)
        )
        st.session_state.aspirations = st.selectbox("Do you want to work locally or internationally?", 
                                                   options=["Locally", "Internationally", "Both"],
                                                   index=["Locally", "Internationally", "Both"].index(st.session_state.aspirations))

        st.session_state.hobbies = st.text_area("Hobbies (e.g., music, sports, reading)", st.session_state.hobbies)

        # Submit button for interests form
        submit_button_2 = st.form_submit_button("Next: Skills & Languages")
    
    # If the form is submitted, go to the next step
    if submit_button_2:
        go_to_next_step()

# Skills and Language Section
if st.session_state.step == 3:
    st.header("Skills and Languages")
    with st.form(key='skills_form'):
        # Asking about skills and languages
        st.session_state.skills = st.text_area("Skills (e.g., programming, communication, leadership)", st.session_state.skills)
        st.session_state.languages = st.text_area("Languages you speak", st.session_state.languages)

        # Submit button for skills form
        submit_button_3 = st.form_submit_button("Submit")
    
    # If the form is submitted, show the recommendation section
    if submit_button_3:
        st.session_state.step = 4

# Final Recommendations Section
if st.session_state.step == 4:
    st.header("Summary of the Inputs")

    # Collect all data entered by the user and display it
    st.write(f"**Age**: {st.session_state.age}")
    st.write(f"**Gender**: {st.session_state.gender}")
    st.write(f"**Country**: {st.session_state.country}")
    st.write(f"**Qualification**: {st.session_state.qualification}")
    st.write(f"**Academic Interest**: {st.session_state.academic_interest}")
    st.write(f"**Career Aspiration**: {st.session_state.aspirations}")
    st.write(f"**Hobbies**: {st.session_state.hobbies}")
    st.write(f"**Skills**: {st.session_state.skills}")
    st.write(f"**Languages**: {st.session_state.languages}")

    # Placeholder for AI-generated response (can be replaced with actual recommendation logic)
    st.write("### Career and Study Path Recommendations")
    st.write(f"Recommended Study Paths: Based on your interest in {st.session_state.academic_interest} and skills.")
    st.write(f"Potential Career Options: Considering your aspiration to work {st.session_state.aspirations}.")

    # Provide a button to restart the app
    restart_button = st.button("Restart")
    if restart_button:
        st.session_state.step = 1
        st.session_state.age = ""
        st.session_state.gender = ""
        st.session_state.country = ""
        st.session_state.qualification = ""
        st.session_state.academic_interest = "STEM (Science, Technology, Engineering, Mathematics)"
        st.session_state.aspirations = ""
        st.session_state.hobbies = ""
        st.session_state.skills = ""
        st.session_state.languages = ""

    # Now, call the Hugging Face model to get recommendations based on user input
    if st.button("Get Career Recommendations"):
        user_data = {
            "age": st.session_state.age,
            "gender": st.session_state.gender,
            "country": st.session_state.country,
            "qualification": st.session_state.qualification,
            "academic_interest": st.session_state.academic_interest,
            "aspirations": st.session_state.aspirations,
            "hobbies": st.session_state.hobbies,
            "skills": st.session_state.skills,
            "languages": st.session_state.languages
        }

        headers = {
            "Authorization": f"Bearer {hf_token}"
        }

        # You can call Hugging Face's Inference API or any model endpoint you prefer here
        response = requests.post(
            "https://api-inference.huggingface.co/models/openai/gpt2",
            headers=headers,
            json={"inputs": str(user_data)}
        )

        # Check for valid response and display it
        if response.status_code == 200:
            recommendations = response.json()  # assuming the API returns recommendations
            st.write("### Career Recommendations")
            st.write(recommendations)
        else:
            st.error("Failed to get recommendations from the model. Please try again.")

