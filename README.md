# 📧 Enhanced Mail App

A modern, feature-rich email sending application built with Flask. Send personalized emails to multiple recipients with beautiful templates, contact management, and comprehensive tracking.

## ✨ Features

### 🔐 Security & Configuration
- **Secure Configuration**: Environment-based configuration with proper secret key management
- **Email Validation**: Real-time email format validation
- **File Upload Security**: Restricted file types and size limits (16MB max)
- **Input Sanitization**: Comprehensive input validation and sanitization

### 🎨 User Experience
- **Modern UI**: Beautiful, responsive design with gradient backgrounds and smooth animations
- **Multiple Templates**: Choose from Default, Professional, or Casual email templates
- **Email Preview**: Preview emails before sending with real-time template rendering
- **Draft Auto-Save**: Automatically saves drafts locally to prevent data loss
- **Progress Feedback**: Detailed success/failure reporting for bulk emails

### 📊 Contact Management
- **Contact Storage**: Save and manage recipient contacts
- **Contact Import**: Easy contact selection for email fields
- **Bulk Operations**: Export contacts to CSV, select all contacts
- **Contact Validation**: Duplicate prevention and email validation

### 📈 Email Tracking
- **Send History**: Complete history of sent emails with timestamps
- **Success/Failure Tracking**: Detailed status tracking for each email
- **Statistics Dashboard**: Visual stats showing total, successful, and failed emails
- **Export Functionality**: Export history to CSV for analysis

### 🛠 Technical Improvements
- **Better Error Handling**: Specific error messages and graceful failure handling
- **Logging**: Comprehensive logging for debugging and monitoring
- **File Management**: Automatic cleanup of uploaded attachments
- **Responsive Design**: Mobile-friendly interface

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Email account with SMTP access (Gmail, Outlook, etc.)

### Installation

1. **Clone or download the project**
   ```bash
   cd "Desktop/Mail App"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your email settings
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## ⚙️ Configuration

### Email Setup

#### Gmail Setup
1. Enable 2-factor authentication
2. Generate an app password: [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Use the app password in your `.env` file

#### Other Providers
- **Outlook/Hotmail**: `smtp.live.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **Custom SMTP**: Use your provider's settings

### Environment Variables
```env
SECRET_KEY=your-super-secret-key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

## 📱 Usage

### Sending Emails
1. **Fill in recipients**: Enter comma-separated emails and names
2. **Choose template**: Select from Default, Professional, or Casual
3. **Compose message**: Write your subject and body
4. **Add attachments**: Optional file attachments (multiple formats supported)
5. **Preview**: Use the preview button to see how your email will look
6. **Send**: Click send to deliver to all recipients

### Managing Contacts
1. **Add contacts**: Use the contacts page to save frequently used emails
2. **Import contacts**: Click "Load from Contacts" on the send page
3. **Export contacts**: Download your contact list as CSV

### Viewing History
1. **Track sends**: View all sent emails with timestamps and status
2. **Export history**: Download sending history for analysis
3. **Clear history**: Remove old records when needed

## 🎨 Email Templates

### Default Template
Clean, simple design suitable for general use

### Professional Template
Formal business template with company branding

### Casual Template
Fun, colorful template for informal communications

## 📁 File Structure
```
Mail App/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment configuration template
├── README.md             # This file
├── static/
│   └── style.css         # Enhanced CSS styles
├── templates/
│   ├── index.html        # Main email sending form
│   ├── contacts.html     # Contact management
│   ├── history.html      # Email history
│   ├── email_template.html           # Default email template
│   ├── email_template_professional.html  # Professional template
│   └── email_template_casual.html        # Casual template
└── Uploads/              # Temporary file storage (auto-created)
```

## 🔧 Technical Details

### Supported File Types
- Documents: `.txt`, `.pdf`, `.doc`, `.docx`
- Spreadsheets: `.xls`, `.xlsx`
- Presentations: `.ppt`, `.pptx`
- Images: `.png`, `.jpg`, `.jpeg`, `.gif`

### Data Storage
- **Contacts**: Stored in `contacts.json`
- **History**: Stored in `email_history.json`
- **Drafts**: Stored in browser localStorage
- **Logs**: Stored in `mail_app.log`

### Security Features
- Environment-based configuration
- Input validation and sanitization
- File type restrictions
- Secure file handling
- Error logging without sensitive data exposure

## 🐛 Troubleshooting

### Common Issues

**"Authentication failed"**
- Check your email credentials
- For Gmail, ensure you're using an app password
- Verify 2FA is enabled for Gmail

**"File too large"**
- Maximum file size is 16MB per file
- Try compressing large files

**"Invalid email format"**
- Ensure emails are properly formatted
- Check for extra spaces or special characters

**"Template not found"**
- Ensure all template files are in the templates/ directory
- Check file permissions

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application!

## 📄 License

This project is open source and available under the MIT License.
