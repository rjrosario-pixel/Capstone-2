import re
import socket
from urllib.parse import urlparse
import requests
from datetime import datetime

# Helper: Check if the URL has an IP address
def url_having_ip(url):
    try:
        ip = socket.gethostbyname(urlparse(url).hostname)
        if re.match(r"\d+\.\d+\.\d+\.\d+", ip):
            return 1
    except:
        return -1
    return -1

def url_length(url):
    return 1 if len(url) >= 75 else -1

def url_short(url):
    shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|yfrog\.com|migre\.me|ff\.im|tiny\.cc"
    return 1 if re.search(shortening_services, url) else -1

def having_at_symbol(url):
    return 1 if "@" in url else -1

def doubleSlash(url):
    return 1 if url.rfind('//') > 6 else -1

def prefix_suffix(url):
    domain = urlparse(url).netloc
    return 1 if '-' in domain else -1

def sub_domain(url):
    domain = urlparse(url).netloc
    if domain.count('.') > 2:
        return 1
    else:
        return -1

def SSLfinal_State(url):
    try:
        if url.startswith("https"):
            return -1
    except:
        pass
    return 1

def domain_registration(url):
    return -1  # Placeholder for whois query (domain age)

def favicon(url):
    return -1  # Placeholder

def port(url):
    return -1  # Placeholder, assume normal port

def https_token(url):
    domain = urlparse(url).netloc
    return 1 if 'https' in domain else -1

def request_url(url):
    return -1  # Placeholder

def url_of_anchor(url):
    return -1  # Placeholder

def Links_in_tags(url):
    return -1  # Placeholder

def sfh(url):
    return -1  # Placeholder

def email_submit(url):
    return -1  # Placeholder

def abnormal_url(url):
    return -1  # Placeholder

def redirect(url):
    return 1 if url.count('//') > 1 else -1

def on_mouseover(url):
    return -1  # Placeholder

def rightClick(url):
    return -1  # Placeholder

def popup(url):
    return -1  # Placeholder

def iframe(url):
    return -1  # Placeholder

def age_of_domain(url):
    return -1  # Placeholder

def check_dns(url):
    try:
        socket.gethostbyname(urlparse(url).hostname)
        return -1
    except:
        return 1

def web_traffic(url):
    return -1  # Placeholder

def page_rank(url):
    return -1  # Placeholder

def google_index(url):
    return -1  # Placeholder

def links_pointing(url):
    return -1  # Placeholder

def statistical(url):
    return -1  # Placeholder

def extract_url_features(url):
    return [
        url_having_ip(url),
        url_length(url),
        url_short(url),
        having_at_symbol(url),
        doubleSlash(url),
        prefix_suffix(url),
        sub_domain(url),
        SSLfinal_State(url),
        domain_registration(url),
        favicon(url),
        port(url),
        https_token(url),
        request_url(url),
        url_of_anchor(url),
        Links_in_tags(url),
        sfh(url),
        email_submit(url),
        abnormal_url(url),
        redirect(url),
        on_mouseover(url),
        rightClick(url),
        popup(url),
        iframe(url),
        age_of_domain(url),
        check_dns(url),
        web_traffic(url),
        page_rank(url),
        google_index(url),
        links_pointing(url),
        statistical(url)
    ]
