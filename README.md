# gmail-oauth

### Setting Up the Flask Site with Google OAuth2

#### 1. Installation:

First, ensure you have Python installed. Then follow these steps:

- **Clone the repository** containing the Flask site code.
  
  ```bash
  git clone <repository_URL>
  cd <repository_name>
  
- Install required packages listed in the requirements.txt file using pip.
  ```bash
  pip install -r requirements.txt

#### 2. Getting API Keys from Google:
Go to the Google Developers Console:

Visit Google Developers Console.
Create a new project or select an existing one.
Set up OAuth Credentials:

In the project dashboard, navigate to the "Credentials" section.
Click "Create Credentials" and select "OAuth client ID".
Choose "Web application" as the application type.
Add your site's URL (e.g., http://localhost:5000) to the Authorized Redirect URIs.

Get Client ID and Secret:

After creating credentials, you'll receive a Client ID and Client Secret.
Copy these values to a safe place as they'll be used in your Flask app.

#### 3. Configuration:
Configure the Flask App:

Open the .env file and add the obtained Client ID and Client Secret

#### 4. Running the Flask App:
Run the Flask App:

Execute the app.py file to start the Flask application.

#### 5. Access the site:

Go to http://localhost:5000 or the URL you specified.
You should see the site up and running.

Note:
Ensure the correct callback URLs are set both in your Google Developer Console credentials and within your Flask app configuration.
For production, use environment variables to store sensitive information like API keys and secrets.
These steps should help you set up the Flask site with Google OAuth2 authentication.
