import os
import re
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, jsonify, session
from flask_mail import Mail, Message
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mail_app.log'),
        logging.StreamHandler()
    ]
)

# Mail configuration using env vars
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions for attachments
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'}

mail = Mail(app)

# Utility functions
def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_email_history(to_emails, subject, status):
    """Save email sending history to JSON file"""
    history_file = 'email_history.json'
    history_entry = {
        'timestamp': datetime.now().isoformat(),
        'recipients': to_emails,
        'subject': subject,
        'status': status
    }

    try:
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = []

        history.append(history_entry)

        # Keep only last 100 entries
        if len(history) > 100:
            history = history[-100:]

        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to save email history: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        to_emails = [e.strip() for e in request.form['to'].split(',') if e.strip()]
        cc_emails = [e.strip() for e in request.form.get('cc', '').split(',') if e.strip()]
        names = [n.strip() for n in request.form['names'].split(',') if n.strip()]
        subject = request.form['subject'].strip()
        body = request.form['body'].strip()
        template_choice = request.form.get('template', 'default')

        # Validation
        if not to_emails or not names or not subject or not body:
            flash("Please fill in all required fields.", "danger")
            return redirect('/')

        if len(to_emails) != len(names):
            flash("Number of emails and names must match.", "danger")
            return redirect('/')

        # Validate email formats
        invalid_emails = [email for email in to_emails + cc_emails if not validate_email(email)]
        if invalid_emails:
            flash(f"Invalid email format(s): {', '.join(invalid_emails)}", "danger")
            return redirect('/')

        # Create uploads directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        try:
            sent_count = 0
            failed_emails = []

            for recipient, name in zip(to_emails, names):
                try:
                    msg = Message(subject=subject, recipients=[recipient], cc=cc_emails)

                    # Choose template
                    if template_choice == 'professional':
                        template_name = 'email_template_professional.html'
                    elif template_choice == 'casual':
                        template_name = 'email_template_casual.html'
                    else:
                        template_name = 'email_template.html'

                    msg.html = render_template(template_name, name=name, body=body)

                    # Handle attachments with validation
                    if 'attachments' in request.files:
                        for file in request.files.getlist('attachments'):
                            if file.filename:
                                if not allowed_file(file.filename):
                                    flash(f"File type not allowed: {file.filename}", "warning")
                                    continue

                                filename = secure_filename(file.filename)
                                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                                file.save(filepath)

                                with open(filepath, 'rb') as f:
                                    msg.attach(filename, file.content_type or 'application/octet-stream', f.read())

                                # Clean up uploaded file after attaching
                                os.remove(filepath)

                    mail.send(msg)
                    sent_count += 1
                    logging.info(f"Email sent successfully to {recipient}")

                except Exception as e:
                    failed_emails.append(f"{recipient}: {str(e)}")
                    logging.error(f"Failed to send email to {recipient}: {e}")

            # Save to history
            save_email_history(to_emails, subject, f"Sent: {sent_count}, Failed: {len(failed_emails)}")

            if sent_count > 0:
                flash(f"Successfully sent {sent_count} email(s)!", "success")

            if failed_emails:
                flash(f"Failed to send to: {'; '.join(failed_emails)}", "danger")

        except Exception as e:
            logging.error(f"General error in email sending: {e}")
            flash(f"Error: {str(e)}", "danger")
            save_email_history(to_emails, subject, f"Failed: {str(e)}")

        return redirect('/')

    return render_template('index.html')

@app.route('/preview', methods=['POST'])
def preview_email():
    """Preview email before sending"""
    name = request.form.get('preview_name', 'Preview User')
    body = request.form.get('body', '')
    template_choice = request.form.get('template', 'default')

    if template_choice == 'professional':
        template_name = 'email_template_professional.html'
    elif template_choice == 'casual':
        template_name = 'email_template_casual.html'
    else:
        template_name = 'email_template.html'

    try:
        preview_html = render_template(template_name, name=name, body=body)
        return jsonify({'success': True, 'html': preview_html})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/history')
def email_history():
    """View email sending history"""
    try:
        if os.path.exists('email_history.json'):
            with open('email_history.json', 'r') as f:
                history = json.load(f)
            # Sort by timestamp, newest first
            history.sort(key=lambda x: x['timestamp'], reverse=True)
        else:
            history = []
        return render_template('history.html', history=history)
    except Exception as e:
        flash(f"Error loading history: {e}", "danger")
        return redirect('/')

@app.route('/contacts')
def contacts():
    """Manage contacts"""
    try:
        if os.path.exists('contacts.json'):
            with open('contacts.json', 'r') as f:
                contacts = json.load(f)
        else:
            contacts = []
        return render_template('contacts.html', contacts=contacts)
    except Exception as e:
        flash(f"Error loading contacts: {e}", "danger")
        return redirect('/')

@app.route('/save_contact', methods=['POST'])
def save_contact():
    """Save a new contact"""
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()

    if not name or not email:
        flash("Name and email are required.", "danger")
        return redirect('/contacts')

    if not validate_email(email):
        flash("Invalid email format.", "danger")
        return redirect('/contacts')

    try:
        if os.path.exists('contacts.json'):
            with open('contacts.json', 'r') as f:
                contacts = json.load(f)
        else:
            contacts = []

        # Check if contact already exists
        for contact in contacts:
            if contact['email'].lower() == email.lower():
                flash("Contact with this email already exists.", "warning")
                return redirect('/contacts')

        contacts.append({'name': name, 'email': email})

        with open('contacts.json', 'w') as f:
            json.dump(contacts, f, indent=2)

        flash("Contact saved successfully!", "success")
    except Exception as e:
        flash(f"Error saving contact: {e}", "danger")

    return redirect('/contacts')

@app.route('/delete_contact/<int:index>')
def delete_contact(index):
    """Delete a contact"""
    try:
        if os.path.exists('contacts.json'):
            with open('contacts.json', 'r') as f:
                contacts = json.load(f)

            if 0 <= index < len(contacts):
                deleted_contact = contacts.pop(index)

                with open('contacts.json', 'w') as f:
                    json.dump(contacts, f, indent=2)

                flash(f"Contact '{deleted_contact['name']}' deleted successfully!", "success")
            else:
                flash("Contact not found.", "danger")
        else:
            flash("No contacts found.", "danger")
    except Exception as e:
        flash(f"Error deleting contact: {e}", "danger")

    return redirect('/contacts')

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear email history"""
    try:
        if os.path.exists('email_history.json'):
            os.remove('email_history.json')
        return jsonify({'success': True})
    except Exception as e:
        logging.error(f"Error clearing history: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
