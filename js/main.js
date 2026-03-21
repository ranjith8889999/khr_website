/* ============================================
   MAIN JAVASCRIPT - Kolan Hanmanth Reddy Website
   ============================================ */

// Initialize AOS (Animate On Scroll)
document.addEventListener('DOMContentLoaded', function() {
    AOS.init({
        duration: 800,
        easing: 'ease-in-out-cubic',
        once: true,
        offset: 100
    });
});

/* ============================================
   NAVIGATION & MENU
   ============================================ */

const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');
const navLinks = document.querySelectorAll('.nav-link');
const navbar = document.getElementById('navbar');
const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
const dropdownLinks = document.querySelectorAll('.dropdown-link');

// Helper function to close mobile menu
function closeMobileMenu() {
    if (window.innerWidth <= 768) {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.classList.remove('active');
        });
    }
}

// Hamburger menu toggle
hamburger.addEventListener('click', function() {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close menu when regular nav link is clicked
navLinks.forEach(link => {
    // Skip dropdown toggles - they have their own handler
    if (!link.classList.contains('dropdown-toggle')) {
        link.addEventListener('click', function() {
            closeMobileMenu();
        });
    }
});

// Dropdown menu toggle on mobile
dropdownToggles.forEach(toggle => {
    toggle.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            e.preventDefault();
            e.stopPropagation();
            const dropdownMenu = this.nextElementSibling;
            const isActive = dropdownMenu.classList.contains('active');
            
            // Close all other dropdowns
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.classList.remove('active');
            });
            
            // Toggle current dropdown
            if (!isActive) {
                dropdownMenu.classList.add('active');
            }
        }
    });
});

// Close menu when dropdown link is clicked
dropdownLinks.forEach(link => {
    link.addEventListener('click', function() {
        closeMobileMenu();
    });
});

// Sticky navbar
window.addEventListener('scroll', function() {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

/* ============================================
   BACK TO TOP BUTTON
   ============================================ */

const backToTop = document.getElementById('backToTop');

window.addEventListener('scroll', function() {
    if (window.pageYOffset > 300) {
        backToTop.classList.add('show');
    } else {
        backToTop.classList.remove('show');
    }
});

backToTop.addEventListener('click', function() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

/* ============================================
   FORM HANDLING
   ============================================ */

// Helper function to show messages
function showMessage(formId, message, type) {
    const form = document.getElementById(formId);
    let messageEl = form.querySelector('.success-message, .error-message');
    
    if (!messageEl) {
        messageEl = document.createElement('div');
        messageEl.className = type === 'success' ? 'success-message' : 'error-message';
        form.insertBefore(messageEl, form.firstChild);
    }
    
    messageEl.textContent = message;
    messageEl.classList.add('show');
    
    setTimeout(() => {
        messageEl.classList.remove('show');
    }, 5000);
}

// Helper function to validate email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Helper function to validate phone
function isValidPhone(phone) {
    const phoneRegex = /^[0-9]{10}$/;
    return phoneRegex.test(phone.replace(/[^0-9]/g, ''));
}

// Complaint Form Handler
const complaintForm = document.getElementById('complaintForm');
if (complaintForm) {
    complaintForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Validate form
        const name = document.getElementById('complaint-name').value.trim();
        const phone = document.getElementById('complaint-phone').value.trim();
        const email = document.getElementById('complaint-email').value.trim();
        const area = document.getElementById('complaint-area').value.trim();
        const category = document.getElementById('complaint-category').value;
        const subject = document.getElementById('complaint-subject').value.trim();
        const message = document.getElementById('complaint-message').value.trim();
        const address = document.getElementById('complaint-address').value.trim();
        
        if (!name || !phone || !email || !area || !category || !subject || !message || !address) {
            showMessage('complaintForm', 'Please fill all required fields', 'error');
            return;
        }
        
        if (!isValidEmail(email)) {
            showMessage('complaintForm', 'Please enter a valid email address', 'error');
            return;
        }
        
        if (!isValidPhone(phone)) {
            showMessage('complaintForm', 'Please enter a valid 10-digit phone number', 'error');
            return;
        }
        
        // Submit form
        try {
            const formData = {
                name, phone, email, area, category, subject, message, address
            };
            
            // Show loading
            const submitBtn = complaintForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';
            
            // Call backend API
            const result = await submitComplaintToAPI(formData);
            
            // Re-enable button
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
            
            if (result.success) {
                complaintForm.reset();
                const details = `
                    <strong>Reference Number:</strong>
                    <p style="font-size: 18px; color: var(--primary-color); font-weight: bold; margin: 10px 0;">${result.reference_number}</p>
                    <p style="font-size: 13px; color: #666;">Please save this reference number for tracking your complaint. A confirmation email has been sent to ${email}.</p>
                `;
                showModal('success', 'Complaint Submitted Successfully!', result.message, details);
            } else {
                showModal('error', 'Submission Failed', result.message || 'Unable to submit complaint. Please try again later.');
            }
            
        } catch (error) {
            console.error('Error submitting complaint:', error);
            showModal('error', 'Error', 'Failed to submit complaint. Please check your connection and try again.');
        }
    });
}

// Feedback Form Handler
const feedbackForm = document.getElementById('feedbackForm');
if (feedbackForm) {
    feedbackForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const name = document.getElementById('feedback-name').value.trim();
        const email = document.getElementById('feedback-email').value.trim();
        const phone = document.getElementById('feedback-phone').value.trim();
        const category = document.getElementById('feedback-category').value;
        const rating = document.querySelector('input[name="rating"]:checked');
        const message = document.getElementById('feedback-message').value.trim();
        
        if (!name || !email || !category || !rating || !message) {
            showMessage('feedbackForm', 'Please fill all required fields', 'error');
            return;
        }
        
        if (!isValidEmail(email)) {
            showMessage('feedbackForm', 'Please enter a valid email address', 'error');
            return;
        }
        
        if (phone && !isValidPhone(phone)) {
            showMessage('feedbackForm', 'Please enter a valid 10-digit phone number', 'error');
            return;
        }
        
        try {
            const formData = {
                name, email, phone, category, rating: rating.value, message
            };
            
            // Show loading
            const submitBtn = feedbackForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';
            
            // Call backend API
            const result = await submitFeedbackToAPI(formData);
            
            // Re-enable button
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
            
            if (result.success) {
                feedbackForm.reset();
                // Reset star rating
                document.querySelectorAll('.rating-stars input').forEach(input => {
                    input.checked = false;
                });
                
                const details = `
                    <p style="font-size: 14px; color: #666;">A confirmation email has been sent to ${email}. Thank you for helping us improve!</p>
                `;
                showModal('success', 'Thank You for Your Feedback!', result.message, details);
            } else {
                showModal('error', 'Submission Failed', result.message || 'Unable to submit feedback. Please try again later.');
            }
            
        } catch (error) {
            console.error('Error submitting feedback:', error);
            showModal('error', 'Error', 'Failed to submit feedback. Please check your connection and try again.');
        }
    });
}

