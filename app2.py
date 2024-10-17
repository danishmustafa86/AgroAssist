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

# Language selection
# Language selection
language = st.selectbox("Select Language", [
    "English", 
    "Español", 
    "Français", 
    "اردو", 
    "Deutsch", 
    "中文", 
    "العربية", 
    "Русский"
])
translations = {
    "English": {
        "weather_forecast": "Weather Forecast",
        "enter_location": "Enter your location",
        "recommended_crops": "Recommended Crops for",
        "spraying_advisory": "Spraying Advisory for",
        "chat_with_agrobot": "Chat with AgroBot",
        "soil_health_monitoring": "Soil Health Monitoring",
        "check_soil_health": "Check Soil Health",
        "agro_assist": "AgroAssist: Your Smart Farming Assistant",
        "Give_Feedback": "We Value Your Feedback!",
        "follow_us": "Follow Us",
        "help_faqs": "Help & FAQs",
        "learn_more": "Learn More About Smart Farming",
    },
    "Español": {
        "weather_forecast": "Pronóstico del Tiempo",
        "enter_location": "Ingresa tu ubicación",
        "recommended_crops": "Cultivos Recomendados para",
        "spraying_advisory": "Consejos de Pulverización para",
        "chat_with_agrobot": "Chatea con AgroBot",
        "soil_health_monitoring": "Monitoreo de Salud del Suelo",
        "check_soil_health": "Verificar Salud del Suelo",
        "agro_assist": "AgroAssist: Tu Asistente Agrícola Inteligente",
        "Give_Feedback": "¡Valoramos Tu Opinión!",
        "follow_us": "Síguenos",
        "help_faqs": "Ayuda y Preguntas Frecuentes",
        "learn_more": "Aprende Más Sobre Agricultura Inteligente",
    },
    "Français": {
        "weather_forecast": "Prévisions Météorologiques",
        "enter_location": "Entrez votre emplacement",
        "recommended_crops": "Cultures Recommandées pour",
        "spraying_advisory": "Conseil de Pulvérisation pour",
        "chat_with_agrobot": "Discuter avec AgroBot",
        "soil_health_monitoring": "Surveillance de la Santé du Sol",
        "check_soil_health": "Vérifier la Santé du Sol",
        "agro_assist": "AgroAssist: Votre Assistant Agricole Intelligent",
        "Give_Feedback": "Nous Valorisons Vos Retours!",
        "follow_us": "Suivez-nous",
        "help_faqs": "Aide & FAQ",
        "learn_more": "En Savoir Plus Sur l'Agriculture Intelligente",
    },
    "اردو": {
        "weather_forecast": "موسمی پیش گوئی",
        "enter_location": "اپنی جگہ درج کریں",
        "recommended_crops": "کیلیے تجویز کردہ فصلیں",
        "spraying_advisory": "کے لیے چھڑکاؤ کی مشاورت",
        "chat_with_agrobot": "ایگرو بوٹ سے بات چیت کریں",
        "soil_health_monitoring": "زمین کی صحت کی نگرانی",
        "check_soil_health": "زمین کی صحت چیک کریں",
        "agro_assist": "ایگرو اسسٹ: آپ کا ذہین زرعی معاون",
        "Give_Feedback": "ہم آپ کی رائے کی قدر کرتے ہیں!",
        "follow_us": "ہمارا ساتھ دیں",
        "help_faqs": "مدد اور اکثر پوچھے جانے والے سوالات",
        "learn_more": "ذہین زراعت کے بارے میں مزید جانیں",
    },
    "Deutsch": {
        "weather_forecast": "Wettervorhersage",
        "enter_location": "Geben Sie Ihren Standort ein",
        "recommended_crops": "Empfohlene Pflanzen für",
        "spraying_advisory": "Sprühberatung für",
        "chat_with_agrobot": "Chatte mit AgroBot",
        "soil_health_monitoring": "Boden Gesundheitsüberwachung",
        "check_soil_health": "Boden Gesundheit überprüfen",
        "agro_assist": "AgroAssist: Ihr intelligenter Landwirtschaftsassistent",
        "Give_Feedback": "Wir schätzen Ihr Feedback!",
        "follow_us": "Folgen Sie uns",
        "help_faqs": "Hilfe & FAQs",
        "learn_more": "Erfahren Sie mehr über intelligente Landwirtschaft",
    },
    "中文": {
        "weather_forecast": "天气预报",
        "enter_location": "输入您的位置",
        "recommended_crops": "推荐的作物",
        "spraying_advisory": "喷洒建议",
        "chat_with_agrobot": "与AgroBot聊天",
        "soil_health_monitoring": "土壤健康监测",
        "check_soil_health": "检查土壤健康",
        "agro_assist": "AgroAssist：您的智能农业助手",
        "Give_Feedback": "我们重视您的反馈!",
        "follow_us": "关注我们",
        "help_faqs": "帮助与常见问题",
        "learn_more": "了解更多关于智能农业的信息",
    },
    "العربية": {
        "weather_forecast": "توقعات الطقس",
        "enter_location": "أدخل موقعك",
        "recommended_crops": "المحاصيل الموصى بها لـ",
        "spraying_advisory": "نصيحة الرش لـ",
        "chat_with_agrobot": "الدردشة مع AgroBot",
        "soil_health_monitoring": "مراقبة صحة التربة",
        "check_soil_health": "تحقق من صحة التربة",
        "agro_assist": "AgroAssist: مساعدك الزراعي الذكي",
        "Give_Feedback": "نحن نقدر ملاحظاتك!",
        "follow_us": "تابعنا",
        "help_faqs": "المساعدة والأسئلة الشائعة",
        "learn_more": "تعلم المزيد عن الزراعة الذكية",
    },
    "Русский": {
        "weather_forecast": "Прогноз погоды",
        "enter_location": "Введите ваше местоположение",
        "recommended_crops": "Рекомендуемые культуры для",
        "spraying_advisory": "Совет по распылению для",
        "chat_with_agrobot": "Поговорите с AgroBot",
        "soil_health_monitoring": "Мониторинг здоровья почвы",
        "check_soil_health": "Проверить здоровье почвы",
        "agro_assist": "AgroAssist: Ваш умный сельскохозяйственный помощник",
        "Give_Feedback": "Мы ценим ваш отзыв!",
        "follow_us": "Следите за нами",
        "help_faqs": "Помощь и часто задаваемые вопросы",
        "learn_more": "Узнайте больше о смарт-фермерстве",
    },
}

