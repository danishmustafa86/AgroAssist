import os
import streamlit as st
import requests
from openai import OpenAI
from PIL import Image
import io
import base64  # Import base64 to encode the image

# Access API keys and base URL from Streamlit secrets
openai_api_key = st.secrets["openai"]["api_key"]
openai_base_url = st.secrets["openai"]["base_url"]
weather_api_key = st.secrets["weather"]["api_key"]

# Initialize OpenAI client with secret credentials
client = OpenAI(api_key=openai_api_key, base_url=openai_base_url)

# Set up Streamlit interface
st.set_page_config(page_title="AgroAssist", layout="wide")
st.title("AgroAssist: Your Smart Farming Assistant")
st.sidebar.title("Menu")

# Weather Forecast Feature
def get_weather_data(location):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={weather_api_key}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return {'message': response.json().get('message', 'Unknown error occurred')}
    
    return response.json()

# Sidebar for weather forecast input
st.sidebar.subheader("Weather Forecast")
location = st.sidebar.text_input("Enter your location", placeholder="e.g., City, State")
if location:
    weather_data = get_weather_data(location)
    if 'list' in weather_data:
        st.subheader(f"Weather in {location}")
        for forecast in weather_data['list'][:10]:  # Show next 5 forecasts
            st.write(f"{forecast['dt_txt']} - {forecast['main']['temp']}°C, {forecast['weather'][0]['description']}")
    else:
        if 'message' in weather_data:
            st.error(f"Error: {weather_data['message']}")
        else:
            st.error("Error fetching weather data. Please check the location or API key.")

# Crop Recommendation System
st.sidebar.subheader("Crop Recommendation")

# Allow the user to input any place over the world
region = st.sidebar.text_input("Enter your region or location", placeholder="e.g., City, Country")

# Select soil type remains as a dropdown menu
soil_type = st.sidebar.selectbox("Select soil type", ["Clay", "Sandy", "Loamy"])

# Get Recommendations based on user input
if st.sidebar.button("Get Recommendations"):
    # Make an API call to provide crop recommendations based on input region and soil type
    response = client.chat.completions.create(
        model="o1-mini",
        messages=[{
            "role": "user", 
            "content": f"Provide crop recommendations for the location {region} with soil type {soil_type}."
        }],
        max_tokens=90,
    )

    message = response.choices[0].message.content
    st.subheader(f"Recommended Crops for {region}")
    st.write(message)

# Spraying Advisory System
st.sidebar.subheader("Spraying Advisory")
crop = st.sidebar.text_input("Enter your crop type", placeholder="e.g., Wheat, Rice")
if crop:
    response = client.chat.completions.create(
        model="o1-mini",
        messages=[{"role": "user", "content": f"What is the spraying schedule for {crop}?"}],
        max_tokens=100,
    )

    message = response.choices[0].message.content
    st.subheader(f"Spraying Advisory for {crop}")
    st.write(message)

# Multilingual Chatbot
st.sidebar.subheader("Chat with AgroBot")
user_input = st.sidebar.text_input("Ask your question (e.g., crop advice, disease prevention)", placeholder="Type your question here...")
if user_input:
    response = client.chat.completions.create(
        model="o1-mini",
        messages=[{"role": "user", "content": user_input}],
        max_tokens=100,
    )

    message = response.choices[0].message.content
    st.subheader("AgroBot Response")
    st.write(message)

# Soil Health Monitoring Feature
st.sidebar.subheader("Soil Health Monitoring")

# Add more parameters for soil health analysis
ph_level = st.sidebar.slider("Select soil pH level", 0.0, 14.0, 7.0)
moisture = st.sidebar.slider("Select soil moisture level (%)", 0, 100, 50)
temperature = st.sidebar.slider("Select soil temperature (°C)", -10, 50, 20)
nitrogen = st.sidebar.slider("Select Nitrogen (N) level (ppm)", 0, 100, 30)
phosphorus = st.sidebar.slider("Select Phosphorus (P) level (ppm)", 0, 100, 20)
potassium = st.sidebar.slider("Select Potassium (K) level (ppm)", 0, 100, 40)
organic_matter = st.sidebar.slider("Select organic matter (%)", 0, 10, 5)
compaction = st.sidebar.slider("Select soil compaction level (g/cm³)", 1.0, 2.5, 1.4)

# Trigger the check when the button is clicked
if st.sidebar.button("Check Soil Health"):
    # Make an API call to assess soil health based on multiple factors
    response = client.chat.completions.create(
        model="o1-mini",
        messages=[{
            "role": "user", 
            "content": f"Assess soil health with pH level {ph_level}, moisture {moisture}%, temperature {temperature}°C, Nitrogen (N) {nitrogen} ppm, Phosphorus (P) {phosphorus} ppm, Potassium (K) {potassium} ppm, organic matter {organic_matter}%, compaction {compaction} g/cm³."
        }],
        max_tokens=100,
    )

    message = response.choices[0].message.content
    st.subheader("Soil Health Assessment Result")
    st.write(message)

# Final note for the user
st.sidebar.markdown("#### AgroAssist: Your Smart Farming Assistant")
st.sidebar.markdown("### We Value Your Feedback!")
st.sidebar.markdown("[Click here to provide feedback](https://docs.google.com/forms/u/0/d/1VXQ1dd6p_SFwjuWkTcqtZ1-A5O1M-FdyktcwTYXX5ig/viewform?edit_requested=true)")
st.sidebar.markdown("### Follow Us")
st.sidebar.markdown("[Linkedin](https://www.linkedin.com/in/danishmustafa86/) | [Facebook](https://www.facebook.com/danish.jajja.56?_rdc=1&_rdr) | [Github](https://github.com/danishmustafa86)")
st.sidebar.markdown("[Help & FAQs](link_to_help_section)")
st.sidebar.markdown("[Learn More About Smart Farming](https://www.cropin.com/smart-farming)")