// Skills Registration Form Handler
const skillsForm = document.getElementById('skillsForm');
if (skillsForm) {
    skillsForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const name = document.getElementById('skills-name').value.trim();
        const dob = document.getElementById('skills-dob').value;
        const email = document.getElementById('skills-email').value.trim();
        const phone = document.getElementById('skills-phone').value.trim();
        const education = document.getElementById('skills-education').value;
        const institution = document.getElementById('skills-institution').value.trim();
        const location = document.getElementById('skills-location').value.trim();
        const city = document.getElementById('skills-city').value.trim();
        const motivation = document.getElementById('skills-motivation').value.trim();
        
        if (!name || !dob || !email || !phone || !education || !location || !city || !motivation) {
            showMessage('skillsForm', 'Please fill all required fields', 'error');
            return;
        }
        
        if (!isValidEmail(email)) {
            showMessage('skillsForm', 'Please enter a valid email address', 'error');
            return;
        }
        
        if (!isValidPhone(phone)) {
            showMessage('skillsForm', 'Please enter a valid 10-digit phone number', 'error');
            return;
        }
        
        try {
            const formData = {
                name, dob, email, phone, education, institution, location, city, motivation
            };
            
            // Show loading
            const submitBtn = skillsForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';
            
            // Call backend API
            const result = await submitSkillsToAPI(formData);
            
            // Re-enable button
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
            
            if (result.success) {
                skillsForm.reset();
                const details = `
                    <p style="font-size: 14px; color: #666;">A confirmation email has been sent to ${email}. You will receive further updates about the skills development program soon.</p>
                `;
                showModal('success', 'Registration Successful!', result.message, details);
            } else {
                showModal('error', 'Registration Failed', result.message || 'Unable to submit registration. Please try again later.');
            }
            
        } catch (error) {
            console.error('Error submitting registration:', error);
            showModal('error', 'Error', 'Failed to submit registration. Please check your connection and try again.');
        }
    });
}

