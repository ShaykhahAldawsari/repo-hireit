import streamlit as st

# Main Page Content
def main_page():
    # Add custom CSS for styling the buttons
    st.markdown(
        """
        <style>
            .main-container {
                max-width: 600px;
                margin: auto;
                text-align: center;
            }
            .button-row {
                display: flex;
                justify-content: space-between;
                gap: 10px;
            }
            .stButton>button {
                padding: 20px 40px;
                font-size: 20px;
                flex: 1; /* Make buttons take equal space */
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Main container with centered content
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Display Logo
    st.image("pages/HIREiT_logo.png")

    # Add buttons under the image, side by side
    st.markdown(
        """
        <div class="button-row">
            <div>
                <form action="/interviewer">
                    <button class="stButton" style="width: 100%;">Interviewer</button>
                </form>
            </div>
            <div>
                <form action="/interviewee">
                    <button class="stButton" style="width: 100%;">Interviewee</button>
                </form>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)
