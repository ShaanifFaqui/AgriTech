from flask import Blueprint, render_template, request, render_template_string
import joblib
import numpy as np
import os

crop_recommendation_bp = Blueprint('crop_recommendation', __name__, template_folder='templates', static_folder='static', url_prefix='/crop-recommendation')

# Get the absolute path to the model directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    model = joblib.load(os.path.join(BASE_DIR, 'model', 'rf_model.pkl'))
    label_encoder = joblib.load(os.path.join(BASE_DIR, 'model', 'label_encoder.pkl'))
    print("Crop Recommendation models loaded successfully")
except FileNotFoundError as e:
    print(f"Warning: Crop Recommendation model files not found: {e}")
    print("Crop Recommendation functionality will be limited.")
    model = None
    label_encoder = None

@crop_recommendation_bp.route('/')
def home():
    print("Crop Recommendation route accessed - rendering Crop Recommendation page")
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Crop Recommendation | AgriTech</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background: green;;
                min-height: 100vh;
                color: #333;
                margin: 0;
            }
            .container {
                max-width: 500px;
                margin: 40px auto 0 auto;
                background: #fff;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.10);
                padding: 36px 32px 32px 32px;
            }
            .header {
                text-align: center;
                margin-bottom: 24px;
            }
            .header h1 {
                font-size: 2.2rem;
                color: #667eea;
                margin-bottom: 10px;
                font-weight: 700;
            }
            .header p {
                color: #555;
                font-size: 1.1rem;
            }
            form {
                display: flex;
                flex-direction: column;
                gap: 18px;
            }
            .input-group {
                display: flex;
                align-items: center;
                gap: 12px;
                background: #f7fafc;
                border-radius: 10px;
                padding: 10px 14px;
                box-shadow: 0 2px 8px rgba(102,126,234,0.04);
            }
            .input-group i {
                color: #667eea;
                font-size: 1.2rem;
                min-width: 22px;
            }
            label {
                font-weight: 600;
                color: #667eea;
                font-size: 1rem;
                min-width: 120px;
            }
            input[type="number"] {
                flex: 1;
                padding: 10px 12px;
                border: 1px solid #b2bec3;
                border-radius: 8px;
                font-size: 1rem;
                outline: none;
                background: #fff;
                transition: border 0.2s;
            }
            input[type="number"]:focus {
                border: 1.5px solid #667eea;
            }
            button {
                margin-top: 10px;
                padding: 14px 0;
                background: linear-gradient(90deg, #667eea, #764ba2);
                color: #fff;
                border: none;
                border-radius: 10px;
                font-size: 1.15rem;
                font-weight: 700;
                cursor: pointer;
                box-shadow: 0 4px 16px rgba(102,126,234,0.13);
                transition: background 0.2s, transform 0.2s;
                letter-spacing: 1px;
            }
            button:hover {
                background: linear-gradient(90deg, #764ba2, #667eea);
                transform: translateY(-2px) scale(1.03);
            }
            .how-it-works {
                background: rgba(102,126,234,0.08);
                border-radius: 16px;
                margin-top: 36px;
                padding: 24px 18px;
            }
            .how-it-works h2 {
                color: #764ba2;
                font-size: 1.2rem;
                margin-bottom: 16px;
                text-align: center;
                font-weight: 700;
            }
            .how-it-works ul {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            .how-it-works li {
                margin-bottom: 10px;
                padding-left: 22px;
                position: relative;
                color: #444;
                font-size: 1rem;
            }
            .how-it-works li:before {
                content: '\\2714';
                position: absolute;
                left: 0;
                color: #43cea2;
                font-weight: bold;
            }
            .footer {
                text-align: center;
                color: #888;
                margin-top: 32px;
                font-size: 0.98rem;
                opacity: 0.85;
            }
            @media (max-width: 600px) {
                .container {
                    padding: 18px 6px 14px 6px;
                }
                .header h1 {
                    font-size: 1.5rem;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1><i class="fas fa-leaf"></i> Crop Recommendation</h1>
                <p>Get AI-powered crop suggestions based on soil nutrients, climate, and environment.</p>
            </div>
            <form method="post" action="/crop-recommendation/predict">
                <div class="input-group">
                    <i class="fas fa-flask"></i>
                    <label for="N">Nitrogen (N)</label>
                    <input type="number" step="any" name="N" id="N" required placeholder="e.g. 90">
                </div>
                <div class="input-group">
                    <i class="fas fa-flask"></i>
                    <label for="P">Phosphorus (P)</label>
                    <input type="number" step="any" name="P" id="P" required placeholder="e.g. 42">
                </div>
                <div class="input-group">
                    <i class="fas fa-flask"></i>
                    <label for="K">Potassium (K)</label>
                    <input type="number" step="any" name="K" id="K" required placeholder="e.g. 43">
                </div>
                <div class="input-group">
                    <i class="fas fa-thermometer-half"></i>
                    <label for="temperature">Temperature (°C)</label>
                    <input type="number" step="any" name="temperature" id="temperature" required placeholder="e.g. 22.5">
                </div>
                <div class="input-group">
                    <i class="fas fa-tint"></i>
                    <label for="humidity">Humidity (%)</label>
                    <input type="number" step="any" name="humidity" id="humidity" required placeholder="e.g. 80">
                </div>
                <div class="input-group">
                    <i class="fas fa-vial"></i>
                    <label for="ph">pH</label>
                    <input type="number" step="any" name="ph" id="ph" required placeholder="e.g. 6.5">
                </div>
                <div class="input-group">
                    <i class="fas fa-cloud-rain"></i>
                    <label for="rainfall">Rainfall (mm)</label>
                    <input type="number" step="any" name="rainfall" id="rainfall" required placeholder="e.g. 200">
                </div>
                <button type="submit"><i class="fas fa-seedling"></i> Get Recommendation</button>
            </form>
            <div class="how-it-works">
                <h2>How It Works</h2>
                <ul>
                    <li>Input your soil nutrient levels (N, P, K)</li>
                    <li>Provide temperature, humidity, pH, and rainfall data</li>
                    <li>Our AI model analyzes your data</li>
                    <li>Receive crop recommendations instantly</li>
                </ul>
            </div>
        </div>
        <div class="footer">
            &copy; 2024 AgriTech - Crop Recommendation
        </div>
    </body>
    </html>
    ''')

@crop_recommendation_bp.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return render_template('error.html', message='Crop Recommendation model is not available. Please ensure the model files are present.'), 503
    try:
        data = [
            float(request.form['N']),
            float(request.form['P']),
            float(request.form['K']),
            float(request.form['temperature']),
            float(request.form['humidity']),
            float(request.form['ph']),
            float(request.form['rainfall'])
        ]
        prediction_num = model.predict([data])[0]
        prediction_label = label_encoder.inverse_transform([prediction_num])[0]
        # Render a simple, modern result page directly for clarity
        return render_template_string(f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Crop Recommendation Result | AgriTech</title>
                <link href="https://fonts.googleapis.com/css2?family=Inter:wght@600&display=swap" rel="stylesheet">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
                <style>
                    body {{
                        font-family: 'Inter', sans-serif;
                        background: green;;
                        min-height: 100vh;
                        color: #333;
                        margin: 0;
                    }}
                    .result-container {{
                        max-width: 420px;
                        margin: 80px auto;
                        background: #fff;
                        border-radius: 18px;
                        box-shadow: 0 8px 32px rgba(24,90,157,0.18);
                        padding: 36px 32px 32px 32px;
                        text-align: center;
                    }}
                    .result-container h2 {{
                        color: #667eea;
                        font-size: 2rem;
                        margin-bottom: 18px;
                    }}
                    .result-container .icon {{
                        font-size: 3rem;
                        color: #764ba2;
                        margin-bottom: 16px;
                    }}
                    .result-container .crop {{
                        font-size: 1.5rem;
                        color: #185a9d;
                        font-weight: 700;
                        margin-bottom: 12px;
                    }}
                    .back-btn {{
                        display: inline-block;
                        margin-top: 24px;
                        padding: 10px 24px;
                        background: linear-gradient(90deg, #667eea, #764ba2);
                        color: #fff;
                        border: none;
                        border-radius: 8px;
                        font-size: 1rem;
                        font-weight: 600;
                        text-decoration: none;
                        transition: background 0.2s;
                    }}
                    .back-btn:hover {{
                        background: linear-gradient(90deg, #764ba2, #667eea);
                    }}
                </style>
            </head>
            <body>
                <div class="result-container">
                    <div class="icon"><i class="fas fa-seedling"></i></div>
                    <h2>Recommended Crop</h2>
                    <div class="crop">{prediction_label}</div>
                    <a href="/crop-recommendation/" class="back-btn"><i class="fas fa-arrow-left"></i> Try Again</a>
                </div>
            </body>
            </html>
        ''')
    except Exception as e:
        return render_template('error.html', message=f'Prediction error: {e}'), 500