// Contact Form Handler
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const name = document.getElementById('contact-name').value.trim();
        const email = document.getElementById('contact-email').value.trim();
        const phone = document.getElementById('contact-phone').value.trim();
        const subject = document.getElementById('contact-subject').value.trim();
        const message = document.getElementById('contact-message').value.trim();
        
        if (!name || !email || !subject || !message) {
            showMessage('contactForm', 'Please fill all required fields', 'error');
            return;
        }
        
        if (!isValidEmail(email)) {
            showMessage('contactForm', 'Please enter a valid email address', 'error');
            return;
        }
        
        if (phone && !isValidPhone(phone)) {
            showMessage('contactForm', 'Please enter a valid 10-digit phone number', 'error');
            return;
        }
        
        try {
            const formData = {
                name, email, phone, subject, message
            };
            
            // Show loading
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = 'Sending...';
            
            // Call backend API
            const result = await submitContactToAPI(formData);
            
            // Re-enable button
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
            
            if (result.success) {
                contactForm.reset();
                const details = `
                    <p style="font-size: 14px; color: #666;">A confirmation email has been sent to ${email}. We will get back to you as soon as possible.</p>
                `;
                showModal('success', 'Message Sent Successfully!', result.message, details);
            } else {
                showModal('error', 'Failed to Send Message', result.message || 'Unable to send message. Please try again later.');
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            showModal('error', 'Error', 'Failed to send message. Please check your connection and try again.');
        }
    });
}

/* ============================================
   MODAL FUNCTIONS
   ============================================ */

function showModal(type, title, message, details = null) {
    const modal = document.getElementById('responseModal');
    const modalIcon = document.getElementById('modalIcon');
    const modalTitle = document.getElementById('modalTitle');
    const modalMessage = document.getElementById('modalMessage');
    const modalDetails = document.getElementById('modalDetails');
    const modalCloseBtn = document.getElementById('modalCloseBtn');
    
    // Set icon type
    modalIcon.className = 'modal-icon ' + type;
    
    // Set content
    modalTitle.textContent = title;
    modalMessage.textContent = message;
    
    // Set details if provided
    if (details) {
        modalDetails.innerHTML = details;
        modalDetails.classList.add('show');
    } else {
        modalDetails.classList.remove('show');
    }
    
    // Show modal
    modal.style.display = 'block';
    setTimeout(() => modal.classList.add('active'), 10);
    
    // Close button handler
    modalCloseBtn.onclick = () => closeModal();
    
    // Close on overlay click
    modal.querySelector('.modal-overlay').onclick = () => closeModal();
}

function closeModal() {
    const modal = document.getElementById('responseModal');
    modal.classList.remove('active');
    setTimeout(() => modal.style.display = 'none', 300);
}

/* ============================================
   API CALL FUNCTIONS
   ============================================ */

async function submitComplaintToAPI(data) {
    const response = await fetch('/api/complaint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    return await response.json();
}

async function submitFeedbackToAPI(data) {
    const response = await fetch('/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    return await response.json();
}

async function submitSkillsToAPI(data) {
    const response = await fetch('/api/skills-registration', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    return await response.json();
}

async function submitContactToAPI(data) {
    const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    return await response.json();
}

/* ============================================
   LIGHTBOX INITIALIZATION
   ============================================ */

// Lightbox is initialized with lightbox2 library
// Configuration happens automatically for elements with data-lightbox attribute

/* ============================================
   UTILITIES
   ============================================ */

// Smooth scroll for anchor links (enhanced)
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#' && document.querySelector(href)) {
            e.preventDefault();
            const element = document.querySelector(href);
            element.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading state to buttons
document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', function() {
        if (this.type === 'submit' && this.closest('form')) {
            this.style.opacity = '0.7';
            this.style.pointerEvents = 'none';
            setTimeout(() => {
                this.style.opacity = '1';
                this.style.pointerEvents = 'auto';
            }, 2000);
        }
    });
});

// Close mobile menu when window is resized
window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    }
});

// Prevent form submission if needed
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', function(e) {
        // Validation happens in specific form handlers
    });
});

/* ============================================
   PERFORMANCE OPTIMIZATIONS
   ============================================ */

// Lazy load images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src || img.src;
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// Service Worker Registration (for offline support)
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(err => {
        console.log('Service Worker registration failed:', err);
    });
}

/* ============================================
   ACCESSIBILITY ENHANCEMENTS
   ============================================ */

// Keyboard navigation for dropdowns
dropdownToggles.forEach(toggle => {
    toggle.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            this.click();
        }
    });
});

// Set focus management
document.querySelectorAll('input, textarea, button, a[href]').forEach(el => {
    el.addEventListener('focus', function() {
        this.style.outline = '2px solid var(--primary-color)';
        this.style.outlineOffset = '2px';
    });
    
    el.addEventListener('blur', function() {
        this.style.outline = '';
    });
});

/* ============================================
   COMMUNITY IMPACT LOADING
   ============================================ */

// Global variables for community impact
let allCommunityImpacts = [];
let displayedImpacts = 0;
const INITIAL_DISPLAY_COUNT = 6;

// Load community impact from database
async function loadCommunityImpacts() {
    try {
        const response = await fetch('/api/community-impacts');
        const result = await response.json();
        
        if (result.success) {
            allCommunityImpacts = result.data;
            displayCommunityImpacts(INITIAL_DISPLAY_COUNT);
            
            // Show/hide load more button
            const loadMoreBtn = document.getElementById('loadMoreBtn');
            if (allCommunityImpacts.length > INITIAL_DISPLAY_COUNT) {
                loadMoreBtn.style.display = 'inline-flex';
            } else {
                loadMoreBtn.style.display = 'none';
            }
        }
    } catch (error) {
        console.error('Error loading community impacts:', error);
        showFallbackCommunityImpacts();
    }
}

