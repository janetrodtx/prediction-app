import streamlit as st
import pandas as pd

# Load the dataset
df = pd.read_csv("expanded_hair_issues.csv")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1

# Function to go to the next step
def next_step():
    st.session_state.step += 1

# Function to go back
def go_back():
    st.session_state.step -= 1

# --- Step 1: Welcome Page ---
if st.session_state.step == 1:
    st.title("⚡Welcome to Hi Voltage Hair-Care!⚡")
    st.write("Find the best hair care routine for you by answering a few quick questions.")
    if st.button("Get Started"):
        next_step()

# --- Step 2: Choose Hair Concern ---
elif st.session_state.step == 2:
    st.subheader("🔍 What's your hair concern?")
    hair_issue = st.selectbox("Choose your hair issue:", df["Issue"].unique())
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
    st.write(f"💡 **Solution:** The right hair care routine can help manage this issue.")
    
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

# --- Step 5: Show Product Recommendation ---
elif st.session_state.step == 5:
    result = df[(df["Issue"] == st.session_state.hair_issue) & (df["Budget"].str.lower().str.strip() == st.session_state.budget.lower().strip())]
    
    if not result.empty:
        st.subheader(f"✨ Your Hair Fix for **{st.session_state.hair_issue}** ✨")
        st.write(f"💰 **Budget:** {result.iloc[0]['Budget']}")
        product_info = result.iloc[0]['Recommended Product & Link']
        product_name = product_info.split('](')[0][1:]  # Extract text inside [ ]
        product_link = product_info.split('](')[1][:-1]  # Extract URL inside ( )

        st.markdown(f'[🛍 Buy {product_name} Now]({product_link})', unsafe_allow_html=True)
    else:
        st.warning("❌ No product found for the selected budget.")
    
    if st.button("Start Over"):
        st.session_state.step = 1

