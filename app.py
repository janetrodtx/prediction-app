import streamlit as st
import pandas as pd

# ✅ Load the latest dataset
df = pd.read_csv("Updated_Hair_Issues_Dataset - Updated_Hair_Issues_Dataset.csv.csv")

# ✅ Ensure column names are clean
df.columns = df.columns.str.strip()

# ✅ Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1

# Function to go to the next step
def next_step():
    st.session_state.step += 1

# Function to go back
def go_back():
    st.session_state.step -= 1

# --- 🎨 Custom Styling for Dark Mode & UI ---
st.markdown(
    """
    <style>
        body, .stApp {
            background-color: black;
            color: white;
        }
        h1, h2, h3, .stSelectbox label, .stRadio label {
            color: white;
            font-family: 'Arial', sans-serif;
            text-align: center;
        }
        .stRadio div {
            color: white !important;  /* ✅ Fixes budget text visibility */
        }
        .stButton button {
            background-color: #FFD700;
            color: black;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px;
        }
        .styled-image {
            display: block;
            margin: auto;
            width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Step 1: Welcome Page ---
if st.session_state.step == 1:
    st.image("welcome.png", use_column_width=True)  # ✅ Welcome Screen UI
    if st.button("Start"):
        next_step()

# --- Step 2: Choose Hair Concern ---
elif st.session_state.step == 2:
    st.image("concern.png", use_column_width=True)  # ✅ Hair Concern Selection UI
    hair_issue = st.selectbox("", df["Issue"].unique())
    st.session_state.hair_issue = hair_issue  # Store choice in session state
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            go_back()
    with col2:
        if st.button("Next"):
            next_step()

# --- Step 3: Show Cause & Solution ---
elif st.session_state.step == 3:
    issue_data = df[df["Issue"] == st.session_state.hair_issue].iloc[0]

    # ✅ Custom CSS to fix background size and center content properly
    st.markdown(
        f"""
        <style>
            .stApp {{
                background: url("back1.png") no-repeat center center fixed;
                background-size: 90% auto; /* Scales image width to 90% while keeping proportions */
                background-position: center;
                background-attachment: fixed;
                background-repeat: no-repeat;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                padding-top: 50px;
            }}
            .content-container {{
                background: rgba(0, 0, 0, 0.6); /* Slight transparency for better text visibility */
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                max-width: 700px;
                margin: auto;
            }}
            h2, p {{
                color: white;
                font-family: 'Arial', sans-serif;
            }}
        </style>
        <div class='content-container'>
            <h2>Understanding {issue_data['Issue']}</h2>
            <p>📖 <b>Definition:</b> {issue_data['Definition']}</p>
            <p>⚠️ <b>Cause:</b> {issue_data['Cause']}</p>
            <p>🛠 <b>Solution:</b> {issue_data['Solution']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            go_back()
    with col2:
        if st.button("Next"):
            next_step()


# --- Step 4: Select Budget ---
elif st.session_state.step == 4:
    st.image("budget.png", use_container_width=True)  # ✅ Budget Selection UI

    # Create three columns for budget options
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("", key="under25"):  # ✅ Clickable PNG for Under $25
            st.session_state.budget = "Under $25"
            next_step()
        st.image("under25.png", width=150)

    with col2:
        if st.button("", key="25nup"):  # ✅ Clickable PNG for $25 & Up
            st.session_state.budget = "$25 & Up"
            next_step()
        st.image("25nup.png", width=150)

    with col3:
        if st.button("", key="75nup"):  # ✅ Clickable PNG for $75 & Up
            st.session_state.budget = "$75 & Up"
            next_step()
        st.image("75nup.png", width=150)

    # Back button at the bottom
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back"):
            go_back()

# --- Step 5: Show Product Recommendations ---
elif st.session_state.step == 5:
    result = df[
        (df["Issue"] == st.session_state.hair_issue) &
        (df["Budget"].str.lower().str.strip() == st.session_state.budget.lower().strip())
    ]

    # ✅ CSS for overlaying text on the image
    st.markdown(
      
        <style>
            .container {
                position: relative;
                width: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
            }
            .image {
                width: 80%; /* Adjust image size */
                height: auto;
                display: block;
            }
            .overlay-text {
                position: absolute;
                top: 50%;  /* Moves text UP/DOWN */
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 30px;
                font-weight: bold;
                color: white;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
                font-family: 'Arial', sans-serif;
            }
        </style>
        <div class="container">
            <img src="back2.png" class="image">
            <div class="overlay-text">Recommended Products for {}</div>
        </div>
        .format(st.session_state.hair_issue),
        unsafe_allow_html=True
    )

    # Budget and product recommendations
    if not result.empty:
        st.markdown(f"<h3 style='text-align: center; color: white;'>💰 <b>Budget:</b> {result.iloc[0]['Budget']}</h3>", unsafe_allow_html=True)

        product_text = result.iloc[0]['Recommended Product & Link']

        if "](" in product_text:  # Check if there are links
            formatted_products = product_text.replace(", ", "<br>🔹 ")  # Bullet points for list
            st.markdown(f"<p style='text-align: center; font-size: 18px; color: white;'>🔹 {formatted_products}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='text-align: center; font-size: 18px; color: white;'>🔹 {product_text}</p>", unsafe_allow_html=True)

    else:
        st.warning("❌ No product found for the selected budget.")

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            go_back()
    with col2:
        if st.button("Start Over"):
            st.session_state.step = 1