// Display community impacts up to a certain count
function displayCommunityImpacts(count) {
    const grid = document.getElementById('communityGrid');
    grid.innerHTML = '';
    
    const impactsToShow = allCommunityImpacts.slice(0, count);
    displayedImpacts = count;
    
    impactsToShow.forEach((impact, index) => {
        const card = document.createElement('div');
        card.className = 'community-card';
        card.setAttribute('data-aos', 'fade-up');
        card.setAttribute('data-aos-delay', (index % 6) * 100);
        
        card.innerHTML = `
            <div class="community-image">
                <img src="${impact.image_url}" alt="${impact.title}" onerror="this.src='images/placeholder.jpg'">
                <div class="overlay">
                    <span class="overlay-title">${impact.overlay_title}</span>
                </div>
            </div>
            <div class="community-content">
                <h3>${impact.title}</h3>
                <p>${impact.description}</p>
                <span class="badge">${impact.badge}</span>
            </div>
        `;
        
        grid.appendChild(card);
    });
    
    // Re-initialize AOS for new elements
    if (typeof AOS !== 'undefined') {
        AOS.refresh();
    }
    
    // Update load more button
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if (displayedImpacts >= allCommunityImpacts.length) {
        loadMoreBtn.style.display = 'none';
    } else {
        loadMoreBtn.style.display = 'inline-flex';
    }
}

// Show fallback static content if API fails
function showFallbackCommunityImpacts() {
    const grid = document.getElementById('communityGrid');
    grid.innerHTML = `
        <div class="community-card" data-aos="fade-up">
            <div class="community-image">
                <img src="images/hq720.jpg" alt="Free Medical Camp">
                <div class="overlay">
                    <span class="overlay-title">Medical Camps</span>
                </div>
            </div>
            <div class="community-content">
                <h3>Free Medical Camps</h3>
                <p>Organized and participated in free medical camps in Girinagar and other areas, providing health checkups and medicines to economically disadvantaged residents.</p>
                <span class="badge">Healthcare</span>
            </div>
        </div>
        
        <div class="community-card" data-aos="fade-up">
            <div class="community-image">
                <img src="images/588266246_1428314585529785_7601836298558718966_n.jpg" alt="Community Engagement">
                <div class="overlay">
                    <span class="overlay-title">Community Engagement</span>
                </div>
            </div>
            <div class="community-content">
                <h3>Grassroots Community Engagement</h3>
                <p>Sustained, visible engagement with residents through local meetings, neighborhood events, and public forums to address community concerns.</p>
                <span class="badge">Outreach</span>
            </div>
        </div>
        
        <div class="community-card" data-aos="fade-up">
            <div class="community-image">
                <img src="images/587850980_1428313072196603_8882777926802737058_n.jpg" alt="Youth Leadership">
                <div class="overlay">
                    <span class="overlay-title">Youth Programs</span>
                </div>
            </div>
            <div class="community-content">
                <h3>Youth Volunteer Leadership</h3>
                <p>Leadership and mobilization of youth volunteers through Sevadal organization to support community welfare programs and local development.</p>
                <span class="badge">Youth</span>
            </div>
        </div>
        
        <div class="community-card" data-aos="fade-up">
            <div class="community-image">
                <img src="images/608145349_1456202209407689_6360395274668037289_n.jpg" alt="Blood Donation Camp">
                <div class="overlay">
                    <span class="overlay-title">Health Awareness</span>
                </div>
            </div>
            <div class="community-content">
                <h3>Health & Welfare Initiatives</h3>
                <p>Active participation in blood donation drives and health awareness programs to promote community wellness and social responsibility.</p>
                <span class="badge">Wellness</span>
            </div>
        </div>
    `;
    
    // Hide load more button on fallback
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if (loadMoreBtn) {
        loadMoreBtn.style.display = 'none';
    }
}

// Load more button handler
document.addEventListener('DOMContentLoaded', function() {
    // Load community impacts on page load
    loadCommunityImpacts();
    
    // Add load more button handler
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function() {
            displayCommunityImpacts(allCommunityImpacts.length);
        });
    }

    // Load news on page load
    loadNews();
    
    // Add news load more button handler
    const loadMoreNewsBtn = document.getElementById('loadMoreNewsBtn');
    if (loadMoreNewsBtn) {
        loadMoreNewsBtn.addEventListener('click', function() {
            displayNews(allNews.length);
        });
    }
});

/* ============================================
   NEWS LOADING
   ============================================ */

