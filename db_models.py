from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# User accounts
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    phishing_urls = db.relationship('PhishingURL', backref='user', lazy=True)
    safe_urls = db.relationship('SafeURL', backref='safe_user', lazy=True)  # ✅ changed backref name
# URLs submitted by users for scanning
class PhishingURL(db.Model):
    __tablename__ = 'phishing_urls'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False, unique=True)
    domain = db.Column(db.String)
    result = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# Blacklisted URLs from PhishTank or GitHub
class BlacklistURL(db.Model):
    __tablename__ = 'blacklist_urls'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False, unique=True)
    domain = db.Column(db.String)
    source = db.Column(db.String)  # 'PhishTank' or 'GitHub'
    added_on = db.Column(db.DateTime, default=datetime.utcnow)

# Safe URLs submitted or imported
class SafeURL(db.Model):
    __tablename__ = 'safe_urls'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False, unique=True)
    added_on = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class BlacklistIP(db.Model):
    __tablename__ = 'blacklist_ips'
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String, unique=True, nullable=False)
    source = db.Column(db.String, default='GitHub')
    added_on = db.Column(db.DateTime, default=datetime.utcnow)


class BlacklistDomain(db.Model):
    __tablename__ = 'blacklist_domains'
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String, unique=True, nullable=False)
    source = db.Column(db.String, default='GitHub')
    added_on = db.Column(db.DateTime, default=datetime.utcnow)
