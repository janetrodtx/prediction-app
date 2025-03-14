import streamlit as st
import pandas as pd
import os

# ✅ Load the latest dataset
csv_file = "Updated_Hair_Issues_Dataset - Updated_Hair_Issues_Dataset.csv.csv"
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.strip()  # Ensure column names are clean
else:
    st.error("❌ Data file not found. Please upload 'Updated_Hair_Issues_Dataset.csv'.")
    st.stop()

# ✅ Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1

# Function to go to the next step
def next_step():
    st.session_state.step += 1

# Function to go back
def go_back():
    st.session_state.step -= 1

# Function to display images safely
def show_image(image_path):
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.warning(f"⚠️ Missing image: {image_path}")

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
    </style>
    """,
    unsafe_allow_html=True
)

# --- Step 1: Welcome Page ---
if st.session_state.step == 1:
    show_image("1.png")  # ✅ Welcome Screen UI
    if st.button("Start"):
        next_step()

# --- Step 2: Choose Hair Concern ---
elif st.session_state.step == 2:
    show_image("2.png")  # ✅ Hair Concern Selection UI
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
    show_image("4.png")  # ✅ Understanding Your Hair UI

    st.markdown(f"<h2 style='text-align: center;'>Understanding {issue_data['Issue']}</h2>", unsafe_allow_html=True)
    st.write(f"📖 **Definition:** {issue_data['Definition']}")
    st.write(f"⚠️ **Cause:** {issue_data['Cause']}")
    st.write("🛠 **Solution:**")
    st.write(issue_data["Solution"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            go_back()
    with col2:
        if st.button("Next"):
            next_step()

# --- Step 4: Select Budget ---
elif st.session_state.step == 4:
    show_image("3.png")  # ✅ Budget Selection UI
    budget = st.radio("", ["Under $25", "$25 & Up", "$75 & Up"])
    st.session_state.budget = budget  # Store budget selection
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            go_back()
    with col2:
        if st.button("See My Product Recommendation"):
            next_step()

# --- Step 5: Show Product Recommendations ---
elif st.session_state.step == 5:
    result = df[
        (df["Issue"] == st.session_state.hair_issue) &
        (df["Budget"].str.lower().str.strip() == st.session_state.budget.lower().strip())
    ]

    show_image("5.png")  # ✅ Product Recommendation UI

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