// Global variables for news
let allNews = [];
let displayedNews = 0;
const INITIAL_NEWS_COUNT = 4;

// Load news from database
async function loadNews() {
    try {
        const response = await fetch('/api/news');
        const result = await response.json();
        
        if (result.success) {
            allNews = result.data;
            displayNews(INITIAL_NEWS_COUNT);
            
            // Show/hide load more button
            const loadMoreNewsBtn = document.getElementById('loadMoreNewsBtn');
            if (allNews.length > INITIAL_NEWS_COUNT) {
                loadMoreNewsBtn.style.display = 'inline-flex';
            } else {
                loadMoreNewsBtn.style.display = 'none';
            }
        }
    } catch (error) {
        console.error('Error loading news:', error);
        showFallbackNews();
    }
}

// Helper function to format news date for display
function formatNewsDate(dateStr) {
    // If date is in YYYY-MM-DD format, convert to readable format
    if (dateStr && dateStr.match(/^\d{4}-\d{2}-\d{2}$/)) {
        const date = new Date(dateStr + 'T00:00:00');
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return date.toLocaleDateString('en-US', options);
    }
    // Return as-is if already in text format (e.g., "March 2024")
    return dateStr;
}

// Display news up to a certain count
function displayNews(count) {
    const grid = document.getElementById('newsGrid');
    grid.innerHTML = '';
    
    const newsToShow = allNews.slice(0, count);
    displayedNews = count;
    
    newsToShow.forEach((news, index) => {
        const article = document.createElement('article');
        article.className = 'news-card';
        article.setAttribute('data-aos', 'fade-up');
        article.setAttribute('data-aos-delay', (index % 4) * 100);
        
        // Check if news has image
        let imageHTML = '';
        if (news.image_url && news.image_url.trim() !== '') {
            imageHTML = `<div class="news-image" style="margin-bottom: 15px;">
                <img src="${news.image_url}" alt="${news.title}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px;">
            </div>`;
        }
        
        // Check if news has external link
        const hasLink = news.link_url && news.link_url.trim() !== '';
        const readMoreLink = hasLink 
            ? `<a href="${news.link_url}" target="_blank" class="read-more">Read More <i class="fas fa-arrow-right"></i></a>`
            : `<a href="#" class="read-more" onclick="return false;" style="cursor: default; opacity: 0.5;">No link available</a>`;
        
        article.innerHTML = `
            ${imageHTML}
            <div class="news-header">
                <span class="news-date">${formatNewsDate(news.news_date)}</span>
                <span class="news-category">${news.category}</span>
            </div>
            <h3>${news.title}</h3>
            <p>${news.description}</p>
            ${readMoreLink}
        `;
        
        grid.appendChild(article);
    });
    
    // Re-initialize AOS for new elements
    if (typeof AOS !== 'undefined') {
        AOS.refresh();
    }
    
    // Update load more button
    const loadMoreNewsBtn = document.getElementById('loadMoreNewsBtn');
    if (displayedNews >= allNews.length) {
        loadMoreNewsBtn.style.display = 'none';
    } else {
        loadMoreNewsBtn.style.display = 'inline-flex';
    }
}

// Show fallback static content if API fails
function showFallbackNews() {
    const grid = document.getElementById('newsGrid');
    grid.innerHTML = `
        <article class="news-card" data-aos="fade-up">
            <div class="news-header">
                <span class="news-date">December 2023</span>
                <span class="news-category">Politics</span>
            </div>
            <h3>2023 Legislative Assembly Election</h3>
            <p>Contested Telangana Legislative Assembly election from Quthbullapur as INC candidate, garnering strong voter support and finishing as runner-up.</p>
            <a href="#" class="read-more">Read More <i class="fas fa-arrow-right"></i></a>
        </article>
        
        <article class="news-card" data-aos="fade-up">
            <div class="news-header">
                <span class="news-date">October 2023</span>
                <span class="news-category">Community</span>
            </div>
            <h3>Youth Join Congress in Quthbullapur</h3>
            <p>150 youths joined Indian National Congress in a show of support for inclusive development and grassroots leadership in Quthbullapur constituency.</p>
            <a href="#" class="read-more">Read More <i class="fas fa-arrow-right"></i></a>
        </article>
        
        <article class="news-card" data-aos="fade-up">
            <div class="news-header">
                <span class="news-date">October 2023</span>
                <span class="news-category">Community</span>
            </div>
            <h3>Community Group Meeting in HMT Colony</h3>
            <p>Met with Kurma Sangam community group in HMT Colony to listen to residents' concerns and discuss development initiatives for the area.</p>
            <a href="#" class="read-more">Read More <i class="fas fa-arrow-right"></i></a>
        </article>
        
        <article class="news-card" data-aos="fade-up">
            <div class="news-header">
                <span class="news-date">September 2023</span>
                <span class="news-category">Healthcare</span>
            </div>
            <h3>Free Medical Camp in Girinagar</h3>
            <p>Participated as chief guest in free medical camp providing health checkups and medicines to underprivileged residents of Girinagar area.</p>
            <a href="#" class="read-more">Read More <i class="fas fa-arrow-right"></i></a>
        </article>
    `;
    
    // Hide load more button on fallback
    const loadMoreNewsBtn = document.getElementById('loadMoreNewsBtn');
    if (loadMoreNewsBtn) {
        loadMoreNewsBtn.style.display = 'none';
    }
}

