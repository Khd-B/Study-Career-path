import streamlit as st
from transformers import ByT5Tokenizer, ByT5ForConditionalGeneration

# Load the ByT5 model and tokenizer using st.cache_resource
@st.cache_resource
def load_model():
    tokenizer = ByT5Tokenizer.from_pretrained("google/byt5-small")
    model = ByT5ForConditionalGeneration.from_pretrained("google/byt5-small")
    return tokenizer, model

tokenizer, model = load_model()

# Function to generate career recommendations
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
        
        "Generate academic and career advice based on the above profile."
    )

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=300) 

    recommendations = tokenizer.decode(outputs[0], skip_special_tokens=True)
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
        if st.form_submit_button("Next: Skills & Languages"):
            st.
