import streamlit as st

# Main Page Configuration

# FAQs Content
def faqs_page():
    st.title("Frequently Asked Questions")

    st.markdown("""
        Below you can find answers to common questions. Click on each question to view the answer.
    """)

    # Dropdown Questions
    with st.expander("What is the Interview Automation System?"):
        st.write("The Interview Automation System is a platform designed to streamline and partially automate interviews by providing tools for scheduling, conducting, and analyzing interviews with AI insights.")

    with st.expander("How do I access my account?"):
        st.write("You can access your account by logging in using the username and password you created during sign-up.")

    with st.expander("How do I create a new interview (for Interviewers)?"):
        st.write("Log in to your interviewer account and click on \"Create New Interview\" on your dashboard.")

    with st.expander("Where can I find reports for completed interviews?"):
        st.write("Reports can be accessed from your dashboard under the \"Interviewee Reports\" section.")

    with st.expander("How do I check my scheduled interviews (for Interviewees)?"):
        st.write("After logging in, you can view all your scheduled interviews on your dashboard.")

    with st.expander("What should I do if I cannot start my interview?"):
        st.write("Ensure your device's camera and microphone are functioning. If the problem persists, contact support.")

    with st.expander("How is my data protected?"):
        st.write("We prioritize data security by encrypting sensitive information and following industry best practices.")

    with st.expander("Can I change my password?"):
        st.write("Yes, you can change your password from your account settings after logging in.")

    with st.expander("Who do I contact for support?"):
        st.write("For support, email us at support@interviewautomation.com or visit the \"Contact Us\" page.")

# Display FAQs
faqs_page()