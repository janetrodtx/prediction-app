import streamlit as st
import pandas as pd

# ✅ Load the latest dataset
df = pd.read_csv("Updated_Hair_Issues_Dataset_Cleaned.csv")

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

# --- 🎨 Custom Styling for Dark Mode ---
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
    st.image("Screenshot 2025-03-11 221723.png", width=250)  # ✅ Logo added
    st.title("Welcome to Hi Voltage Visuals:")
    st.title("Hair Care Edition⚡")
    st.write("✨Find the best hair care recommendations for your budget by answering a few quick questions✨")
    if st.button("Get Started"):
        next_step()

# --- Step 2: Choose Hair Concern ---
elif st.session_state.step == 2:
    st.subheader("🔍 What's your hair concern?")
    hair_issue = st.selectbox("Choose your hair issue with the dropdown menu:", df["Issue"].unique())
    st.session_state.hair_issue = hair_issue  # Store choice in session state
    if st.button("Next"):
        next_step()
    if st.button("Back"):
        go_back()

# --- Step 3: Show Cause & Solution ---
elif st.session_state.step == 3:
    issue_data = df[df["Issue"] == st.session_state.hair_issue].iloc[0]

    st.subheader(f"💡 Understanding **{issue_data['Issue']}**")
    st.write(f"📖 **Definition:** {issue_data['Definition']}")
    st.write(f"⚠️ **Cause:** {issue_data['Cause']}")

    # Ensure "Solution" exists to prevent errors
    if "Solution" in df.columns:
        st.write("🛠 **Solution:**")
        st.write(issue_data["Solution"])
    else:
        st.write("🛠 **Solution:** No solution available. Please update dataset.")

    if st.button("Next"):
        next_step()
    if st.button("Back"):
        go_back()

# --- Step 4: Select Budget ---
elif st.session_state.step == 4:
    st.subheader("💰 What's your budget?")
    budget = st.radio("Select your budget:", ["Under $25", "$25 & Up", "$75 & Up"])
    st.session_state.budget = budget  # Store budget selection
    if st.button("See My Product Recommendation"):
        next_step()
    if st.button("Back"):
        go_back()

# --- Step 5: Show Product Recommendations ---
elif st.session_state.step == 5:
    result = df[
        (df["Issue"] == st.session_state.hair_issue) &
        (df["Budget"].str.lower().str.strip() == st.session_state.budget.lower().strip())
    ]

    if not result.empty:
        st.subheader(f"✨ Recommended Products for **{st.session_state.hair_issue}** ✨")
        st.write(f"💰 **Budget:** {result.iloc[0]['Budget']}")

        # Extract and display recommended products properly
        product_text = result.iloc[0]['Recommended Product & Link']  # Get full product string

        # Ensure proper formatting and display
        if "](" in product_text:  # Check if there are links in the string
            formatted_products = product_text.replace(", ", "\n🔹 ")  # Add bullet points correctly
            st.markdown(f"🔹 {formatted_products}", unsafe_allow_html=True)
        else:
            st.write(f"🔹 {product_text}")  # If no links, display as plain text

    else:
        st.warning("❌ No product found for the selected budget.")

    if st.button("Start Over"):
        st.session_state.step = 1

