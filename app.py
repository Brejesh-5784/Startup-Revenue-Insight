import streamlit as st
import joblib
import numpy as np
import pandas as pd

# --- Page Configuration (Must be FIRST Streamlit call) ---
st.set_page_config(
    page_title="Startup Profit Prediction",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Configuration for your specific model ---
FEATURE_NAMES = ['R&D Spend', 'Administration', 'Marketing Spend', 'State_encoded']
STATE_MAPPING = {
    'California': 0,
    'Florida': 1,
    'New York': 2
}
MODEL_PATH = 'model.pkl'

# --- Load the Model ---
@st.cache_resource
def load_model(path):
    """Loads the pre-trained model."""
    try:
        model = joblib.load(path)
        st.success(f"Model loaded successfully from {path}!")
        return model
    except FileNotFoundError:
        st.error(f"Error: Model file not found at '{path}'. Please ensure 'model.pkl' is in the same directory as 'app.py'.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading model: {e}. Please check your model file and ensure all necessary libraries are installed.")
        st.stop()

model = load_model(MODEL_PATH)

# --- Custom CSS ---
st.markdown("""
    <style>
    .main-header {
        font-size: 3em;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .subheader {
        font-size: 1.5em;
        color: #333;
        text-align: center;
        margin-bottom: 1em;
    }
    .prediction-box {
        background-color: #e6ffe6;
        border-left: 5px solid #4CAF50;
        padding: 1em;
        border-radius: 5px;
        margin-top: 2em;
        text-align: center;
        font-size: 1.8em;
        font-weight: bold;
        color: #2e7d32;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        font-size: 1.2em;
        padding: 0.5em 1em;
        border-radius: 0.5em;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Page Title ---
st.markdown("<h1 class='main-header'>💰 Startup Profit Predictor 💰</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Enter the details below to estimate the profit of a new startup.</p>", unsafe_allow_html=True)

# --- Sidebar Inputs ---
st.sidebar.header("Input Features")

rd_spend = st.sidebar.number_input(
    "R&D Spend (in USD)", min_value=0.0, max_value=200000.0, value=73721.62,
    step=1000.0, format="%.2f"
)

admin_spend = st.sidebar.number_input(
    "Administration Spend (in USD)", min_value=0.0, max_value=200000.0, value=121344.64,
    step=1000.0, format="%.2f"
)

marketing_spend = st.sidebar.number_input(
    "Marketing Spend (in USD)", min_value=0.0, max_value=500000.0, value=211025.10,
    step=1000.0, format="%.2f"
)

selected_state = st.sidebar.selectbox(
    "State", options=list(STATE_MAPPING.keys())
)
state_encoded_value = STATE_MAPPING[selected_state]

# --- Prepare Data for Model ---
input_data = {
    'R&D Spend': rd_spend,
    'Administration': admin_spend,
    'Marketing Spend': marketing_spend,
    'State_encoded': state_encoded_value
}
input_df = pd.DataFrame([input_data], columns=FEATURE_NAMES)

# --- Display Input Summary ---
st.subheader("Your Input Summary:")
st.write(input_df)

# --- Prediction ---
if st.button("Predict Profit"):
    with st.spinner('Calculating profit...'):
        try:
            predicted_profit = model.predict(input_df)[0]
            st.markdown(f"<div class='prediction-box'>Estimated Profit: ${predicted_profit:,.2f}</div>", unsafe_allow_html=True)
            st.success("Prediction complete!")
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")
            st.warning("Please ensure the input values are correct and match the model's expectations.")

st.markdown("---")
st.markdown("App built with ❤️ using Streamlit and a Linear Regression Model.")
