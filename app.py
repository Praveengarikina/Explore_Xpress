from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import re
from city_data import city_data, bus_sites, place_descriptions

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

def normalize_name(name):
    return re.sub(r'[^a-z]', '', name.lower()) if name else ''

@app.route('/')
def home():
    states = list(city_data.keys())
    return render_template('index.html', states=states)

@app.route('/famous.html')
def famous():
    return render_template('famous.html')

@app.route('/place')
def place():
    state = request.args.get('state')
    district = request.args.get('district')
    place_name = request.args.get('place')

    # Prepare image filename
    img_filename = place_name.replace(" ", "_") + ".jpg"
    img_path = os.path.join(app.static_folder, "images", img_filename)
    if not os.path.exists(img_path):
        img_filename = "sample.jpg" 

    # Normalize and find description
    normalized_key = normalize_name(place_name)
    normalized_descriptions = {
        normalize_name(k): v for k, v in place_descriptions.items()
    }
    description = normalized_descriptions.get(normalized_key, "No description available.")

    return render_template(
        'place.html',
        state=state,
        district=district,
        place=place_name,
        image_file=img_filename,
        description=description
    )

@app.route('/get_states', methods=['GET'])
def get_states():
    return jsonify({"states": list(city_data.keys())})

@app.route('/get_cities', methods=['GET'])
def get_cities():
    state = request.args.get('state')
    cities = list(city_data.get(state, {}).keys())
    return jsonify({"cities": cities})

@app.route('/get_places', methods=['GET'])
def get_places():
    state = request.args.get('state')
    city = request.args.get('city')
    places = city_data.get(state, {}).get(city, [])
    return jsonify({"places": places})

@app.route('/get_bus_site')
def get_bus_site():
    state = request.args.get('state')
    url = bus_sites.get(state, None)
    return jsonify({"url": url})

if __name__ == "__main__":
    app.run(debug=True)