# ✅ TESTING & VALIDATION GUIDE

## Frontend Testing

### HTML Validation

#### index.html Checklist
- [ ] All sections present
  - [ ] Navigation bar with logo
  - [ ] Hero section
  - [ ] About section
  - [ ] Timeline section
  - [ ] Vision section
  - [ ] Focus areas section
  - [ ] Community impact section
  - [ ] News section
  - [ ] Media section
  - [ ] Testimonials section
  - [ ] Gallery section
  - [ ] Forms section
  - [ ] Footer

- [ ] All forms present
  - [ ] Complaint form (8 fields)
  - [ ] Feedback form (rating + 4 fields)
  - [ ] Skills registration form (9 fields)
  - [ ] Contact form (5 fields)

- [ ] All links working
  - [ ] Internal navigation links
  - [ ] Social media links
  - [ ] External links
  - [ ] Email links

- [ ] All images loading
  - [ ] Logo image
  - [ ] Hero background
  - [ ] Section images
  - [ ] Gallery images
  - [ ] Testimonial avatars

#### Semantic HTML Check
- [ ] Proper heading hierarchy (h1, h2, h3)
- [ ] Semantic tags used (header, nav, main, section, article, footer)
- [ ] Alt text on all images
- [ ] Form labels properly associated
- [ ] ARIA labels where needed
- [ ] Skip navigation links

### CSS Validation

#### styles.css
- [ ] CSS custom properties defined
- [ ] Color scheme correct
  - [ ] Primary color: #ff9500 (saffron)
  - [ ] Secondary color: #003d7a (blue)
  - [ ] Text colors contrast good
- [ ] All components styled
  - [ ] Buttons
  - [ ] Cards
  - [ ] Forms
  - [ ] Navigation
  - [ ] Sections
- [ ] Responsive design basics applied
- [ ] Font sizes proper
- [ ] Line heights readable

#### responsive.css
- [ ] Mobile breakpoint (480px)
  - [ ] Navigation collapses
  - [ ] Forms stack vertically
  - [ ] Images scale properly
  - [ ] Text readable
- [ ] Tablet breakpoint (768px)
  - [ ] 2-column layouts
  - [ ] Navigation adjusted
  - [ ] Cards responsive
- [ ] Desktop layout
  - [ ] Multi-column layouts
  - [ ] Full width utilized
- [ ] Extra small devices (360px)
  - [ ] All content visible
  - [ ] No horizontal scroll
- [ ] Landscape orientation

#### animations.css
- [ ] All animations defined
- [ ] Timing is smooth
- [ ] No janky transitions
- [ ] Performance optimized
  - [ ] Using will-change
  - [ ] Using translateZ(0)
  - [ ] GPU acceleration enabled
- [ ] Accessibility respected
  - [ ] prefers-reduced-motion checked

### JavaScript Testing

#### main.js Functionality
- [ ] Navigation menu
  - [ ] Hamburger toggle works
  - [ ] Dropdown menus open/close
  - [ ] Sticky navbar on scroll
  - [ ] Mobile menu closes on link click
  
- [ ] Form handling
  - [ ] All 4 forms submit
  - [ ] Validation works
    - [ ] Required fields checked
    - [ ] Email format validated
    - [ ] Phone 10 digits validated
  - [ ] Success messages show
  - [ ] Error messages display
  
- [ ] Data persistence
  - [ ] localStorage saves data
  - [ ] Data persists on reload
  - [ ] Admin can view submitted data
  
- [ ] Animations
  - [ ] AOS scroll animations work
  - [ ] Page transitions smooth
  - [ ] No visual glitches

- [ ] Utilities
  - [ ] Back-to-top button works
  - [ ] Smooth scrolling works
  - [ ] Keyboard navigation works
  - [ ] Focus management good

### Responsive Design Testing

#### Mobile (375px)
```
Windows:
- Ctrl + Shift + I (open DevTools)
- iPhone 12 Pro (390x844)
- iPhone 12 (360x800)

Expected Results:
- ✓ All content visible
- ✓ No horizontal scroll
- ✓ Touch targets (44x44px min)
- ✓ Menu accessible
- ✓ Forms usable
```

#### Tablet (768px)
```
- iPad (768x1024)
- Galaxy Tab (810x1080)

Expected Results:
- ✓ 2-column layouts
- ✓ Readable text
- ✓ Images scale properly
- ✓ Forms accessible
```

#### Desktop (1920px)
```
- Full HD (1920x1080)
- 2K (2560x1440)

Expected Results:
- ✓ Multi-column layouts
- ✓ Maximum width applied
- ✓ Proper spacing
- ✓ Professional appearance
```

### Browser Compatibility Testing

#### Chrome/Edge
Test on:
- [ ] Latest version
- [ ] Previous version
- [ ] Windows, Mac, Linux

#### Firefox
Test on:
- [ ] Latest version
- [ ] Previous version

#### Safari
Test on:
- [ ] Latest version
- [ ] iOS Safari

#### Mobile Browsers
Test on:
- [ ] Chrome (Android)
- [ ] Safari (iOS)
- [ ] Firefox (Android)

---

