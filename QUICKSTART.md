# Quick Start Guide - Kolan Hanmanth Reddy Website

## ⚡ 5-Minute Quick Start

### Windows Users
1. **Download & Extract**: Extract the project folder
2. **Run Setup**: Double-click `setup.bat` and wait for completion
3. **Start Backend**: 
   - Open Command Prompt
   - Navigate to project folder
   - Run: `venv\Scripts\activate.bat`
   - Run: `cd backend && python app.py`
4. **Open Website**: Double-click `index.html` or open in browser at `http://localhost:8000`
5. **Admin Panel**: Go to Admin → Login with `khr`/`khr@123`

### Mac/Linux Users
1. **Download & Extract**: Extract the project folder
2. **Open Terminal**: Navigate to project directory
3. **Setup**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   cd backend
   pip install -r requirements.txt
   python app.py
   ```
4. **Open Website**: Open `index.html` in browser
5. **Admin Panel**: Login with `khr`/`khr@123`

## 📋 Website Sections

### Public Sections
- **Hero**: Leadership introduction
- **About**: Biography and background
- **Timeline**: Political journey milestones
- **Vision**: Future goals and plans
- **Focus Areas**: Key initiatives
- **Community Impact**: Service and achievements
- **News**: Latest updates
- **Media**: Press coverage and links
- **Gallery**: Photo gallery
- **Testimonials**: Success stories

### Interactive Forms
1. **Complaint Form**: File public complaints
2. **Feedback Form**: Submit ratings and suggestions
3. **Skills Program**: Register for youth training
4. **Contact Form**: General inquiries

## 🔑 Admin Access

### Default Credentials
- **URL**: http://localhost:5000/admin/login.html
- **Username**: khr
- **Password**: khr@123

⚠️ **Change these immediately in production!**

### Admin Dashboard Features
- View all complaints
- Track complaint status
- View feedback and ratings
- Manage skill registrations
- View contact messages
- Update submission status

## 🎨 Customization

### Change Text Content
Edit `kolan.txt` with:
- Biography details
- Focus areas
- Community service information
- Timeline points

### Change Images
Replace files in `images/` folder with your images

### Change Colors
Edit `css/styles.css`:
```css
--primary-color: #ff9500;      /* Orange */
--secondary-color: #003d7a;    /* Blue */
```

### Change Contact Info
Edit footer in `index.html`:
```html
<!-- Update address, phone, links -->
```

## 🚀 Common Tasks

### Add New Section
1. Add HTML in `index.html`
2. Add CSS in `css/styles.css`
3. Add animations in `css/animations.css`
4. Use `data-aos="fade-up"` for animations

### Modify Form Fields
1. Edit form in `index.html`
2. Update validation in `js/main.js`
3. Update database model in `backend/app.py` (if needed)

### Configure Email
1. Update `backend/app.py`:
   ```python
   app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
   app.config['MAIL_PASSWORD'] = 'your-app-password'
   ```
2. For Gmail:
   - Enable 2-Step Verification
   - Create App Password
   - Use App Password in config

## 📱 Testing

### Test on Different Devices
1. Open in Chrome DevTools (F12)
2. Click device toggle (mobile icon)
3. Test on:
   - iPhone (375px)
   - iPad (768px)
   - Desktop (1024px+)

### Test Forms
1. Submit complaint with test data
2. Check email for confirmation
3. Visit admin dashboard
4. View complaint details
5. Update status

## 🔧 Troubleshooting

### "Python not found"
- Install Python 3.7+
- Add to PATH during installation
- Restart Command Prompt

### "Port already in use"
- Change port in `app.py`:
  ```python
  app.run(debug=True, port=5001)  # Use 5001 instead
  ```

### Forms not working
- Check browser console (F12)
- Ensure backend is running
- Clear browser cache

### Emails not sending
- Check email configuration
- Use app-specific password (if Gmail)
- Check junk/spam folder

## 📞 Support Resources

- **Python**: https://python.org
- **Flask**: https://flask.palletsprojects.com
- **Bootstrap**: https://getbootstrap.com
- **Font Awesome**: https://fontawesome.com

## 🎯 Next Steps

1. ✅ Customize content with your information
2. ✅ Update images with your photos
3. ✅ Change admin credentials
4. ✅ Configure email settings
5. ✅ Test all forms
6. ✅ Deploy to hosting service

## 📚 File Overview

```
khr1/
├── index.html          # Main website
├── css/               # Styling
│   ├── styles.css
│   ├── responsive.css
│   └── animations.css
├── js/                # JavaScript
│   └── main.js
├── admin/             # Admin panel
│   ├── login.html
│   └── dashboard.html
├── backend/           # Python backend
│   ├── app.py
│   └── requirements.txt
├── images/            # Images folder
└── README.md          # Full documentation
```

## ⚙️ Initial Configuration

Before going live, update:

1. **Personal Information**
   - Name, contact details
   - Social media links
   - Biography content

2. **Email Settings**
   - SMTP configuration
   - Email addresses
   - Sender name

3. **Security**
   - Change admin password
   - Update SECRET_KEY
   - Enable HTTPS

4. **Branding**
   - Colors (if needed)
   - Logo (if needed)
   - Font (if needed)

## ✨ Pro Tips

1. **Mobile First**: Test on mobile before desktop
2. **Optimization**: Compress images before upload
3. **SEO**: Add meta tags in `<head>`
4. **Analytics**: Add Google Analytics ID
5. **Backup**: Regular database backups
6. **Monitoring**: Set up error logging
7. **Testing**: Test forms before going live

## 🎉 You're Ready!

Your website is now set up and ready to use. Start by:
1. Customizing content
2. Testing all features
3. Sharing with users
4. Monitoring submissions

Happy serving! 🚀

---

For detailed documentation, see `README.md`
