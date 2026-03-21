"""
Seed data for Media & Recognition and Testimonials
Run this script once to populate the database with initial data
"""
import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

# Media & Recognition items (6 items from the original static content)
media_items = [
    {
        "title": "The Hans India",
        "description": "Coverage of free medical camp participation in Girinagar area",
        "icon": "fas fa-newspaper",
        "link_url": "https://www.thehansindia.com/telangana/quthubullapur-congress-in-charge-kolan-hanumanth-reddy-participates-in-medical-camp-853126",
        "link_text": "Read Article",
        "media_type": "news",
        "display_order": 1,
        "is_active": True
    },
    {
        "title": "Official Social Media",
        "description": "Verified Facebook profile with community engagement and social service updates",
        "icon": "fas fa-facebook",
        "link_url": "https://www.facebook.com/kolanhanmanthreddy/",
        "link_text": "Visit Facebook",
        "media_type": "social",
        "display_order": 2,
        "is_active": True
    },
    {
        "title": "Instagram",
        "description": "Photo updates from community programs and public engagement events",
        "icon": "fas fa-instagram",
        "link_url": "https://www.instagram.com/kolan.hanmanthreddy/",
        "link_text": "View Photos",
        "media_type": "social",
        "display_order": 3,
        "is_active": True
    },
    {
        "title": "The Hans India",
        "description": "Coverage of community group meeting (Kurma Sangam) in HMT Colony",
        "icon": "fas fa-newspaper",
        "link_url": "https://www.thehansindia.com/festival-of-democracy/quthbullapur-congress-candidate-meets-kurma-sangam-in-hmt-colony-837018",
        "link_text": "Read Article",
        "media_type": "news",
        "display_order": 4,
        "is_active": True
    },
    {
        "title": "The Hans India",
        "description": "Reports on youth joining Congress initiative in Quthbullapur",
        "icon": "fas fa-newspaper",
        "link_url": "https://www.thehansindia.com/telangana/150-youths-join-congress-in-quthbullapur-constituency-835566",
        "link_text": "Read Article",
        "media_type": "news",
        "display_order": 5,
        "is_active": True
    },
    {
        "title": "The Hans India",
        "description": "Coverage of prayers at Ellamma Temple before nomination filing",
        "icon": "fas fa-newspaper",
        "link_url": "https://www.thehansindia.com/telangana/kolan-hanumanth-reddy-offer-prayers-at-ellamma-temple-before-filing-nomination-836461",
        "link_text": "Read Article",
        "media_type": "news",
        "display_order": 6,
        "is_active": True
    }
]

# Testimonials items (4 items from the original static content)
testimonials = [
    {
        "name": "Community Resident",
        "designation": "Resident",
        "location": "Girinagar Area",
        "testimonial_text": "The free medical camp organized by Kolan Hanmanth Reddy was a great help for our family. We got free consultation and medicines which would have been very expensive otherwise.",
        "rating": 5,
        "avatar_icon": "fas fa-user",
        "display_order": 1,
        "is_active": True
    },
    {
        "name": "Youth Volunteer",
        "designation": "Volunteer",
        "location": "Quthbullapur Sevadal",
        "testimonial_text": "Kolan Sir's leadership has motivated us to engage in community service. The youth programs have given us a platform to contribute to society meaningfully.",
        "rating": 5,
        "avatar_icon": "fas fa-user",
        "display_order": 2,
        "is_active": True
    },
    {
        "name": "Community Leader",
        "designation": "Leader",
        "location": "HMT Colony",
        "testimonial_text": "He genuinely listens to community concerns and takes steps to address them. His transparent approach to governance is refreshing and needed in our constituency.",
        "rating": 5,
        "avatar_icon": "fas fa-user",
        "display_order": 3,
        "is_active": True
    },
    {
        "name": "Social Worker",
        "designation": "NGO Representative",
        "location": "Quthbullapur NGO",
        "testimonial_text": "Collaborating with Kolan Hanmanth Reddy on welfare programs has been excellent. He supports grassroots initiatives and empowers community organizations.",
        "rating": 5,
        "avatar_icon": "fas fa-user",
        "display_order": 4,
        "is_active": True
    }
]

def seed_media():
    """Seed media items"""
    print("\n🎬 Seeding Media & Recognition items...")
    success_count = 0
    
    for item in media_items:
        try:
            response = requests.post(f'{BASE_URL}/api/media', json=item)
            result = response.json()
            
            if result.get('success'):
                print(f"✓ Added: {item['title']}")
                success_count += 1
            else:
                print(f"✗ Failed: {item['title']} - {result.get('message')}")
        except Exception as e:
            print(f"✗ Error adding {item['title']}: {str(e)}")
    
    print(f"\n✅ Media items seeded: {success_count}/{len(media_items)}")

def seed_testimonials():
    """Seed testimonials"""
    print("\n💬 Seeding Testimonials...")
    success_count = 0
    
    for item in testimonials:
        try:
            response = requests.post(f'{BASE_URL}/api/testimonials', json=item)
            result = response.json()
            
            if result.get('success'):
                print(f"✓ Added testimonial from: {item['name']}")
                success_count += 1
            else:
                print(f"✗ Failed: {item['name']} - {result.get('message')}")
        except Exception as e:
            print(f"✗ Error adding {item['name']}: {str(e)}")
    
    print(f"\n✅ Testimonials seeded: {success_count}/{len(testimonials)}")

if __name__ == '__main__':
    print("=" * 60)
    print("DATABASE SEEDING SCRIPT")
    print("=" * 60)
    print("\nMake sure the Flask backend is running on http://127.0.0.1:5000")
    print("Press Ctrl+C to cancel\n")
    
    try:
        # Test connection
        response = requests.get(f'{BASE_URL}/api/media/all')
        print("✓ Backend connection successful")
        
        # Seed data
        seed_media()
        seed_testimonials()
        
        print("\n" + "=" * 60)
        print("SEEDING COMPLETED!")
        print("=" * 60)
        print("\n✓ You can now view the data in the admin dashboard")
        print("✓ The website will display the new dynamic content")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend!")
        print("Make sure Flask server is running: python backend/app.py")
    except KeyboardInterrupt:
        print("\n\n⚠ Seeding cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
