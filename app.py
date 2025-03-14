import streamlit as st
import base64

# Function to set background for Steps 3 & 5
def set_background(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    background_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1
if "selected_budget" not in st.session_state:
    st.session_state.selected_budget = None

# Define steps
steps = [
    "Step 1: Welcome",
    "Step 2: Select Your Budget",
    "Step 3: Show Cause & Solution",
    "Step 4: Product Analysis",
    "Step 5: Show Product Recommendations",
]

# Apply background only for Step 3 & 5
if st.session_state.step in [3, 5]:
    set_background("images/back1.png")

# Display the step title
st.title(steps[st.session_state.step - 1])

# Step 2: Budget Selection
if st.session_state.step == 2:
    st.write("💰 **Please select your budget:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("![Under $25](images/under25.png)", key="under_25"):
            st.session_state.selected_budget = "Under $25"
            st.success("Selected budget: Under $25")
    
    with col2:
        if st.button("![$25 & Up](images/25nup.png)", key="25_and_up"):
            st.session_state.selected_budget = "$25 & Up"
            st.success("Selected budget: $25 & Up")
    
    with col3:
        if st.button("![$75 & Up](images/75nup.png)", key="75_and_up"):
            st.session_state.selected_budget = "$75 & Up"
            st.success("Selected budget: $75 & Up")

# Show selected budget after Step 2
if st.session_state.selected_budget and st.session_state.step > 2:
    st.write(f"🎯 **Your selected budget:** {st.session_state.selected_budget}")

# Navigation buttons
col1, col2 = st.columns(2)

with col1:
    if st.session_state.step > 1:
        if st.button("⬅ Previous"):
            st.session_state.step -= 1

with col2:
    if st.session_state.step < len(steps):
        if st.button("Next ➡"):
            st.session_state.step += 1