## Backend Testing

### Flask Application Testing

#### Basic Functionality
```bash
# Start the Flask server
python backend/app.py

# Expected output:
# * Running on http://127.0.0.1:5000
# * Debug mode: on (or off for production)
```

#### API Endpoint Testing

Use curl, Postman, or Thunder Client:

##### 1. Test Complaint Form
```bash
POST http://localhost:5000/api/complaint
Content-Type: application/json

{
  "name": "Test User",
  "phone": "9876543210",
  "email": "test@example.com",
  "area": "Quthbullapur",
  "category": "complaint",
  "subject": "Test Complaint",
  "message": "This is a test complaint",
  "address": "Test Address"
}

# Expected Response:
{
  "success": true,
  "message": "Complaint submitted successfully",
  "reference_number": "CMP-202603031234"
}
```

##### 2. Test Feedback Form
```bash
POST http://localhost:5000/api/feedback
Content-Type: application/json

{
  "name": "Test User",
  "email": "test@example.com",
  "phone": "9876543210",
  "category": "service",
  "rating": 5,
  "message": "Great service!"
}

# Expected Response:
{
  "success": true,
  "message": "Thank you for your feedback!"
}
```

##### 3. Test Skills Registration
```bash
POST http://localhost:5000/api/skills-registration
Content-Type: application/json

{
  "name": "Test User",
  "phone": "9876543210",
  "email": "test@example.com",
  "dob": "2005-01-15",
  "education": "12th Pass",
  "institution": "Test School",
  "location": "District",
  "city": "Quthbullapur",
  "motivation": "To learn new skills"
}

# Expected Response:
{
  "success": true,
  "message": "Registration received!"
}
```

##### 4. Test Contact Form
```bash
POST http://localhost:5000/api/contact
Content-Type: application/json

{
  "name": "Test User",
  "email": "test@example.com",
  "phone": "9876543210",
  "subject": "Contact",
  "message": "Test message"
}

# Expected Response:
{
  "success": true,
  "message": "Message received!"
}
```

##### 5. Health Check
```bash
GET http://localhost:5000/api/status

# Expected Response:
{
  "status": "ok",
  "message": "API is running"
}
```

### Database Testing

#### Database File Check
```bash
# Check if database exists
ls -la backend/khr_database.db  # Linux/Mac
dir backend\khr_database.db     # Windows

# Expected: File should exist with size > 0 KB
```

#### Database Content Verification
```bash
# Using Python to check database
python
>>> from backend.app import db, Complaint, Feedback, SkillsRegistration, Contact
>>> from flask import Flask
>>> app = Flask(__name__)
>>> app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///backend/khr_database.db'
>>> with app.app_context():
...     complaints = Complaint.query.all()
...     print(f"Complaints: {len(complaints)}")
...     feedback = Feedback.query.all()
...     print(f"Feedback: {len(feedback)}")
```

### Email Testing

#### Test Email Sending
```python
# Add to backend/app.py to test email
if __name__ == '__main__':
    with app.app_context():
        send_complaint_confirmation_email(
            name="Test User",
            email="your_email@gmail.com",
            reference_number="TEST-001"
        )
```

#### Expected Results
- [ ] Email received in inbox
- [ ] Email contains reference number
- [ ] Email has proper formatting
- [ ] Links are clickable
- [ ] Branding matches website

---

## Admin Panel Testing

### Admin Login Testing
- [ ] Login page loads
- [ ] Can login with demo credentials
  - Username: khr
  - Password: khr@123
- [ ] Session maintains on navigation
- [ ] Page redirects on logout
- [ ] Remember me checkbox works

### Admin Dashboard Testing
- [ ] Dashboard loads after login
- [ ] Statistics cards display
  - [ ] Complaint count
  - [ ] Feedback count
  - [ ] Registration count
  - [ ] Contact count

#### Complaints Tab
- [ ] All complaints display
- [ ] Filter buttons work (All/Pending/Resolved)
- [ ] Click complaint shows modal
- [ ] Modal displays full details
- [ ] Status can be updated
- [ ] Delete works
- [ ] Pagination works (if > 10 items)

#### Feedback Tab
- [ ] All feedback displays
- [ ] Star rating shows
- [ ] Modal displays full feedback
- [ ] Delete works
- [ ] Sorting works

#### Skills Tab
- [ ] All registrations display
- [ ] Filter buttons work (All/Pending/Approved)
- [ ] Modal shows full details
- [ ] Status can be updated
- [ ] Email sending works

#### Contacts Tab
- [ ] All contacts display
- [ ] Modal shows full message
- [ ] Delete works
- [ ] Status tracking works

---

## Security Testing

### Input Validation
- [ ] Test with special characters: `<script>alert('xss')</script>`
- [ ] Test with long strings (1000+ chars)
- [ ] Test with SQL injection: `'; DROP TABLE complaints; --`
- [ ] Test with invalid emails
- [ ] Test with invalid phone numbers
- [ ] Test empty fields

Expected: All rejected gracefully with error messages

### CORS Testing
```bash
# Test from different origin
curl -H "Origin: http://example.com" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -X OPTIONS http://localhost:5000/api/complaint

# Expected: CORS headers returned
```

