import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Load the model and tokenizer using st.cache_resource
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("facebook/m2m100_418M")
    model = AutoModelForSeq2SeqLM.from_pretrained("facebook/m2m100_418M")
    return tokenizer, model

tokenizer, model = load_model()

# Create a translation pipeline using the model
pipe = pipeline("translation", model=model, tokenizer=tokenizer)

# Function to generate career recommendations based on user data
def generate_career_recommendations(user_data):
    prompt = (
        f"User Profile:\n"
        f"Age: {user_data['age']}\n"
        f"Gender: {user_data['gender']}\n"
        f"Country: {user_data['country']}\n"
        f"Qualification: {user_data['qualification']}\n"
        f"Academic Interest: {user_data['academic_interest']}\n"
        f"Career Aspiration: {user_data['aspirations']}\n"
        f"Hobbies: {user_data['hobbies']}\n"
        f"Skills: {user_data['skills']}\n"
        f"Languages: {user_data['languages']}\n\n"
        "Translate this user profile into career and academic advice."
    )

    # Use the model to generate a translation (career advice or recommendations)
    output = pipe(prompt, max_length=300)

    recommendations = output[0]['translation_text']
    return recommendations

# Streamlit UI
st.title("Career and Study Path Recommendation")

# Multi-step form using session state
if 'step' not in st.session_state:
    st.session_state.step = 1

# Initialize user data in session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'age': '',
        'gender': '',
        'country': '',
        'qualification': '',
        'academic_interest': 'STEM',
        'aspirations': 'Locally',
        'hobbies': '',
        'skills': '',
        'languages': ''
    }

# Step 1: Personal Information
if st.session_state.step == 1:
    st.header("Personal Information")
    with st.form(key='personal_info_form'):
        st.session_state.user_data['age'] = st.text_input("Age", st.session_state.user_data['age'])
        st.session_state.user_data['gender'] = st.text_input("Gender", st.session_state.user_data['gender'])
        st.session_state.user_data['country'] = st.text_input("Country", st.session_state.user_data['country'])
        st.session_state.user_data['qualification'] = st.text_input("Qualification", st.session_state.user_data['qualification'])
        if st.form_submit_button("Next: Interests"):
            st.session_state.step = 2

# Step 2: Interests
if st.session_state.step == 2:
    st.header("Your Interests")
    with st.form(key='interests_form'):
        st.session_state.user_data['academic_interest'] = st.radio(
            "Which academic field interests you the most?",
            options=["STEM", "Humanities", "Arts", "Business"],
            index=["STEM", "Humanities", "Arts", "Business"].index(st.session_state.user_data['academic_interest'])
        )
        st.session_state.user_data['aspirations'] = st.selectbox(
            "Do you want to work locally or internationally?",
            options=["Locally", "Internationally", "Both"],
            index=["Locally", "Internationally", "Both"].index(st.session_state.user_data['aspirations'])
        )
        st.session_state.user_data['hobbies'] = st.text_area("Hobbies", st.session_state.user_data['hobbies'])
        st.session_state.user_data['skills'] = st.text_area("Skills", st.session_state.user_data['skills'])
        st.session_state.user_data['languages'] = st.text_area("Languages", st.session_state.user_data['languages'])
        
        if st.form_submit_button("Next: Get Recommendations"):
            st.session_state.step = 3

# Step 3: Display Recommendations
if st.session_state.step == 3:
    st.header("Career and Study Path Recommendations")
    
    # Generate recommendations based on user data
    recommendations = generate_career_recommendations(st.session_state.user_data)
    
    # Display recommendations
    st.write(recommendations)

    # Option to reset the form
    if st.button("Start Over"):
        st.session_state.step = 1
