import streamlit as st
from pymongo import MongoClient

# MongoDB Configuration
MONGO_URI = "mongodb+srv://lshayikhah:0IPDJsxf5tkxKNIj@cluster0.dahg8.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["interview_system"]
users_collection = db["users"]
interviews_collection = db["interviews"]

st.set_page_config(page_title="HIREiT", page_icon="🔍", layout="centered")

# Helper Functions
def authenticate_user(username, password):
    user = users_collection.find_one({"username": username, "password": password, "role": "interviewer"})
    return user is not None 

def create_account(username, password, organization):
    if users_collection.find_one({"username": username}):
        return False
    users_collection.insert_one({"username": username, "password": password, "role": "interviewer", "organization": organization})
    return True

def login_signup_page():
    st.title("Interviewer Login/Sign-Up")
    tab = st.tabs(["Login", "Sign-Up"])

    # Login Tab
    with tab[0]:
        st.subheader("Login")
        username = st.text_input("National ID", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        login_btn = st.button("Login")

        if login_btn:
            if authenticate_user(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["page"] = "dashboard"  # Navigate to Dashboard
            else:
                st.error("Invalid username or password")

    # Sign-Up Tab
    with tab[1]:
        st.subheader("Sign-Up")
        new_username = st.text_input("National ID", key="signup_username")
        new_password = st.text_input("New Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
        organization = st.text_input("Organization", key="signup_organization")
        signup_btn = st.button("Sign-Up")

        if signup_btn:
            if new_password == confirm_password:
                if create_account(new_username, new_password, organization):
                    st.success("Account created successfully! Please log in.")
                else:
                    st.error("National ID already exists.")
            else:
                st.error("Passwords do not match.")

def dashboard_page():
    st.title(f"Welcome, {st.session_state['username']} - Interviewer Dashboard")

    # Create New Interview Section
    st.subheader("Create a New Interview")
    interviewee = st.text_input("Interviewee Username")
    date = st.date_input("DueDate")
    time = st.time_input("Due Time")
    questions = st.text_area("Questions").split("\n")
    create_btn = st.button("Create Interview")

    if create_btn:
        if interviewee and date and time and questions:
            interviews_collection.insert_one({
                "interviewee": interviewee,
                "interviewer": st.session_state["username"],
                "date": str(date),
                "time": str(time),
                "questions": questions,
                "status": "scheduled"
            })
            st.success("Interview scheduled successfully!")
        else:
            st.error("Please fill in all fields.")

    # View Scheduled Interviews
    st.subheader("Scheduled Interviews")
    interviews = list(interviews_collection.find({"interviewer": st.session_state["username"]}))

    if len(interviews) > 0:
        for interview in interviews:
            st.markdown(
                f"- **Interviewee:** {interview['interviewee']} | **Due Date:** {interview['date']} | **Due Time:** {interview['time']}"
            )
            if st.button(f"View Interview: {interview['_id']}", key=f"view_{interview['_id']}"):
                st.session_state["current_interview"] = interview
                st.session_state["page"] = "view_interview"
    else:
        st.write("No scheduled interviews.")

    # Logout Button
    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["page"] = "login"

# View Interview Page
def view_interview_page():
    interview = st.session_state["current_interview"]

    st.title(f"Interview ID: {interview['_id']}")
    st.subheader(f"Interviewee: {interview['interviewee']} | Due Date: {interview['date']} | DueTime: {interview['time']}")

    # Display Questions
    st.subheader("Interview Questions")
    for idx, question in enumerate(interview.get("questions", []), start=1):
        st.markdown(f"**Q{idx}: {question}**")

    if st.button("Back to Dashboard"):
        st.session_state["page"] = "dashboard"

# Main Logic
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "current_interview" not in st.session_state:
    st.session_state["current_interview"] = None

if not st.session_state["authenticated"]:
    login_signup_page()
else:
    if st.session_state["page"] == "dashboard":
        dashboard_page()
    elif st.session_state["page"] == "view_interview":
        view_interview_page()
