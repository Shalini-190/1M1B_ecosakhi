import requests
from bs4 import BeautifulSoup

def get_monthly_solar_generation():
    url = "https://npp.gov.in/public-reports/cea/monthly/generation/17_16_INDIA_2024_Apr.html"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("tr")
        for row in rows:
            if "Solar Energy" in row.text:
                cols = row.find_all("td")
                if len(cols) > 5:
                    return (
                        f"📅 <b>Monthly Solar Report (NPP)</b><br>"
                        f"🔆 Source: {cols[0].text.strip()}<br>"
                        f"📊 Target: <b>{cols[4].text.strip()} MU</b><br>"
                        f"⚡ Actual: <b>{cols[5].text.strip()} MU</b>"
                    )
        return "⚠️ Could not extract solar data from NPP."
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_karnataka_sldc_solar_data():
    # Live site is JavaScript-rendered, so we give user a friendly message and link
    return (
        "🔆 <b>Karnataka SLDC - Live Solar Data</b><br>"
        "📡 This data is shown in dynamic charts that can't be scraped directly.<br>"
        "🖥 <a href='https://kptclsldc.in/' target='_blank'>Click here to view the live dashboard →</a>"
    )
