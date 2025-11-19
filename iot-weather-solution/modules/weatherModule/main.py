import ntplib
import requests
import json
import asyncio
from datetime import datetime
from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import Message


# ───────────────────────────────────────────────
# 1. GET NTP TIME
# ───────────────────────────────────────────────
def get_ntp_time():
    servers = [
        "pool.ntp.org",
        "time.google.com",
        "time.windows.com",
        "time.apple.com",
        "time.cloudflare.com"
    ]
    client = ntplib.NTPClient()

    for server in servers:
        try:
            response = client.request(server, version=3, timeout=2)
            return datetime.fromtimestamp(response.tx_time).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        except Exception:
            pass

    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')


# ───────────────────────────────────────────────
# 2. WEATHER API
# ───────────────────────────────────────────────
API_KEY = "6434ee1ebdd04dcf2f07348d28351e10"
CITIES = ["Casablanca", "Rabat", "Marrakech", "Tangier", "Agadir","Fes"]   # ← MULTI-VILLES


def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[Weather] Error for city {city}: {e}")
        return None


# ───────────────────────────────────────────────
# 3. MAIN LOOP (IoT Edge)
# ───────────────────────────────────────────────
async def main():
    print("🟩 Starting IoT Edge Weather Module...")

    client = IoTHubModuleClient.create_from_edge_environment()

    await client.connect()
    print("🟢 Connected to EdgeHub")

    while True:
        try:
            ntp_time = get_ntp_time()

            for city in CITIES:
                weather = get_weather(city)

                if weather is None:
                    continue

                data = {
                    "timestamp": ntp_time,
                    "temperature": round(weather["main"]["temp"], 2),
                    "humidity": weather["main"]["humidity"],
                    "wind_speed": round(weather["wind"]["speed"], 2),
                    "wind_direction": weather["wind"]["deg"],
                    "city": city,
                    "source": "edge-weather-module"
                }

                msg = Message(json.dumps(data))
                msg.content_type = "application/json"
                msg.content_encoding = "utf-8"

                await client.send_message_to_output(msg, "output1")
                print(f"📡 Sent → {city} |||||||||| Temp {data['temperature']}°C")

            await asyncio.sleep(30)

        except Exception as e:
            print(f"⚠ Error in loop: {e}")
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
