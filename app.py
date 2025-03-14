import streamlit as st

# Define the budget images
budget_images = {
    "under_25": "under25.png",
    "25_and_up": "25nup.png",
    "75_and_up": "75nup.png"
}

# Define the background image for Steps 3 and 5
background_image = "back1.png"

# Function to set the background
def set_background(step):
    if step in [3, 5]:  # Apply background only to Step 3 and Step 5
        page_bg = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{get_image_as_base64(background_image)}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """
        st.markdown(page_bg, unsafe_allow_html=True)

# Helper function to encode image as base64
import base64
def get_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Define the steps
steps = [
    "Step 1: Welcome",
    "Step 2: Select Your Budget",
    "Step 3: Show Cause & Solution",
    "Step 4: Product Analysis",
    "Step 5: Show Product Recommendations",
]

# Streamlit session state for step navigation
if "step" not in st.session_state:
    st.session_state.step = 1
if "selected_budget" not in st.session_state:
    st.session_state.selected_budget = None

# Function to change steps
def next_step():
    if st.session_state.step < len(steps):
        st.session_state.step += 1

def prev_step():
    if st.session_state.step > 1:
        st.session_state.step -= 1

# Set background if applicable
set_background(st.session_state.step)

# Main app layout
st.title(steps[st.session_state.step - 1])

# Step 2: Budget Selection
if st.session_state.step == 2:
    st.write("Please select your budget:")
    cols = st.columns(3)
    
    for idx, (key, img) in enumerate(budget_images.items()):
        with cols[idx]:
            if st.button(f"![Budget]({img})", key=key):
                st.session_state.selected_budget = key
                st.success(f"Selected budget: {key.replace('_', ' ').title()}")
                next_step()

# Display selected budget after Step 2
if st.session_state.selected_budget and st.session_state.step > 2:
    st.write(f"**Your selected budget:** {st.session_state.selected_budget.replace('_', ' ').title()}")

# Step navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.session_state.step > 1:
        st.button("Previous", on_click=prev_step)
with col2:
    if st.session_state.step < len(steps):
        st.button("Next", on_click=next_step)