# Set translations based on selected language
selected_lang = translations[language]

# Weather Forecast Feature
def get_weather_data(location):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={weather_api_key}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return {'message': response.json().get('message', 'Unknown error occurred')}
    
    return response.json()

# Sidebar for weather forecast input
st.sidebar.subheader(selected_lang["weather_forecast"])
location = st.sidebar.text_input(selected_lang["enter_location"], placeholder="e.g., City, State")
if location:
    weather_data = get_weather_data(location)
    if 'list' in weather_data:
        st.subheader(f"{selected_lang['weather_forecast']} in {location}")
        for forecast in weather_data['list'][:10]:  # Show next 5 forecasts
            st.write(f"{forecast['dt_txt']} - {forecast['main']['temp']}°C, {forecast['weather'][0]['description']}")
    else:
        if 'message' in weather_data:
            st.error(f"Error: {weather_data['message']}")
        else:
            st.error("Error fetching weather data. Please check the location or API key.")

# Crop Recommendation System
st.sidebar.subheader(selected_lang["recommended_crops"])

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
        max_tokens=100,
    )

    message = response.choices[0].message.content
    st.subheader(f"{selected_lang['recommended_crops']} {region}")
    st.write(message)

# Spraying Advisory System
st.sidebar.subheader(selected_lang["spraying_advisory"])
crop = st.sidebar.text_input("Enter your crop type", placeholder="e.g., Wheat, Rice")
if crop:
    response = client.chat.completions.create(
        model="o1-mini",
        messages=[{"role": "user", "content": f"What is the spraying schedule for {crop}?"}],
        max_tokens=100,
    )

    message = response.choices[0].message.content
    st.subheader(f"{selected_lang['spraying_advisory']} {crop}")
    st.write(message)

# Multilingual Chatbot
st.sidebar.subheader(selected_lang["chat_with_agrobot"])
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
st.sidebar.subheader(selected_lang["soil_health_monitoring"])

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
if st.sidebar.button(selected_lang["check_soil_health"]):
    # Make an API call to assess soil health based on multiple factors
    response = client.chat.completions.create(
        model="o1-mini",
        messages=[{
            "role": "user", 
            "content": f"Assess soil health with pH level {ph_level}, moisture {moisture}%, temperature {temperature}°C, Nitrogen (N) {nitrogen} ppm, Phosphorus (P) {phosphorus} ppm, Potassium (K) {potassium} ppm, organic matter {organic_matter}%, and compaction {compaction} g/cm³."
        }],
        max_tokens=100,
    )

    message = response.choices[0].message.content
    st.subheader(f"{selected_lang['soil_health_monitoring']}")
    st.write(message)


# Follow us and Help & FAQs Section
# Follow Us Section
st.sidebar.subheader(selected_lang["follow_us"])
st.sidebar.markdown("[Twitter](https://twitter.com/AgroAssist)")
st.sidebar.markdown("[Linkedin](https://www.linkedin.com/in/danishmustafa86/)")
st.sidebar.markdown("[Facebook](https://facebook.com/AgroAssist)")

# # Help & FAQs Section
# st.sidebar.subheader(selected_lang["help_faqs"])
# st.sidebar.markdown("[Help & FAQs](#)")

# Learn More Section
st.sidebar.subheader(selected_lang["learn_more"])
st.sidebar.markdown("[https://www.cropin.com/smart-farming](#)")

# Give Feedback Section
st.sidebar.subheader(selected_lang["Give_Feedback"])
st.sidebar.markdown("[Provide Feedback](https://docs.google.com/forms/d/1VXQ1dd6p_SFwjuWkTcqtZ1-A5O1M-FdyktcwTYXX5ig/edit?usp=forms_home&ths=true)")
