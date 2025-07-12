def extract_features(url):
    # Example: basic dummy feature extraction
    features = []
    features.append(len(url))                 # Length of URL
    features.append(url.count('.'))           # Count of dots
    features.append(int('https' in url))      # HTTPS flag
    features.append(int('login' in url))      # Common phishing keyword
    # Add more features as needed
    return features
