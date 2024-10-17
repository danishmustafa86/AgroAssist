# Step 1: Import required libraries
import streamlit as st
import requests
from PIL import Image

# Step 2: Set up Streamlit interface
st.set_page_config(page_title="AgroAssist", layout="wide")
st.title("AgroAssist: Your Smart Farming Assistant")
st.sidebar.title("Menu")

# Weather Forecast Feature
def get_weather_data(location):
    api_key = ''  # Replace with your OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    return response

# Sidebar for weather forecast input
st.sidebar.subheader("Weather Forecast")
location = st.sidebar.text_input("Enter your location")
if location:
    weather_data = get_weather_data(location)

    # Check if the API request was successful and 'list' exists
    if 'list' in weather_data:
        st.subheader(f"Weather in {location}")
        for forecast in weather_data['list'][:5]:  # Safely access 'list'
            st.write(f"{forecast['dt_txt']} - {forecast['main']['temp']}°C")
    else:
        # Handle error case (e.g., location not found or invalid API key)
        if 'message' in weather_data:
            st.error(f"Error: {weather_data['message']}")
        else:
            st.error("Error fetching weather data. Please check the location or API key.")

# Crop Disease Detection Feature
st.sidebar.subheader("Crop Disease Detection")
uploaded_file = st.sidebar.file_uploader("Upload an image of your crop")
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Crop Image", use_column_width=True)

    # Send to AIML API (assuming AIML API for disease detection)
    disease_url = "https://api.aimlapi.com/disease_detection"
    files = {'file': uploaded_file}
    headers = {'Authorization': ''}  # Replace with your AIML API key
    response = requests.post(disease_url, files=files, headers=headers).json()

    st.subheader("Disease Detection Result")
    if response.get("disease"):
        st.write(f"Disease: {response['disease']}")
        st.write(f"Suggested Action: {response['suggestion']}")
    else:
        st.error("Could not detect disease. Please try again.")

# Crop Recommendation System
st.sidebar.subheader("Crop Recommendation")
region = st.sidebar.selectbox("Select your region", ["Region1", "Region2", "Region3"])
soil_type = st.sidebar.selectbox("Select soil type", ["Clay", "Sandy", "Loamy"])
if st.sidebar.button("Get Recommendations"):
    crop_recommendation_url = "https://api.aimlapi.com/crop_recommendation"
    data = {"region": region, "soil_type": soil_type}
    headers = {'Authorization': 'Bearer your_api_key'}  # Replace with your AIML API key
    response = requests.post(crop_recommendation_url, json=data, headers=headers).json()

    st.subheader("Recommended Crops")
    if response.get("crops"):
        for crop in response["crops"]:
            st.write(f"Crop: {crop['name']} | Suitable Time: {crop['season']}")
    else:
        st.error("Could not retrieve crop recommendations. Please check the inputs or try again.")

# Spraying Advisory System
st.sidebar.subheader("Spraying Advisory")
crop = st.sidebar.text_input("Enter your crop type")
if crop:
    spraying_url = "https://api.aimlapi.com/spraying_schedule"
    data = {"crop": crop}
    headers = {'Authorization': 'Bearer your_api_key'}  # Replace with your AIML API key
    response = requests.post(spraying_url, json=data, headers=headers).json()

    st.subheader(f"Spraying Advisory for {crop}")
    if response.get("schedule"):
        st.write(f"Next Spraying Time: {response['schedule']['next_spray']}")
        st.write(f"Pesticide Type: {response['schedule']['pesticide']}")
    else:
        st.error("Could not retrieve spraying schedule. Please check the crop type or try again.")

# Multilingual Chatbot
st.sidebar.subheader("Chat with AgroBot")
user_input = st.sidebar.text_input("Ask your question (e.g., crop advice, disease prevention)")
if user_input:
    chatbot_url = "https://api.aimlapi.com/gpt_chatbot"
    data = {"query": user_input}
    headers = {'Authorization': 'Bearer your_api_key'}  # Replace with your AIML API key
    response = requests.post(chatbot_url, json=data, headers=headers).json()

    st.subheader("AgroBot Response")
    if response.get("response"):
        st.write(response['response'])
    else:
        st.error("Chatbot could not provide a response. Please try again.")

# Soil Health Monitoring Feature
st.sidebar.subheader("Soil Health Monitoring")
ph_level = st.sidebar.slider("Select soil pH level", 0.0, 14.0, 7.0)
moisture = st.sidebar.slider("Select soil moisture level (%)", 0, 100, 50)
if st.sidebar.button("Check Soil Health"):
    soil_health_url = "https://api.aimlapi.com/soil_health"
    data = {"ph_level": ph_level, "moisture": moisture}
    headers = {'Authorization': 'Bearer your_api_key'}  # Replace with your AIML API key
    response = requests.post(soil_health_url, json=data, headers=headers).json()

    st.subheader("Soil Health Report")
    if response.get("ph_level") and response.get("moisture"):
        st.write(f"pH Level: {response['ph_level']}")
        st.write(f"Moisture Level: {response['moisture']}")
        st.write(f"Recommended Action: {response['recommendation']}")
    else:
        st.error("Could not retrieve soil health data. Please try again.")