/* ============================================
   MEDIA & RECOGNITION
   ============================================ */

// Load media from database
async function loadMedia() {
    const mediaGrid = document.getElementById('mediaGrid');
    const mediaLoading = document.getElementById('mediaLoading');
    
    if (!mediaGrid || !mediaLoading) return;
    
    mediaLoading.style.display = 'flex';
    
    try {
        const response = await fetch('/api/media');
        const result = await response.json();
        
        if (result.success && result.data && result.data.length > 0) {
            displayMedia(result.data);
        } else {
            showFallbackMedia();
        }
    } catch (error) {
        console.error('Error loading media:', error);
        showFallbackMedia();
    } finally {
        mediaLoading.style.display = 'none';
    }
}

// Display media items
function displayMedia(mediaItems) {
    const grid = document.getElementById('mediaGrid');
    grid.innerHTML = '';
    
    mediaItems.forEach(item => {
        const mediaItem = document.createElement('div');
        mediaItem.className = 'media-item';
        mediaItem.setAttribute('data-aos', 'fade-up');
        
        mediaItem.innerHTML = `
            <div class="media-card">
                <h3><i class="${item.icon}"></i> ${item.title}</h3>
                <p>${item.description}</p>
                <a href="${item.link_url}" target="_blank" class="media-link">${item.link_text || 'Read Article'}</a>
            </div>
        `;
        
        grid.appendChild(mediaItem);
    });
    
    // Re-initialize AOS for new elements
    if (typeof AOS !== 'undefined') {
        AOS.refresh();
    }
}

// Show fallback static content if API fails
function showFallbackMedia() {
    const grid = document.getElementById('mediaGrid');
    grid.innerHTML = `
        <div class="media-item" data-aos="fade-up">
            <div class="media-card">
                <h3><i class="fas fa-newspaper"></i> The Hans India</h3>
                <p>Coverage of free medical camp participation in Girinagar area</p>
                <a href="https://www.thehansindia.com/telangana/quthubullapur-congress-in-charge-kolan-hanumanth-reddy-participates-in-medical-camp-853126" target="_blank" class="media-link">Read Article</a>
            </div>
        </div>
        <div class="media-item" data-aos="fade-up">
            <div class="media-card">
                <h3><i class="fas fa-facebook"></i> Official Social Media</h3>
                <p>Verified Facebook profile with community engagement and social service updates</p>
                <a href="https://www.facebook.com/kolanhanmanthreddy/" target="_blank" class="media-link">Visit Facebook</a>
            </div>
        </div>
        <div class="media-item" data-aos="fade-up">
            <div class="media-card">
                <h3><i class="fas fa-instagram"></i> Instagram</h3>
                <p>Photo updates from community programs and public engagement events</p>
                <a href="https://www.instagram.com/kolan.hanmanthreddy/" target="_blank" class="media-link">View Photos</a>
            </div>
        </div>
    `;
}

// Load media on page load
loadMedia();

/* ============================================
   TESTIMONIALS & SUCCESS STORIES
   ============================================ */

// Load testimonials from database
async function loadTestimonials() {
    const testimonialsGrid = document.getElementById('testimonialsGrid');
    const testimonialsLoading = document.getElementById('testimonialsLoading');
    
    if (!testimonialsGrid || !testimonialsLoading) return;
    
    testimonialsLoading.style.display = 'flex';
    
    try {
        const response = await fetch('/api/testimonials');
        const result = await response.json();
        
        if (result.success && result.data && result.data.length > 0) {
            displayTestimonials(result.data);
        } else {
            showFallbackTestimonials();
        }
    } catch (error) {
        console.error('Error loading testimonials:', error);
        showFallbackTestimonials();
    } finally {
        testimonialsLoading.style.display = 'none';
    }
}

