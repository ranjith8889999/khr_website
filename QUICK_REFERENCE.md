# 📚 QUICK REFERENCE GUIDE

## Project Overview
**Website**: Kolan Hanmanth Reddy - Political Leader Website  
**Status**: ✅ Complete & Ready for Deployment  
**Version**: 1.0.0  
**Tech Stack**: HTML5, CSS3, JavaScript, Python Flask, SQLite

---

## 🗂️ File Structure Quick Reference

```
ROOT
├── index.html                  # Main website
├── setup.bat                   # Windows auto-setup
├── .env.example               # Config template
├── .gitignore                 # Git ignore rules
│
├── README.md                  # 📘 Full documentation
├── QUICKSTART.md             # ⚡ 5-min setup guide
├── PROJECT_SUMMARY.md        # 📊 Completion summary
├── TESTING_VALIDATION.md     # ✅ Test checklist
├── DEPLOYMENT_CHECKLIST.md   # 🚀 Deploy guide
│
├── css/
│   ├── styles.css           # Main styles
│   ├── responsive.css       # Mobile responsive
│   └── animations.css       # Animations & effects
│
├── js/
│   └── main.js             # All JavaScript functions
│
├── admin/
│   ├── login.html          # Admin login
│   └── dashboard.html      # Admin panel
│
├── backend/
│   ├── app.py             # Flask app (all backend logic)
│   └── requirements.txt    # Python dependencies
│
├── data/
│   └── content.json       # Structured content reference
│
└── images/                # Image assets (7 images provided)
    └── (image files)
```

---

## 🎯 Key Files & Their Purpose

| File | Purpose | Size |
|------|---------|------|
| index.html | Main website with all sections | 1000+ lines |
| css/styles.css | Primary styling | 1500+ lines |
| js/main.js | Form handling & interactions | 700+ lines |
| backend/app.py | Flask API & database | 500+ lines |
| admin/dashboard.html | Admin interface | 900+ lines |
| README.md | Complete documentation | 2000+ words |

---

## 🚀 Getting Started (5 Minutes)

### Windows Setup
```bash
# 1. Extract project folder
# 2. Open Command Prompt in project folder
# 3. Run setup script
setup.bat

# 4. Start backend (in Command Prompt)
python backend/app.py

# 5. Open website (in browser)
http://localhost:5000/index.html
```

### Mac/Linux Setup
```bash
# 1. Extract project folder
# 2. Open Terminal in project folder
# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r backend/requirements.txt

# 5. Start backend
python backend/app.py

# 6. Open website
# Open index.html in browser
```

---

## 📝 Configuration

### Email Setup (Important!)
Edit `backend/app.py`, find these lines:

```python
# Line ~20-30
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = "your_email@gmail.com"      # UPDATE THIS
MAIL_PASSWORD = "your_app_password"         # UPDATE THIS
MAIL_DEFAULT_SENDER = "noreply@example.com" # UPDATE THIS
```

### Admin Credentials
**Current Demo Credentials:**
```
Username: khr
Password: khr@123
```

To change these permanently in backend/app.py, find this line (around line ~150):

```python
# IMPORTANT: Change demo credentials!
admin_user = AdminUser(
    username="khr",            # Change this
    email="admin@example.com", # Change this
    password_hash=generate_password_hash("khr@123"), # Change to your password
    is_active=True
)
```

---

## 🔗 API Endpoints Reference

### Base URL
```
http://localhost:5000/api
```

### Complaints
```
POST /api/complaint
Body: {name, phone, email, area, category, subject, message, address}
Response: {success: true, reference_number: "CMP-..."}
```

### Feedback
```
POST /api/feedback
Body: {name, email, phone, category, rating, message}
Response: {success: true}
```

### Skills Registration
```
POST /api/skills-registration
Body: {name, phone, email, dob, education, institution, location, city, motivation}
Response: {success: true}
```

### Contact
```
POST /api/contact
Body: {name, email, phone, subject, message}
Response: {success: true}
```

### Status Check
```
GET /api/status
Response: {status: "ok", message: "API is running"}
```

---

## 🎨 CSS Quick Reference

### Colors
```css
--primary-color: #ff9500;    /* Saffron */
--secondary-color: #003d7a;  /* Blue */
--text-color: #333333;
--light-color: #f5f5f5;
--danger-color: #dc3545;
```

### Responsive Breakpoints
```css
/* Desktop */
@media (max-width: 1200px) { }

/* Tablet */
@media (max-width: 768px) { }

/* Mobile */
@media (max-width: 480px) { }

/* Small Mobile */
@media (max-width: 360px) { }
```

---

## 📱 Form Fields Reference

### Complaint Form
1. Name (required)
2. Phone (10 digits, required)
3. Email (valid format, required)
4. Area (required)
5. Category (select, required)
6. Subject (required)
7. Message (required)
8. Address (required)

### Feedback Form
1. Name (required)
2. Email (required)
3. Phone (10 digits, required)
4. Category (select, required)
5. Rating (1-5 stars, required)
6. Message (required)

### Skills Registration Form
1. Name (required)
2. Phone (10 digits, required)
3. Email (required)
4. Date of Birth (required)
5. Education (required)
6. Institution (required)
7. Location (select, required)
8. City (required)
9. Motivation (required)

### Contact Form
1. Name (required)
2. Email (required)
3. Phone (10 digits, required)
4. Subject (required)
5. Message (required)

---

## 🔐 Admin Dashboard

### Login
```
URL: http://localhost:5000/admin/login.html
Username: khr
Password: khr@123
```

### Dashboard Features
- View all submissions
- Filter by status
- Update complaint status
- View detailed information
- Delete records
- Track statistics

---

## 📊 Database Schema

