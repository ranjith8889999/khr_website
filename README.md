# Kolan Hanmanth Reddy - Political Leader Website

A modern, premium political leader website built with HTML5, CSS3, JavaScript, and Python Flask backend. This comprehensive platform showcases Kolan Hanmanth Reddy's political career, community service initiatives, and provides interactive forms for complaints, feedback, and youth skill registration.

## 🌟 Features

### Frontend Features
- **Responsive Design**: Mobile-first approach, fully responsive on all devices
- **Modern UI/UX**: Clean, elegant, and professional design with animations
- **Smooth Animations**: AOS (Animate On Scroll) library for smooth transitions
- **Interactive Components**: Lightbox gallery, dropdown menus, form validation
- **Sticky Navigation**: Easy navigation with sticky navbar
- **Section-based Layout**: Well-organized sections with clear information hierarchy

### Backend Features
- **Python Flask API**: RESTful API for form submissions
- **Database**: SQLite database for storing complaints, feedback, and registrations
- **Email Notifications**: Automated confirmation emails to users
- **Admin Dashboard**: Comprehensive admin panel to manage all submissions
- **Status Tracking**: Track complaint and registration status
- **Data Management**: View, update, and manage all user submissions

### Forms & Systems
1. **Complaint Filing System**
   - Public complaint submission form
   - Reference number generation
   - Status tracking (pending, resolved, rejected)
   - Email notifications

2. **Feedback System**
   - 5-star rating system
   - Feedback categories
   - Public submission form
   - Admin view of all feedback

3. **Skills for Youth Program**
   - Youth skill development registration
   - Automatic confirmation emails
   - Admin tracking and management
   - Status updates (pending, approved, rejected)

4. **Contact Form**
   - General inquiry form
   - Message tracking
   - Email notifications

## 📁 Folder Structure

```
khr1/
├── index.html                  # Main website page
├── kolan.txt                   # Content file
├── css/
│   ├── styles.css             # Main stylesheet
│   ├── responsive.css         # Media queries and responsive design
│   └── animations.css         # Animation keyframes
├── js/
│   └── main.js                # Main JavaScript functionality
├── admin/
│   ├── login.html             # Admin login page
│   └── dashboard.html         # Admin dashboard
├── backend/
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   └── khr_database.db        # SQLite database (auto-created)
├── images/                    # Image folder with all assets
└── data/
    └── content.json          # Content data (optional)
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Modern web browser
- Text editor or IDE (VS Code recommended)

### Installation

#### 1. Clone/Download the Project
```bash
# Navigate to the project directory
cd khr1
```

#### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### 4. Configure Email (Optional)
Edit `backend/app.py` and update the email configuration:
```python
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
```

#### 5. Initialize Database
```bash
python app.py
```
This will create the SQLite database automatically.

### Running the Website

#### Option 1: Backend + Frontend (Full Stack)
```bash
# Terminal 1: Start Flask backend
cd backend
python app.py
# Server runs on http://localhost:5000

# Terminal 2: Serve frontend (open in browser)
# Open ../index.html in your browser
# Or use a local server:
cd ..
python -m http.server 8000
# Visit http://localhost:8000/index.html
```

#### Option 2: Frontend Only (Demo Mode)
```bash
# Just open index.html directly in your browser
# Or use a local server:
python -m http.server 8000
# Visit http://localhost:8000/index.html
```

## 📝 Usage

### Public Website
1. **Browse the Website**: Navigate through different sections
   - Hero section with leadership introduction
   - About section with biography
   - Timeline showing political journey
   - Vision and focus areas
   - Community impact showcase
   - News and media coverage
   - Photo gallery

2. **Submit Forms**:
   - **Complaints**: Navigate to "Programs > Complaints"
   - **Feedback**: Navigate to "Programs > Feedback"
   - **Skills Registration**: Navigate to "Programs > Youth Skills"
   - **Contact**: Scroll to "Contact" section

3. **Admin Access**:
   - Click "Admin" button in navigation
   - Login credentials (default):
     - Username: `khr`
     - Password: `khr@123`
   - View and manage all submissions
   - Update status of complaints and registrations

### Admin Dashboard
1. **Overview**: View statistics and recent submissions
2. **Complaints**: View all complaints, filter by status, update status
3. **Feedback**: View all feedback and ratings
4. **Skills Program**: View registrations, approve/reject applicants
5. **Messages**: View contact form submissions

## 🔧 Configuration

### Customize Content
Edit `kolan.txt` to update content. The website pulls information about:
- Biography and profile
- Political journey and timeline
- Focus areas and initiatives
- Community service details

### Update Images
Replace image files in the `images/` folder:
- Use optimized images for web (min 72 DPI, max 2MB)
- Maintain aspect ratio for consistency
- Recommended format: JPEG or WebP

### Customize Colors
Edit CSS variables in `css/styles.css`:
```css
:root {
    --primary-color: #ff9500;      /* Orange/Saffron */
    --secondary-color: #003d7a;    /* Blue */
    --accent-color: #1e88e5;       /* Light Blue */
    /* ... other colors ... */
}
```

## 📱 Responsive Breakpoints
- **Desktop**: 1200px and above
- **Tablet**: 768px to 1199px
- **Mobile**: 480px to 767px
- **Extra Small**: Below 480px

## 🔐 Security Notes

1. **Admin Panel**: Currently uses simple authentication for demo. For production:
   - Implement proper authentication with hashing
   - Use environment variables for sensitive data
   - Enable HTTPS
   - Implement CSRF protection

2. **Database**: 
   - SQLite suitable for small-to-medium sites
   - For larger scale, migrate to PostgreSQL or MySQL
   - Implement regular backups

3. **Email Configuration**:
   - Use app-specific passwords for Gmail
   - For production, use professional email service (SendGrid, AWS SES, etc.)

## 🚢 Deployment

### Local Deployment
1. Ensure Python and dependencies are installed
2. Run `python backend/app.py`
3. Serve frontend files through web server

### Cloud Deployment Options

#### Heroku
```bash
# Create Procfile
echo "web: python backend/app.py" > Procfile