// Display testimonials
function displayTestimonials(testimonials) {
    const grid = document.getElementById('testimonialsGrid');
    grid.innerHTML = '';
    
    testimonials.forEach(item => {
        const testimonialCard = document.createElement('div');
        testimonialCard.className = 'testimonial-card';
        testimonialCard.setAttribute('data-aos', 'fade-up');
        
        // Generate star rating
        const stars = '★'.repeat(item.rating) + '☆'.repeat(5 - item.rating);
        
        testimonialCard.innerHTML = `
            <div class="testimonial-header">
                <div class="testimonial-avatar">
                    <i class="${item.avatar_icon}"></i>
                </div>
                <div class="testimonial-info">
                    <h4>${item.name}</h4>
                    <p>${item.designation}, ${item.location}</p>
                    <div class="stars">
                        ${'<i class="fas fa-star"></i>'.repeat(item.rating)}
                    </div>
                </div>
            </div>
            <p class="testimonial-text">"${item.testimonial_text}"</p>
        `;
        
        grid.appendChild(testimonialCard);
    });
    
    // Re-initialize AOS for new elements
    if (typeof AOS !== 'undefined') {
        AOS.refresh();
    }
}

// Show fallback static content if API fails
function showFallbackTestimonials() {
    const grid = document.getElementById('testimonialsGrid');
    grid.innerHTML = `
        <div class="testimonial-card" data-aos="fade-up">
            <div class="testimonial-header">
                <div class="testimonial-avatar">
                    <i class="fas fa-user"></i>
                </div>
                <div class="testimonial-info">
                    <h4>Community Resident</h4>
                    <p>Girinagar Area</p>
                    <div class="stars">
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                    </div>
                </div>
            </div>
            <p class="testimonial-text">"The free medical camp organized by Kolan Hanmanth Reddy was a great help for our family. We got free consultation and medicines which would have been very expensive otherwise."</p>
        </div>
        <div class="testimonial-card" data-aos="fade-up">
            <div class="testimonial-header">
                <div class="testimonial-avatar">
                    <i class="fas fa-user"></i>
                </div>
                <div class="testimonial-info">
                    <h4>Youth Volunteer</h4>
                    <p>Quthbullapur Sevadal</p>
                    <div class="stars">
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                    </div>
                </div>
            </div>
            <p class="testimonial-text">"Kolan Sir's leadership has motivated us to engage in community service. The youth programs have given us a platform to contribute to society meaningfully."</p>
        </div>
    `;
}

// Load testimonials on page load
loadTestimonials();

/* ============================================
   PHOTO & VIDEO GALLERY
   ============================================ */

// Global variables for gallery
let allPhotos = [];
let allVideos = [];
let currentTab = 'photos';

// Load gallery from database
async function loadGallery() {
    const galleryLoading = document.getElementById('galleryLoading');
    
    if (!galleryLoading) return;
    
    galleryLoading.style.display = 'flex';
    
    try {
        const response = await fetch('/api/gallery');
        const result = await response.json();
        
        if (result.success && result.data && result.data.length > 0) {
            // Separate photos and videos
            allPhotos = result.data.filter(item => item.media_type === 'photo');
            allVideos = result.data.filter(item => item.media_type === 'video');
            
            // Display photos initially
            displayPhotos();
        } else {
            showFallbackGallery();
        }
    } catch (error) {
        console.error('Error loading gallery:', error);
        showFallbackGallery();
    } finally {
        galleryLoading.style.display = 'none';
    }
}

// Display photos
function displayPhotos() {
    const photosGrid = document.getElementById('photosGrid');
    photosGrid.innerHTML = '';
    
    if (allPhotos.length === 0) {
        photosGrid.innerHTML = '<p style="text-align: center; color: #666; grid-column: 1/-1;">No photos available</p>';
        return;
    }
    
    allPhotos.forEach(photo => {
        const photoItem = document.createElement('div');
        photoItem.className = 'gallery-item';
        photoItem.setAttribute('data-aos', 'fade-up');
        
        photoItem.innerHTML = `
            <a href="${photo.media_url}" data-lightbox="gallery" data-title="${photo.title}">
                <img src="${photo.media_url}" alt="${photo.description || photo.title}">
                <div class="gallery-overlay">
                    <i class="fas fa-search-plus"></i>
                </div>
            </a>
        `;
        
        photosGrid.appendChild(photoItem);
    });
    
    // Re-initialize AOS for new elements
    if (typeof AOS !== 'undefined') {
        AOS.refresh();
    }
}

