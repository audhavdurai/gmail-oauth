from flask import Flask, request, redirect, url_for, render_template, session
from requests_oauthlib import OAuth2Session
import imaplib
from dotenv import load_dotenv
import os
from email.parser import BytesParser
from bs4 import BeautifulSoup
from email import policy
import re
import requests


def remove_links(text):
    pattern = r'https?://\S+|www\.\S+'
    
    clean_text = re.sub(pattern, '', text)
    
    return clean_text

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
authorization_base_url = os.getenv('AUTHORIZATION_BASE_URL')
token_url = os.getenv('TOKEN_URL')
scope = os.getenv('SCOPE').split(',')

app = Flask(__name__)
app.secret_key = "secret"

google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

@app.route('/callback/')
def callback():
    full_url = request.url

    redirect_response = full_url.replace('http://', 'https://', 1)
        
    token = google.fetch_token(token_url, client_secret=client_secret, 
                            authorization_response=redirect_response)

    session["refresh_token"] = token['refresh_token']

    r = google.get('https://www.googleapis.com/oauth2/v1/userinfo')
    email = r.json()['email']

    session["email"] = email

    return redirect(url_for('home'))

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    if "refresh_token" in session and "email" in session:
        def get_access_token_from_refresh(refresh_token, client_id, client_secret):
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'client_id': client_id,
                'client_secret': client_secret
            }
            response = requests.post(token_url, data=data)
            return response.json().get('access_token')
    
        access_token = get_access_token_from_refresh(session["refresh_token"], client_id, client_secret)

        def xoauth_authenticate(email, access_token):
            def _auth(*args, **kwargs):
                return 'user=%s\1auth=Bearer %s\1\1' % (email, access_token)
            return 'XOAUTH2', _auth

        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.authenticate(*xoauth_authenticate(session["email"], access_token))

        mail.select('inbox')

        x = 10

        latest_id = mail.search(None, 'ALL')[1][0].split()[-1]

        fin_string = ""

        for email in mail.search(None, 'ALL')[1][0].split()[-x:]:
            ret_string = ""
            latest_id = email
            raw = mail.fetch(latest_id, "(RFC822)")[1][0][1]

            email_message = BytesParser(policy=policy.default).parsebytes(raw)

            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain":
                    ret_string += part.get_payload(decode=True).decode(part.get_content_charset())

                elif content_type == "text/html":
                    html_string = part.get_payload(decode=True).decode(part.get_content_charset())

                    soup = BeautifulSoup(html_string, 'html.parser')
                    text = soup.get_text()
                    ret_string += text + "\n"

                elif "attachment" in content_disposition:
                    filename = part.get_filename()

            fin_string += remove_links(ret_string)
        
        return str((float(len(fin_string))/4.0) * (0.0010/1000.0))

    authorization_url, state = google.authorization_url(authorization_base_url,
        access_type="offline", approval_prompt="force")

    link = str(authorization_url)

    return render_template("index.html", link=link)

if __name__ == '__main__':
    app.run(debug=True)