import streamlit as st

# Main Page Content
def main_page():
    # Logo Section
    st.markdown("""
        <div style="text-align: center;">
            <h1>Interview Automation System</h1>
            <img src="https://via.placeholder.com/150" alt="Logo" style="width:150px; margin-bottom:20px;">
        </div>
    """, unsafe_allow_html=True)

    # Buttons for Interviewer and Interviewee
    st.markdown("""
        <div style="text-align: center; margin-top: 20px;">
            <a href="/interviewer" style="text-decoration: none;">
                <button style="padding: 15px 30px; margin: 10px; font-size: 16px;">Interviewer</button>
            </a>
            <a href="/interviewee" style="text-decoration: none;">
                <button style="padding: 15px 30px; margin: 10px; font-size: 16px;">Interviewee</button>
            </a>
        </div>
    """, unsafe_allow_html=True)
