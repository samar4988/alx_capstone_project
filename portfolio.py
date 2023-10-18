from flask import Flask, request, render_template, jsonify

import smtplib
from email.message import EmailMessage

SMTP_SERVER = 'localhost'
SMTP_PORT = 1025
RECIPIENT_EMAIL = "samar_email@host.com"

app = Flask(__name__)
    
@app.route('/')
def home():
    return render_template('Portfolio.html')

@app.route('/contact_me', methods=['POST'])
def contact_me():
    input_data = request.get_json()

    user_name = input_data.get('user_name')
    user_email = input_data.get('user_email')
    user_message = input_data.get('user_message')

    # If input are valid
    if user_name and user_email and user_message:

        # Create the email message
        msg = EmailMessage()
        msg.set_content(user_message)
        msg['Subject'] = f"Portfolio User {user_name}"
        msg['From'] = user_email
        msg['To'] = RECIPIENT_EMAIL

        # Connect to the SMTP server and send the email
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.sendmail(user_email, RECIPIENT_EMAIL, msg.as_string())
            server.quit()
            print("Email sent successfully.")
            return jsonify({'message': f'Email sent successfully. Thank you {user_name}.'})
        except Exception as e:
            print(f"Error sending email: {e}")
            return jsonify({'error': f'Error sending email: {e}'}), 400
    else:
        return jsonify({'error': 'All input fields must be filled.'}), 400

if __name__ == '__main__':
    app.run(debug=True)


# Start mail server
# python -m smtpd -c DebuggingServer -n localhost:1025


# Start Flask server
# python ./portfolio.py
