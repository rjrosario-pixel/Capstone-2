from flask import Flask, request, jsonify, render_template
import re
from urllib.parse import urlparse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# === Feature extractor ===
def extract_url_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    features = {
        'url_length': len(url),
        'count_dots': domain.count('.'),
        'has_ip': 1 if re.search(r'(\d{1,3}\.){3}\d{1,3}', domain) else 0,
        'count_at': url.count('@'),
        'count_hyphen': domain.count('-'),
        'count_question': url.count('?'),
        'count_equal': url.count('='),
        'count_double_slash': url[8:].count('//'),
        'https': 1 if parsed.scheme == 'https' else 0,
        'domain_length': len(domain),
        'subdomain_count': domain.count('.') - 1 if domain.count('.') > 1 else 0,
        'suspicious_words': int(any(word in url.lower() for word in ['login', 'signin', 'bank', 'update', 'free', 'lucky', 'bonus', 'account']))
    }
    return features

# === Dummy Model Training ===
def train_dummy_model():
    data = [
        [50, 2, 0, 0, 1, 0, 0, 0, 1, 15, 1, 0, 0],  # legit
        [90, 4, 1, 1, 3, 2, 1, 1, 0, 25, 3, 1, 1],  # phishing
        [45, 1, 0, 0, 0, 0, 0, 0, 1, 10, 0, 0, 0],  # legit
        [100, 5, 1, 2, 4, 3, 2, 2, 0, 30, 4, 1, 1]  # phishing
    ]
    df = pd.DataFrame(data, columns=[
        'url_length', 'count_dots', 'has_ip', 'count_at', 'count_hyphen',
        'count_question', 'count_equal', 'count_double_slash', 'https',
        'domain_length', 'subdomain_count', 'suspicious_words', 'label'
    ])
    X = df.drop('label', axis=1)
    y = df['label']
    model = RandomForestClassifier()
    model.fit(X, y)
    return model

model = train_dummy_model()

# === Routes ===
@app.route('/')
def home():
    return render_template('Scanner.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url', '')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    features = extract_url_features(url)
    feature_order = ['url_length', 'count_dots', 'has_ip', 'count_at', 'count_hyphen',
                     'count_question', 'count_equal', 'count_double_slash', 'https',
                     'domain_length', 'subdomain_count', 'suspicious_words']
    
    X = pd.DataFrame([features], columns=feature_order)
    prediction = model.predict(X)[0]
    label = 'Phishing' if prediction == 1 else 'Legitimate'
    return jsonify({'result': label})

if __name__ == '__main__':
    app.run(debug=True)
