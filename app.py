from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

def get_weather(city):
    try:
        url = f"https://wttr.in/pune?format=j1"
        response = requests.get(url)
        data = response.json()

        current_condition = data['current_condition'][0]
        temp_C = float(current_condition['temp_C'])
        weather_desc = current_condition['weatherDesc'][0]['value']

        weather_string = f"{weather_desc}, {temp_C}°C"
        return weather_string, temp_C
    except Exception as e:
        print("Error fetching weather:", e)
        return None, None

def suggest_outfit(temp):
    if temp is None:
        return "❌ Sorry, could not get weather data. Try again."
    elif temp >= 30:
        return "☀️ It's hot! Go for cotton clothes, shorts, and sunglasses."
    elif 20 <= temp < 30:
        return "🌤️ Mild weather! A t-shirt and jeans or a comfy dress works well."
    elif 10 <= temp < 20:
        return "🌥️ It's a bit cool! Try layering with a hoodie or light jacket."
    else:
        return "❄️ Cold weather! Wear a coat, scarf, gloves, and boots."

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/weather", methods=["POST"])
def weather():
    city = request.form.get("city")
    weather_desc, temp = get_weather(city)
    outfit = suggest_outfit(temp)
    return render_template("index.html", weather=weather_desc, outfit=outfit)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