// Display videos
function displayVideos() {
    const videosGrid = document.getElementById('videosGrid');
    videosGrid.innerHTML = '';
    
    if (allVideos.length === 0) {
        videosGrid.innerHTML = '<p style="text-align: center; color: #666; grid-column: 1/-1;">No videos available</p>';
        return;
    }
    
    allVideos.forEach(video => {
        const videoItem = document.createElement('div');
        videoItem.className = 'gallery-item';
        videoItem.setAttribute('data-aos', 'fade-up');
        
        // Check if it's an embed URL (YouTube/Vimeo) or direct video
        if (video.video_embed_url) {
            videoItem.innerHTML = `
                <div class="video-container" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
                    <iframe src="${video.video_embed_url}" 
                            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
                            frameborder="0" 
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                            allowfullscreen
                            title="${video.title}">
                    </iframe>
                </div>
                <p style="padding: 10px; font-size: 14px; font-weight: 600;">${video.title}</p>
            `;
        } else {
            // Direct video file
            const thumbnail = video.thumbnail_url || 'images/video-placeholder.jpg';
            videoItem.innerHTML = `
                <div style="position: relative; cursor: pointer;" onclick="playVideo('${video.media_url}', '${video.title}')">
                    <img src="${thumbnail}" alt="${video.title}" style="width: 100%; height: 200px; object-fit: cover;">
                    <div class="gallery-overlay">
                        <i class="fas fa-play-circle" style="font-size: 48px;"></i>
                    </div>
                </div>
                <p style="padding: 10px; font-size: 14px; font-weight: 600;">${video.title}</p>
            `;
        }
        
        videosGrid.appendChild(videoItem);
    });
    
    // Re-initialize AOS for new elements
    if (typeof AOS !== 'undefined') {
        AOS.refresh();
    }
}

// Switch between photo and video tabs
function switchGalleryTab(tab) {
    currentTab = tab;
    
    const photosTab = document.getElementById('photosTab');
    const videosTab = document.getElementById('videosTab');
    const photosGrid = document.getElementById('photosGrid');
    const videosGrid = document.getElementById('videosGrid');
    
    if (tab === 'photos') {
        // Style active photo tab
        photosTab.style.background = 'linear-gradient(135deg, #ff9500, #ff7800)';
        photosTab.style.color = 'white';
        photosTab.classList.add('active');
        
        // Style inactive video tab
        videosTab.style.background = '#f5f5f5';
        videosTab.style.color = '#666';
        videosTab.classList.remove('active');
        
        // Show photos, hide videos
        photosGrid.style.display = 'grid';
        videosGrid.style.display = 'none';
    } else {
        // Style active video tab
        videosTab.style.background = 'linear-gradient(135deg, #ff9500, #ff7800)';
        videosTab.style.color = 'white';
        videosTab.classList.add('active');
        
        // Style inactive photo tab
        photosTab.style.background = '#f5f5f5';
        photosTab.style.color = '#666';
        photosTab.classList.remove('active');
        
        // Show videos, hide photos
        photosGrid.style.display = 'none';
        videosGrid.style.display = 'grid';
        
        // Load videos if not already loaded
        if (videosGrid.innerHTML === '') {
            displayVideos();
        }
    }
}

// Play video in modal (optional - for direct video files)
function playVideo(videoUrl, title) {
    // Create a simple modal to play video
    const modal = document.createElement('div');
    modal.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 10000; display: flex; align-items: center; justify-content: center;';
    
    modal.innerHTML = `
        <div style="max-width: 90%; max-height: 90%;">
            <video controls autoplay style="width: 100%; max-height: 80vh;">
                <source src="${videoUrl}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <div style="text-align: center; margin-top: 15px;">
                <h3 style="color: white; margin-bottom: 10px;">${title}</h3>
                <button onclick="this.parentElement.parentElement.parentElement.remove()" 
                        style="padding: 10px 20px; background: #ff9500; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px;">
                    Close
                </button>
            </div>
        </div>
    `;
    
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    });
    
    document.body.appendChild(modal);
}

// Show fallback static content if API fails
function showFallbackGallery() {
    const photosGrid = document.getElementById('photosGrid');
    photosGrid.innerHTML = `
        <div class="gallery-item" data-aos="fade-up">
            <a href="images/1390271-kolan-hanmanth-reddy.jpg" data-lightbox="gallery" data-title="Kolan Hanmanth Reddy">
                <img src="images/1390271-kolan-hanmanth-reddy.jpg" alt="Kolan Hanmanth Reddy Portrait">
                <div class="gallery-overlay">
                    <i class="fas fa-search-plus"></i>
                </div>
            </a>
        </div>
        <div class="gallery-item" data-aos="fade-up">
            <a href="images/hq720.jpg" data-lightbox="gallery" data-title="Community Engagement">
                <img src="images/hq720.jpg" alt="Community Engagement Event">
                <div class="gallery-overlay">
                    <i class="fas fa-search-plus"></i>
                </div>
            </a>
        </div>
        <div class="gallery-item" data-aos="fade-up">
            <a href="images/587850980_1428313072196603_8882777926802737058_n.jpg" data-lightbox="gallery" data-title="Youth Program">
                <img src="images/587850980_1428313072196603_8882777926802737058_n.jpg" alt="Youth Engagement Program">
                <div class="gallery-overlay">
                    <i class="fas fa-search-plus"></i>
                </div>
            </a>
        </div>
    `;
}

// Load gallery on page load
loadGallery();

/* ============================================
   DEBUGGING & LOGGING
   ============================================ */

console.log('Kolan Hanmanth Reddy - Political Leader Website Loaded');
console.log('Version: 1.0.0');
console.log('Frontend Ready');