# Deploy
heroku create
git push heroku main
```

#### PythonAnywhere
1. Upload files to PythonAnywhere
2. Configure web app to use Flask
3. Set environment variables

#### AWS/DigitalOcean
1. Create server instance
2. Install Python and dependencies
3. Use Gunicorn as WSGI server
4. Configure Nginx as reverse proxy
5. Set up SSL certificate

## 📊 Database Schema

### Complaints Table
```
- id (Primary Key)
- name, phone, email
- area, category, subject, message, address
- status (pending, resolved, rejected)
- reference_number (unique)
- created_at, updated_at
```

### Feedback Table
```
- id (Primary Key)
- name, email, phone
- category, rating (1-5), message
- created_at
```

### Skills Registrations Table
```
- id (Primary Key)
- name, phone, email, dob
- education, institution
- location, city, motivation
- status (pending, approved, rejected)
- created_at, updated_at
```

### Contacts Table
```
- id (Primary Key)
- name, email, phone
- subject, message
- created_at
```

## 🎨 Customization Guide

### Change Primary Colors
1. Edit `css/styles.css`
2. Update `--primary-color` and `--secondary-color` variables
3. Refresh browser to see changes

### Add New Sections
1. Add HTML in `index.html`
2. Style with CSS classes
3. Add animations with AOS attributes: `data-aos="fade-up"`

### Modify Forms
1. Edit form in `index.html`
2. Update JavaScript validation in `js/main.js`
3. Add backend route in `backend/app.py` if needed

## 📞 Support & Contact

For issues or questions:
1. Check the provided documentation
2. Review code comments
3. Test in different browsers
4. Check browser console for errors (F12)

## 📄 License

This website is a custom political leader website. Use and modify as needed.

## ✅ Browser Compatibility

- Chrome/Chromium: ✅ Latest 2 versions
- Firefox: ✅ Latest 2 versions
- Safari: ✅ Latest 2 versions
- Edge: ✅ Latest 2 versions
- IE11: ❌ Not supported

## 🚀 Performance Tips

1. **Images Optimization**:
   - Use WebP format where possible
   - Compress images before upload
   - Use responsive image sizes

2. **Caching**:
   - Enable browser caching
   - Use CDN for static assets
   - Cache database queries

3. **Code Optimization**:
   - Minify CSS and JavaScript
   - Remove unused code
   - Lazy load images

## 📋 Checklist for Production

- [ ] Update email configuration
- [ ] Change admin credentials
- [ ] Set `debug=False` in Flask
- [ ] Enable HTTPS
- [ ] Set up regular backups
- [ ] Test all forms
- [ ] Optimize images
- [ ] Update ownership information
- [ ] Set up analytics (Google Analytics)
- [ ] Submit sitemap to search engines

## 🎯 Future Enhancements

- [ ] Advanced analytics dashboard
- [ ] Email campaign system
- [ ] News management system
- [ ] Photo gallery management
- [ ] Event calendar
- [ ] Video integration
- [ ] Blog functionality
- [ ] Multi-language support
- [ ] Mobile app

---

**Version**: 1.0.0  
**Last Updated**: March 2024  
**Author**: Admin  

For more information and support, please refer to the inline code comments and documentation.