### Authentication Testing
- [ ] Cannot access admin without login
- [ ] Session expires properly
- [ ] Cannot modify others' submissions
- [ ] Admin credentials are secure

---

## Performance Testing

### Load Time Testing
```bash
# Using Google Lighthouse
# Open DevTools → Lighthouse → Generate Report

Expected Scores:
- Performance: > 80
- Accessibility: > 90
- Best Practices: > 85
- SEO: > 90
```

### Image Optimization
- [ ] All images optimized (< 500KB each)
- [ ] Images load fast
- [ ] Responsive images serve correct size
- [ ] Lazy loading works

### CSS/JS Bundle Size
- [ ] Minified CSS < 100KB
- [ ] Minified JS < 100KB
- [ ] Total webpage < 500KB

---

## Accessibility Testing

### Keyboard Navigation
- [ ] Tab through all interactive elements
- [ ] Focus visible on all elements
- [ ] Can submit forms with keyboard
- [ ] Escape key closes modals
- [ ] Enter key submits forms

### Screen Reader Testing
Using NVDA (Windows), JAWS, or VoiceOver (Mac):
- [ ] Navigation announced correctly
- [ ] Form labels read
- [ ] Images have alt text
- [ ] Buttons are labeled
- [ ] Links are descriptive

### Color Contrast
- [ ] Text: contrast ratio > 4.5:1
- [ ] Large text: contrast ratio > 3:1
- [ ] UI components: contrast ratio > 3:1

### Text Sizing
- [ ] 200% zoom - content readable
- [ ] Font size increase - layout stable

---

## Cross-Browser Testing Matrix

| Feature | Chrome | Firefox | Safari | Edge | Mobile |
|---------|--------|---------|--------|------|--------|
| HTML Rendering | ✓ | ✓ | ✓ | ✓ | ✓ |
| CSS Styling | ✓ | ✓ | ✓ | ✓ | ✓ |
| JavaScript | ✓ | ✓ | ✓ | ✓ | ✓ |
| Forms | ✓ | ✓ | ✓ | ✓ | ✓ |
| Animations | ✓ | ✓ | ✓ | ✓ | ✓ |
| Images | ✓ | ✓ | ✓ | ✓ | ✓ |
| Responsiveness | ✓ | ✓ | ✓ | ✓ | ✓ |
| API Calls | ✓ | ✓ | ✓ | ✓ | ✓ |
| Email | ✓ | ✓ | ✓ | ✓ | N/A |

---

## Test Report Template

```
PROJECT: Kolan Hanmanth Reddy Political Leader Website
DATE: [Date]
TESTER: [Your Name]

Frontend TESTING
- HTML Validation: PASS/FAIL
- CSS Validation: PASS/FAIL
- JavaScript: PASS/FAIL
- Responsive Design: PASS/FAIL
- Icons/Images: PASS/FAIL

BACKEND TESTING
- Flask Server: PASS/FAIL
- API Endpoints: PASS/FAIL
- Database: PASS/FAIL
- Email System: PASS/FAIL

ADMIN PANEL TESTING
- Login: PASS/FAIL
- Dashboard: PASS/FAIL
- CRUD Operations: PASS/FAIL

COMPATIBILITY
- Chrome: PASS/FAIL
- Firefox: PASS/FAIL
- Safari: PASS/FAIL
- Mobile: PASS/FAIL

ISSUES FOUND:
[List any issues]

FIXES APPLIED:
[List fixes]

OVERALL STATUS: PASS/FAIL

APPROVED BY: [Name]
DATE: [Date]
```

---

## Common Issues & Solutions

### Form Not Submitting
```
Issue: Form appears to submit but no data saved
Solution:
1. Check browser console (F12)
2. Check Flask server logs
3. Verify localStorage (DevTools > Application > LocalStorage)
4. Ensure backend is running on port 5000
```

### Images Not Loading
```
Issue: Images show broken icon
Solution:
1. Verify image files exist in images/ folder
2. Check image path in index.html
3. Check browser network tab (F12)
4. Verify image file format is supported (JPG, PNG, GIF, WebP)
```

### Responsive Design Broken
```
Issue: Layout wrong on mobile
Solution:
1. Check viewport meta tag in HTML
2. Verify media queries in CSS
3. Check for hardcoded pixel widths
4. Test with DevTools device emulation
```

### Admin Dashboard Not Loading
```
Issue: Dashboard shows blank or error
Solution:
1. Check browser console errors
2. Verify login was successful
3. Check localStorage data
4. Clear browser cache and reload
```

---

## Sign-Off Checklist

- [ ] All tests completed
- [ ] No critical bugs found
- [ ] Performance acceptable
- [ ] Security verified
- [ ] Accessibility checked
- [ ] Documentation complete
- [ ] Code reviewed
- [ ] Ready for deployment

**Test Completed By**: ________________  
**Date**: ________________  
**Status**: ✅ APPROVED / ❌ NEEDS FIXES

---

**Great job testing the website! 🎉**

Ready for deployment? Check DEPLOYMENT_CHECKLIST.md
