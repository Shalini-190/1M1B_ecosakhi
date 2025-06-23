from flask import Flask, request, jsonify, render_template
from flask import Flask, jsonify
from flask_cors import CORS
import json
import re
import random
import traceback
from thefuzz import process as fuzz_process
import webbrowser
import threading
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from .solar_data import get_monthly_solar_generation, get_karnataka_sldc_solar_data
import os

app = Flask(__name__)
CORS(app)

@app.route("/solar-monthly", methods=["GET"])
def solar_monthly():
    result = get_monthly_solar_generation()
    return jsonify({"type": "answer", "content": result})

@app.route("/solar-live", methods=["GET"])
def solar_live():
    result = get_karnataka_sldc_solar_data()
    return jsonify({"type": "answer", "content": result})


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, 'knowledge_base.json'), 'r', encoding='utf-8') as f:

def get_best_match(query, choices, threshold=80):
    best_match = fuzz_process.extractOne(query, choices)
    return best_match[0] if best_match and best_match[1] >= threshold else None

def get_energy_tip():
    tips = knowledge_base.get('energy_saving_tips', [])
    return f"💡 <b>Energy Saving Tip</b>:<br><ul><li>{random.choice(tips)}</li></ul>" if tips else "No tips available."

def get_quiz_question():
    quiz_questions = knowledge_base.get('quiz_questions', [])
    q = random.choice(quiz_questions)
    return {'type': 'quiz', 'content': {'question': q['question'], 'options': q['options'], 'correct': q['options'].index(q['correct_answer'])}}

def get_realtime_data_info(message):
    state_match = re.search(r'in ([\w\s]+)', message)
    state = state_match.group(1).strip().title() if state_match else None

    energy_type = "power"
    if "wind" in message: energy_type = "wind"
    elif "solar" in message: energy_type = "solar"
    elif "hydro" in message: energy_type = "hydro"

    sldc_links = {
        "Tamil Nadu": "https://www.tnsldc.in/",
        "Karnataka": "https://kptclsldc.in/",
        "Maharashtra": "https://www.mahasldc.in/",
        "Gujarat": "https://www.sldcguj.com/",
        "Rajasthan": "https://www.rvpn.co.in/rvpn/s/sldc-raj"
    }
    
    response_text = f"""
    <p>I cannot provide exact real-time {energy_type} generation data directly. This information is highly dynamic and is best accessed from official sources.</p>
    <p>Here are the best places to find this data for India:</p>
    <ol>
        <li>
            <b>National Power Portal (NPP):</b> The central hub for all Indian power data.
            <br><b>Website:</b> <a href="https://npp.gov.in/" target="_blank" rel="noopener noreferrer">https://npp.gov.in/</a>
        </li>
    """

    if state and state in sldc_links:
        response_text += f"""
        <li>
            <b>{state} Load Despatch Centre (SLDC):</b> For detailed data specific to {state}.
            <br><b>Website:</b> <a href="{sldc_links[state]}" target="_blank" rel="noopener noreferrer">{sldc_links[state]}</a>
        </li>
        """
    else:
        response_text += """
        <li>
            <b>State Load Despatch Centres (SLDC):</b> For detailed data on a specific state, you can search for "[State Name] Load Despatch Centre".
        </li>
        """
    
    response_text += "</ol><p>These portals are the direct sources and will give you the most reliable information.</p>"
    
    return {'type': 'answer', 'content': response_text}

def get_solar_radiation():
    # Simulate some data
    current_hour = datetime.now().hour
    if 6 <= current_hour <= 18:
        radiation = 750 + random.randint(-150, 150)
        cloud_cover = random.randint(0, 40)
    else:
        radiation = 0
        cloud_cover = random.randint(0, 20)

    response_html = f"""
    🌞 <b>Current Solar Radiation in Bangalore (Simulated)</b>:
    <br><br>
    📊 <b>Current Readings:</b>
    <ul>
        <li>Solar Radiation: {radiation} W/m²</li>
        <li>Cloud Coverage: {cloud_cover}%</li>
        <li>Time: {datetime.now().strftime('%I:%M %p')}</li>
    </ul>
    💡 <b>What this means:</b>
    <ul>
        <li>Optimal solar radiation is between 800-1000 W/m².</li>
        <li>Current conditions are <b>{'Good' if radiation > 700 else 'Moderate' if radiation > 400 else 'Low'}</b> for solar generation.</li>
    </ul>
    <small>
        Note: This is simulated data. For official, real-time data, please consult the official portal.
        <br>
        <a href="https://kredl.karnataka.gov.in/" target="_blank" rel="noopener noreferrer">Karnataka Renewable Energy Development Limited (KREDL)</a>
    </small>
    """
    return {'type': 'answer', 'content': response_html}

