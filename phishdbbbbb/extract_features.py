import csv
import tldextract
import ipaddress
import urllib.parse
import re
from datetime import datetime

# ---------- FEATURE EXTRACTION FUNCTIONS ----------
def has_ip(url):
    try:
        hostname = urllib.parse.urlparse(url).hostname
        ipaddress.ip_address(hostname)
        return 1
    except:
        return 0

def url_length(url):
    return len(url)

def has_at_symbol(url):
    return 1 if '@' in url else 0

def count_subdomains(url):
    extracted = tldextract.extract(url)
    return extracted.subdomain.count('.') + 1 if extracted.subdomain else 0

def uses_https(url):
    return 1 if urllib.parse.urlparse(url).scheme == 'https' else 0

def has_suspicious_words(url):
    suspicious_keywords = ['secure', 'account', 'webscr', 'login', 'signin', 'banking']
    return int(any(word in url.lower() for word in suspicious_keywords))

def count_digits(url):
    return sum(c.isdigit() for c in url)

def count_special_chars(url):
    return len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', url))

# ---------- LOAD URLS AND CREATE FEATURES ----------
def extract_features_from_urls(phishing_file, safe_file, output_file):
    print("Generating phishing_dataset.csv...")
    with open(output_file, 'w', newline='', encoding='utf-8') as out_csv:
        writer = csv.writer(out_csv)
        header = [
            'url', 'url_length', 'has_ip', 'has_at_symbol', 'num_subdomains',
            'uses_https', 'has_suspicious_words', 'num_digits', 'num_special_chars', 'Result'
        ]
        writer.writerow(header)

        def process_file(filename, label):
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    url = line.strip()
                    if not url:
                        continue
                    features = [
                        url,
                        url_length(url),
                        has_ip(url),
                        has_at_symbol(url),
                        count_subdomains(url),
                        uses_https(url),
                        has_suspicious_words(url),
                        count_digits(url),
                        count_special_chars(url),
                        label
                    ]
                    writer.writerow(features)

        process_file(phishing_file, 1)   # phishing URLs → 1
        process_file(safe_file, -1)      # safe URLs → -1

    print(f"✅ Done! Dataset saved as {output_file}")

# ---------- USAGE EXAMPLE ----------
if __name__ == '__main__':
    extract_features_from_urls('github_phishing.txt', 'safe_links.txt', 'phishing_dataset.csv')
