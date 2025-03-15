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

    # ✅ Custom CSS to set and scale the background image properly
    st.markdown(
        f"""
        <style>
            .stApp {{
                background: url("back1.png") no-repeat center center fixed;
                background-size: contain; /* Ensures the full image is visible */
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                padding-top: 50px;
            }}
            .content-container {{
                background: rgba(0, 0, 0, 0.7); /* Adds a subtle background to improve readability */
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                max-width: 800px;
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

    st.image("back2.png", use_column_width=True)  # ✅ Product Recommendation UI

    if not result.empty:
        st.markdown(f"<h2 style='text-align: center;'>Recommended Products for {st.session_state.hair_issue}</h2>", unsafe_allow_html=True)
        st.write(f"💰 **Budget:** {result.iloc[0]['Budget']}")

        product_text = result.iloc[0]['Recommended Product & Link']

        # Format product recommendations properly
        if "](" in product_text:  # Check if there are links
            formatted_products = product_text.replace(", ", "\n🔹 ")  # Bullet points for list
            st.markdown(f"🔹 {formatted_products}", unsafe_allow_html=True)
        else:
            st.write(f"🔹 {product_text}")

    else:
        st.warning("❌ No product found for the selected budget.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            go_back()
    with col2:
        if st.button("Start Over"):
            st.session_state.step = 1