def parse_appliance_usage(message):
    appliances = {}
    lines = re.split(r'\n\s*-\s*|\s*-\s*', message)
    appliance_names = r"fan|led bulb|ac|air conditioner|geyser|washing machine|fridge|refrigerator"
    for line in lines:
        if not line.strip(): continue
        line_lower = line.lower()
        base_pattern = r'(\d+)\s*(' + appliance_names + r')s?\s+for\s+([\d\.]+)\s+hours?'
        if 'alternate day' in line_lower:
            match = re.search(base_pattern, line_lower)
            if match:
                quantity, appliance, hours_str = match.groups()
                appliances[appliance.strip()] = {'quantity': int(quantity), 'hours': float(hours_str) / 2}
        elif '24x7' in line_lower:
             match = re.search(r'(\d+)\s*(' + appliance_names + r')s?', line_lower)
             if match:
                quantity, appliance = match.groups()
                appliances[appliance.strip()] = {'quantity': int(quantity), 'hours': 24}
        else:
            match = re.search(base_pattern, line_lower)
            if match:
                quantity, appliance, hours_str = match.groups()
                appliances[appliance.strip()] = {'quantity': int(quantity), 'hours': float(hours_str)}
    if 'air conditioner' in appliances: appliances['ac'] = appliances.pop('air conditioner')
    if 'refrigerator' in appliances: appliances['fridge'] = appliances.pop('refrigerator')
    return appliances

def calculate_energy_usage(appliances):
    details = {'details': [], 'total_daily_units': 0}
    appliance_power = knowledge_base['appliance_power_watt']
    for name, data in appliances.items():
        power = appliance_power.get(name.lower())
        if power:
            units = (power * data['quantity'] * data['hours']) / 1000
            details['details'].append({'appliance': name.title(), 'units': units})
            details['total_daily_units'] += units
    return details

def get_energy_saving_suggestions(usage_details):
    suggestions = []
    sorted_details = sorted(usage_details['details'], key=lambda x: x['units'], reverse=True)
    for detail in sorted_details[:2]:
        appliance_name = detail['appliance'].lower()
        if appliance_name == 'ac': suggestions.append("Set your AC to 24-26°C for optimal savings.")
        elif appliance_name == 'geyser': suggestions.append("Consider a timer for your geyser to avoid overheating.")
        elif appliance_name == 'fridge': suggestions.append("Ensure your fridge's door seals are tight.")
    return f"<br><br>📝 <b>Personalized Suggestions:</b><br><ul>{''.join([f'<li>{s}</li>' for s in suggestions])}</ul>"

def format_energy_usage(usage_details):
    total_daily = usage_details['total_daily_units']
    output = "📝 <b>Estimated Consumption:</b><br><ul>"
    for item in usage_details['details']:
        output += f"<li>{item['appliance']}: {item['units']:.2f} units/day</li>"
    output += f"</ul><br>📊 <b>Total:</b><br>Daily: {total_daily:.2f} units<br>Monthly: {total_daily * 30:.2f} units"
    return output

def process_message(message):
    try:
        user_message = message.lower()

        real_time_keywords = ['how much', 'generate', 'real-time', 'real time', 'status', 'today']
        power_keywords = ['power', 'energy', 'wind', 'solar', 'hydro', 'electricity']
        if any(keyword in user_message for keyword in real_time_keywords) and any(keyword in user_message for keyword in power_keywords):
            return get_realtime_data_info(user_message)

        if re.search(r'(\d+\s+.*(fan|led|ac|fridge|geyser|machine))|we use:', user_message):
            appliances = parse_appliance_usage(message)
            if appliances:
                usage = calculate_energy_usage(appliances)
                response = format_energy_usage(usage)
                if "tip" in user_message or "suggest" in user_message:
                    response += get_energy_saving_suggestions(usage)
                return {'type': 'calculation', 'content': response}
        
        if "solar radiation" in user_message: return get_solar_radiation()
        if "energy saving tip" in user_message: return {'type': 'answer', 'content': get_energy_tip()}
        if "quiz" in user_message: return get_quiz_question()

        definition_qs = [q['question'] for q in knowledge_base.get('definitions', [])]
        best_match = get_best_match(user_message, definition_qs, threshold=75)
        if best_match:
            for definition in knowledge_base['definitions']:
                if definition['question'] == best_match:
                    return {'type': 'definition', 'content': definition['answer']}

        greeting_patterns = [g['pattern'] for g in knowledge_base.get('greetings', [])]
        best_match = get_best_match(user_message, greeting_patterns)
        if best_match:
            for g in knowledge_base['greetings']:
                if g['pattern'] == best_match:
                    return {'type': 'answer', 'content': random.choice(g['responses'])}

        return {'type': 'answer', 'content': "I'm sorry, I couldn't find an answer. Please try rephrasing."}
    except Exception as e:
        traceback.print_exc()
        return {'type': 'error', 'content': f"An error occurred: {e}"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    response = process_message(data.get('message', ''))
    return jsonify(response)

@app.route('/quiz-explanation', methods=['POST'])
def quiz_explanation():
    data = request.get_json()
    question_text = data.get('question', '')
    for q in knowledge_base.get('quiz_questions', []):
        if q['question'] == question_text:
            return jsonify({'explanation': q.get('explanation', 'No explanation available.')})
    return jsonify({'error': 'Question not found'}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True) 
