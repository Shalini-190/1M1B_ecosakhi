import requests
from bs4 import BeautifulSoup

def get_karnataka_sldc_solar_data():
    url = "https://kptclsldc.in/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        lines = soup.get_text(separator="\n").splitlines()
        solar_lines = [line.strip() for line in lines if "solar" in line.lower() and line.strip()]

        if not solar_lines:
            return "❌ No live solar data found."
        return "\n".join(solar_lines[:5])
    except Exception as e:
        return f"❌ Error: {str(e)}"

print(get_karnataka_sldc_solar_data())
