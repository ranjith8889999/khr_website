# 🚀 DEPLOYMENT CHECKLIST

## Pre-Deployment Verification

### Backend Configuration
- [ ] Update email configuration in `backend/app.py`
  - [ ] Set MAIL_SERVER (Gmail, SendGrid, etc.)
  - [ ] Set MAIL_USERNAME
  - [ ] Set MAIL_PASSWORD (Gmail App Password recommended)
  - [ ] Set MAIL_DEFAULT_SENDER
  
- [ ] Update admin credentials
  - [ ] Change default username from "admin"
  - [ ] Change default password
  - [ ] Update in `admin/login.html` if using hardcoded login
  
- [ ] Set Flask SECRET_KEY
  - [ ] Generate new secret: `python -c "import secrets; print(secrets.token_hex(32))"`
  - [ ] Update in backend/app.py config

- [ ] Review database models
  - [ ] Check all field validations
  - [ ] Set proper database file path
  - [ ] Configure backup strategy

### Frontend Configuration
- [ ] Update social media links
  - [ ] Facebook profile URL
  - [ ] Twitter/X handle
  - [ ] Instagram profile
  - [ ] LinkedIn profile
  - [ ] YouTube channel

- [ ] Update contact information
  - [ ] Email address
  - [ ] Phone number
  - [ ] Office address
  - [ ] Office hours

- [ ] Optimize images
  - [ ] Compress all images in `images/` folder
  - [ ] Verify image paths in index.html
  - [ ] Add proper alt text
  - [ ] Test image loading

- [ ] Review content
  - [ ] Verify all text is accurate
  - [ ] Check for typos
  - [ ] Verify links are correct
  - [ ] Check social media links are current

### Testing
- [ ] Test all forms
  - [ ] Complaint form submission
  - [ ] Feedback form submission
  - [ ] Skills registration
  - [ ] Contact form
  
- [ ] Test responses
  - [ ] Verify success messages display
  - [ ] Check error handling
  - [ ] Test validation errors
  
- [ ] Test backend
  - [ ] Start Flask server: `python backend/app.py`
  - [ ] Submit test data
  - [ ] Verify database entries
  - [ ] Check email notifications

- [ ] Test admin panel
  - [ ] Login functionality
  - [ ] View dashboard
  - [ ] Check submitted data
  - [ ] Test status updates

- [ ] Browser testing
  - [ ] Test on Chrome
  - [ ] Test on Firefox
  - [ ] Test on Safari
  - [ ] Test on Edge

- [ ] Device testing
  - [ ] Desktop (1920x1080)
  - [ ] Laptop (1366x768)
  - [ ] Tablet (768x1024)
  - [ ] Mobile (375x667)

---

## Deployment Steps

### Choose Hosting Platform

#### Option 1: Heroku (Easiest for beginners)
- [ ] Create Heroku account
- [ ] Install Heroku CLI
- [ ] Create new app
- [ ] Connect to GitHub repo
- [ ] Deploy main branch
- [ ] Set environment variables
  ```
  MAIL_USERNAME = your_email@gmail.com
  MAIL_PASSWORD = your_app_password
  MAIL_SERVER = smtp.gmail.com
  SECRET_KEY = your_generated_secret
  ```

#### Option 2: PythonAnywhere (Python-specific)
- [ ] Create account
- [ ] Upload files via web interface
- [ ] Configure web app settings
- [ ] Set up virtual environment
- [ ] Set environment variables
- [ ] Restart web app

#### Option 3: AWS (More control)
- [ ] Create AWS account
- [ ] Launch EC2 instance
- [ ] Connect via SSH
- [ ] Install Python, Flask, SQLite
- [ ] Upload code
- [ ] Configure security groups
- [ ] Set environment variables

#### Option 4: DigitalOcean (Affordable)
- [ ] Create account
- [ ] Create droplet
- [ ] SSH into droplet
- [ ] Install dependencies
- [ ] Configure Nginx/Apache
- [ ] Deploy Flask app
- [ ] Set up SSL

#### Option 5: Traditional Hosting (If available)
- [ ] Check Python support
- [ ] Upload via FTP
- [ ] Configure Python interpreter
- [ ] Set up virtual environment
- [ ] Configure web server

### Domain & SSL Configuration
- [ ] Purchase domain name
- [ ] Update DNS settings
- [ ] Point to hosting provider
- [ ] Enable SSL certificate
  - [ ] Use Let's Encrypt (free)
  - [ ] Configure auto-renewal
  - [ ] Update URLs to HTTPS

### Database Configuration
- [ ] Migrate from SQLite to PostgreSQL (optional)
  - [ ] Or use SQLite with proper backups
  - [ ] Set database connection string
  - [ ] Run migrations if needed

- [ ] Set up database backups
  - [ ] Daily backups
  - [ ] Store in cloud
  - [ ] Test backup restoration

### Email Service Setup

#### Gmail Setup
1. [ ] Enable 2-Step Verification on Gmail
2. [ ] Create App Password (16 characters)
3. [ ] Copy password to environment variables
4. [ ] Test with sample email

#### SendGrid Setup
1. [ ] Create SendGrid account
2. [ ] Create API key
3. [ ] Update MAIL_SERVER to SendGrid
4. [ ] Update credentials
5. [ ] Test with sample email

#### Alternative (SES, Mailgun, etc.)
- [ ] Create account
- [ ] Get credentials
- [ ] Update backend/app.py
- [ ] Test email sending

