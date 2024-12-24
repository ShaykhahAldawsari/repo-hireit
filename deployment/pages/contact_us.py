import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Main Page Configuration

# Email Sending Function
def send_email(subject, body):
    sender_email = "lishayikhah@gmail.com"  
    sender_password = "your_password"  # for security reasons
    recipient_email = "lishaikhahil@gmail.com"

    # Setting up the MIME
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to the server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# Contact Us Page Content
def contact_us_page():
    st.title("Contact Us")

    st.markdown("""
    If you have any questions, feedback, or need assistance, please fill out the form below, and we'll get back to you as soon as possible.
    """)

    # Contact Form
    with st.form("contact_form"):
        subject = st.text_input("Subject")
        body = st.text_area("Email Body")
        submitted = st.form_submit_button("Submit")

        if submitted:
            if subject and body:
                if send_email(subject, body):
                    st.success("Your email has been sent successfully!")
                else:
                    st.error("There was an error sending your email. Please try again later.")
            else:
                st.error("Please fill in all the fields before submitting.")

contact_us_page()
