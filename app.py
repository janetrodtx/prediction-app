import streamlit as st
import pandas as pd

# Load the dataset
df = pd.read_csv("expanded_hair_issues.csv")

# --- 🎨 Custom Styling (Black Background & White Text) ---
st.markdown(
    """
    <style>
        /* Set the full page background to black */
        body, .stApp {
            background-color: black;
            color: white;
        }
        /* Change headers and labels to white */
        h1, h2, h3, .stSelectbox label, .stRadio label, .stNumberInput label, .stTextInput label {
            color: white;
            text-align: center;
            font-family: 'Arial', sans-serif;
        }
        /* Style the numbers and dropdowns */
        .stNumberInput input, .stSelectbox select {
            color: white !important;
            background-color: black !important;
        }
        /* Style the buttons */
        .magic-button {
            display: block;
            width: 100%;
            text-align: center;
            background: #FFD700; /* Gold */
            padding: 15px;
            border-radius: 25px;
            font-size: 18px;
            font-weight: bold;
            color: black; /* Black text for contrast */
            cursor: pointer;
            transition: 0.3s;
            border: 2px solid white;
        }
        .magic-button:hover {
            background: #FFA500; /* Orange hover effect */
            color: white;
        }
        /* Style the warning message */
        .stAlert {
            background-color: black;
            color: white;
            border: 2px solid #FFD700;
        }
        /* Glowing effect */
        .glow {
            text-align: center;
            color: #FFD700;
            font-size: 24px;
            font-weight: bold;
            text-shadow: 0px 0px 10px #FFA500;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 🔥 Logo & Title ---
st.image("Screenshot 2025-03-11 221723.png", width=200)
st.title("⚡Welcome to Hi Voltage Vibes!⚡")
st.write("Your **magical** hair care recommendation guide! Answer a few questions and discover the perfect products.")

# --- 📝 User Input ---
st.subheader("🔍 What's your hair concern?")
hair_issue = st.selectbox("Choose your hair issue:", df["Issue"].unique())

st.subheader("💰 What's your budget?")
budget = st.radio("Select your budget:", ["Under $25", "$25 & Up", "$75 & up"])  # Normalized lowercase "up"

# --- 🔄 Ensure Budget Formatting Consistency ---
df["Budget"] = df["Budget"].str.lower().str.strip()
budget = budget.lower().strip()  # Convert user input to lowercase

# --- 🎯 Process Selection ---
result = df[(df["Issue"] == hair_issue) & (df["Budget"] == budget)]

if not result.empty:
    st.subheader(f"✨ Your Hair Fix for **{hair_issue}** ✨")
    st.write(f"📖 **Definition:** {result.iloc[0]['Definition']}")
    st.write(f"⚠️ **Cause:** {result.iloc[0]['Cause']}")
    st.write(f"💰 **Budget:** {result.iloc[0]['Budget']}")
    
    # Extract product name and link
    product_info = result.iloc[0]['Recommended Product & Link']
    product_name = product_info.split('](')[0][1:]  # Extracts text inside [ ]
    product_link = product_info.split('](')[1][:-1]  # Extracts URL inside ( )

    # Styled Button for Product Purchase
    st.markdown(f'<a class="magic-button" href="{product_link}" target="_blank">🛍 Buy {product_name} Now</a>', unsafe_allow_html=True)
else:
    st.warning("❌ No product found for the selected budget.")

# --- 📲 Hi Voltage Vibes Blog & Socials ---
st.markdown("---")
st.subheader("⚡ **Hi Voltage Vibes Blog** ⚡")
st.write("Check out our latest tips, product reviews, and magical hair care secrets!")
st.markdown(
    '<a class="magic-button" href="https://your-blog-url.com" target="_blank">📖 Visit Blog</a>',
    unsafe_allow_html=True
)

st.subheader("✨ Let's Stay Connected! ✨")
st.markdown(
    """
    <p style="text-align:center;">
        <a href="https://www.instagram.com/hivoltagevisuals/">📸 Instagram</a> |
        <a href="https://tiktok.com" target="_blank">🎵 TikTok</a>
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")
st.markdown('<p class="glow">Powered by Hi Voltage Vibes ⚡</p>', unsafe_allow_html=True)
