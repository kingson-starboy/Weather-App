from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route("/")
def home():
    city = request.args.get("city", "").strip()

    # Default values
    weather = {
        "temp": "N/A",
        "condition": "N/A",
        "humidity": "N/A",
        "wind": "N/A",
        "feels_like": "N/A"
    }

    if city:
        try:
            url = f"https://wttr.in/{city}?format=j1"
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            data = response.json()
            current = data["current_condition"][0]

            weather["temp"] = current["temp_C"]
            weather["condition"] = current["weatherDesc"][0]["value"]
            weather["humidity"] = current["humidity"]
            weather["wind"] = current["windspeedKmph"]
            weather["feels_like"] = current["FeelsLikeC"]

        except requests.RequestException:
            weather["condition"] = "Unable to fetch weather"

    return render_template(
        "index.html",
        city=city,
        **weather
    )

if __name__ == "__main__":
    app.run(debug=True)