### Tables
```
complaints (id, name, phone, email, area, category, subject, message, address, status, reference_number, created_at, updated_at, admin_notes)

feedback (id, name, email, phone, category, rating, message, status, created_at)

skills_registrations (id, name, phone, email, dob, education, institution, location, city, motivation, status, confirmation_sent, created_at)

contacts (id, name, email, phone, subject, message, status, created_at)

admin_users (id, username, email, password_hash, role, is_active, created_at)
```

---

## 🧪 Quick Testing

### Test Complaint Submission
```bash
# Using curl
curl -X POST http://localhost:5000/api/complaint \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "phone": "9876543210",
    "email": "test@example.com",
    "area": "Quthbullapur",
    "category": "complaint",
    "subject": "Test",
    "message": "Test complaint",
    "address": "Test Address"
  }'
```

### Test Email
```python
# Add to backend/app.py and run
with app.app_context():
    send_complaint_confirmation_email(
        "Test User",
        "your-email@gmail.com",
        "CMP-TEST-001"
    )
```

---

## 🐛 Troubleshooting Quick Tips

| Problem | Solution |
|---------|----------|
| Port 5000 already in use | Change port in app.py line ~390: `app.run(port=5001)` |
| Module not found | Run: `pip install -r backend/requirements.txt` |
| Forms not saving | Check browser console (F12) for errors |
| Emails not sending | Verify MAIL_USERNAME and MAIL_PASSWORD in app.py |
| Admin dashboard blank | Clear localStorage: DevTools > Application > Clear All |
| Images not loading | Verify images/ folder has files with correct names |
| Responsive not working | Check viewport meta tag in index.html |
| CSS not applying | Clear browser cache (Ctrl+Shift+Delete) |

---

## 📈 Performance Tips

1. **Minify CSS/JS** for production
   ```bash
   # Use online tools or Node.js tools
   ```

2. **Compress images**
   ```bash
   # Use TinyPNG or ImageOptim
   ```

3. **Enable caching**
   ```python
   # Add to backend/app.py
   @app.after_request
   def add_cache_headers(response):
       response.cache_control.max_age = 3600
       return response
   ```

4. **Use CDN** for static files (optional, advanced)

---

## 🔒 Security Checklist

Before deployment:
- [ ] Change admin credentials
- [ ] Update email configuration
- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS
- [ ] Remove debug mode
- [ ] Validate all inputs
- [ ] Check error handling
- [ ] Review admin permissions

---

## 📚 Documentation Map

| Document | Best For |
|----------|----------|
| **README.md** | Complete setup & overview |
| **QUICKSTART.md** | Fast 5-minute setup |
| **PROJECT_SUMMARY.md** | What was built |
| **TESTING_VALIDATION.md** | Testing procedures |
| **DEPLOYMENT_CHECKLIST.md** | Going live |
| **This file** | Quick reference |

---

## 🆘 Getting Help

1. **Check README.md** first
2. **Review TESTING_VALIDATION.md** for known issues
3. **Check browser console** (F12) for errors
4. **Check Flask server logs** for backend issues
5. **Review code comments** in relevant files

---

## ⚡ Common Commands

### Python/Backend
```bash
# Start virtual environment
source venv/bin/activate            # Mac/Linux
venv\Scripts\activate               # Windows

# Install dependencies
pip install -r backend/requirements.txt

# Start Flask server
python backend/app.py

# Run database setup
python -c "from backend.app import *; db.create_all()"
```

### File Navigation
```bash
# List files
ls -la                              # Mac/Linux
dir                                 # Windows

# Check Python version
python --version

# Check pip packages
pip list
```

### Git Commands (After deployment)
```bash
# Initialize git
git init

# Add files
git add .

# Commit
git commit -m "Initial commit"

# Push to GitHub
git push origin main
```

---

## 💡 Pro Tips

1. **Use VS Code** for easier editing
   - Install Python extension
   - Install Live Server extension
   - Install Prettier for formatting

2. **Use Postman** for API testing
   - Download from: https://www.postman.com/downloads/
   - Import API collection
   - Test endpoints easily

3. **Use CloudFlare** for free CDN
   - Speeds up image delivery
   - Provides SSL certificate
   - DDoS protection

4. **Use GitHub** for version control
   - Free public/private repos
   - Easy deployment
   - Easy backups

5. **Use Sentry** for error tracking
   - Catches production errors
   - Sends alerts
   - Tracks user sessions

---

## 📞 Contact & Support

**For Website Visitors:**
- Contact form in index.html
- Social media links in footer
- Email address in contact section

**For Developers/Admins:**
- Check README.md
- Review code comments
- Check error logs
- Test systematically

---

## 🎓 Learning Resources

- **HTML/CSS**: MDN Web Docs (https://developer.mozilla.org)
- **JavaScript**: JavaScript.info (https://javascript.info)
- **Python/Flask**: Flask Official Docs (https://flask.palletsprojects.com)
- **Database**: SQLAlchemy Docs (https://docs.sqlalchemy.org)

---

## 📋 Checklist Before Going Live

- [ ] All forms tested and working
- [ ] Emails sending correctly
- [ ] Admin dashboard functional
- [ ] Images loading properly
- [ ] Mobile responsive verified
- [ ] All links working
- [ ] No console errors
- [ ] Performance acceptable
- [ ] Security reviewed
- [ ] Database backed up

---

## 🏆 You're All Set!

Everything is ready to:
✅ Run locally  
✅ Customize content  
✅ Test thoroughly  
✅ Deploy to production  
✅ Maintain over time  

**Questions?** Check the relevant guide in the docs folder.

---

**Happy coding! 🚀**

*Last Updated: March 3, 2026*  
*Project Version: 1.0.0*  
*Status: Production Ready*
