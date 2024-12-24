import streamlit as st



# About Page Content
def about_page():
    st.title("About Us")

    st.markdown(
        """
        <div style="text-align: center;">
        <h2>Welcome to the Interview Automation System</h2>
    #  i didn't commit the website so manaa doesn't work on it be himself 
    # so you will commit all things (models + stramlit) 
    # no just the website
    # im gonna work on integrating the website with the models  
    # it's not gonna take time i hope

        <hr>

        <p>The Interview Automation System is designed to revolutionize the way interviews are conducted. By leveraging advanced AI and modern technology, our platform helps interviewers and interviewees streamline their interview process, ensuring efficiency and quality insights.</p>

        <hr>

        <h3>Our Mission</h3>
        <p>To empower organizations and individuals by providing a smart, efficient, and user-friendly platform for conducting, analyzing, and improving interviews.</p>

        <hr>

        <h3>Key Features</h3>
        <ul style="list-style-type:none;">
            <li><strong>AI-Powered Analysis:</strong> Real-time analysis of body language, eye contact, voice tone, and more.</li>
            <li><strong>Streamlined Workflow:</strong> From scheduling to final reporting, everything is managed in one place.</li>
            <li><strong>User-Centric Design:</strong> Intuitive interface tailored for both interviewers and interviewees.</li>
        </ul>

        <hr>

        <h3>Our Team</h3>
        <p>We are a group of passionate developers, data scientists, and designers committed to transforming traditional interviews into a seamless experience. Our expertise spans AI, machine learning, and human-computer interaction.</p>

        <hr>

        </div>
        """,
        unsafe_allow_html=True
    )

# Display About Page
about_page()