### Post-Deployment Verification
- [ ] Website loads without errors
- [ ] All pages load correctly
- [ ] Forms submit successfully
- [ ] Emails are received
- [ ] Admin dashboard works
- [ ] Database saves data
- [ ] Images load properly
- [ ] Mobile responsiveness works
- [ ] All links are functional
- [ ] Social media links work

### Performance & Security
- [ ] Run security scan
  - [ ] Check for HTTPS everywhere
  - [ ] Verify no hardcoded secrets
  - [ ] Check CORS configuration
  - [ ] Validate input sanitization

- [ ] Optimize performance
  - [ ] Minify CSS/JS
  - [ ] Compress images
  - [ ] Enable caching
  - [ ] Use CDN if available

- [ ] Set up monitoring
  - [ ] Add error tracking (Sentry)
  - [ ] Set up uptime monitoring
  - [ ] Configure alerts
  - [ ] Review error logs

### Maintenance Plan
- [ ] Schedule regular backups
- [ ] Monitor form submissions
- [ ] Check error logs weekly
- [ ] Update dependencies monthly
- [ ] Review security updates

---

## Email Configuration Guide

### Gmail SMTP Configuration

```python
# In backend/app.py

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = "your_email@gmail.com"  # Your Gmail address
MAIL_PASSWORD = "your_app_password"      # 16-char app password
MAIL_DEFAULT_SENDER = "webmaster@example.com"
```

### Steps to Get Gmail App Password:
1. Go to https://myaccount.google.com
2. Select "Security" on left side
3. Enable "2-Step Verification"
4. Go back to Security
5. Find "App passwords"
6. Select Mail and Windows Computer
7. Copy the 16-character password

### SendGrid Configuration

```python
MAIL_SERVER = "smtp.sendgrid.net"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = "apikey"
MAIL_PASSWORD = "your_sendgrid_api_key"
MAIL_DEFAULT_SENDER = "noreply@yourdomain.com"
```

---

## Environment Variables Template

Create `.env` file in root directory:

```
# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=webmaster@example.com

# Flask Configuration
SECRET_KEY=your_generated_secret_key_here
FLASK_ENV=production
DEBUG=False

# Database
DATABASE_URL=sqlite:///khr_database.db

# Admin Credentials
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=your_admin_password_hash

# Website Configuration
WEBSITE_URL=https://yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com
```

---

## Troubleshooting After Deployment

### Website Not Loading
- [ ] Check web server logs
- [ ] Verify port configuration
- [ ] Check DNS settings
- [ ] Verify SSL certificate
- [ ] Check firewall rules

### Forms Not Submitting
- [ ] Check backend server status
- [ ] Verify API endpoints are accessible
- [ ] Check CORS configuration
- [ ] Review browser console errors
- [ ] Check network tab in DevTools

### Emails Not Sending
- [ ] Verify email credentials
- [ ] Check email logs in backend
- [ ] Test with test email script
- [ ] Verify SMTP port is open
- [ ] Check email provider settings

### Database Errors
- [ ] Verify database file exists
- [ ] Check file permissions
- [ ] Verify database connectivity
- [ ] Check for locked database
- [ ] Review error logs

### Performance Issues
- [ ] Check server resources
- [ ] Enable caching
- [ ] Optimize database queries
- [ ] Minify assets
- [ ] Use CDN for images

### Security Alerts
- [ ] Remove debug mode
- [ ] Update all dependencies
- [ ] Change default credentials
- [ ] Enable HTTPS everywhere
- [ ] Set up security headers

---

## Monitoring Checklist

- [ ] Set up error tracking (Sentry, Rollbar)
- [ ] Configure uptime monitoring
- [ ] Set up email alerts
- [ ] Monitor database usage
- [ ] Track website performance
- [ ] Review user submissions
- [ ] Check admin dashboard
- [ ] Monitor email delivery
- [ ] Track visitor statistics
- [ ] Review security logs

---

## Maintenance Schedule

### Daily
- [ ] Check error logs
- [ ] Monitor form submissions
- [ ] Verify website uptime

### Weekly
- [ ] Review submitted forms
- [ ] Check email notifications
- [ ] Monitor database size
- [ ] Check backup status

### Monthly
- [ ] Update dependencies
- [ ] Review security updates
- [ ] Optimize database
- [ ] Check server performance
- [ ] Update content if needed

### Quarterly
- [ ] Full security audit
- [ ] Disaster recovery test
- [ ] Performance optimization
- [ ] User feedback review
- [ ] Capacity planning

---

## Success Criteria

Your deployment is successful when:
✅ Website loads in all browsers  
✅ All forms submit correctly  
✅ Emails are received  
✅ Admin dashboard shows submitted data  
✅ Mobile version is responsive  
✅ No console errors  
✅ Database is growing with submissions  
✅ Performance is satisfactory  
✅ SSL certificate is valid  
✅ All links work correctly  

---

## Final Reminders

🔒 **Security First**
- Never commit .env with real credentials
- Use strong admin password
- Keep dependencies updated
- Enable HTTPS
- Regular security audits

📈 **Growth Ready**
- Monitor submissions
- Back up data regularly
- Plan for scaling
- Track metrics
- Get user feedback

🤝 **Community Support**
- Enable feedback system
- Monitor complaints
- Respond to messages
- Engage with community
- Share updates regularly

---

**Good luck with your deployment! 🚀**

For help: Check README.md or QUICKSTART.md
