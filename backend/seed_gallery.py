"""
Seed gallery data with existing photos
Run this script once to populate the database with initial gallery images
"""
import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

# Gallery items (6 existing photos from static content)
gallery_photos = [
    {
        "title": "Kolan Hanmanth Reddy",
        "description": "Official portrait of Kolan Hanmanth Reddy",
        "media_url": "images/1390271-kolan-hanmanth-reddy.jpg",
        "media_type": "photo",
        "display_order": 1,
        "is_active": True
    },
    {
        "title": "Community Engagement",
        "description": "Community engagement event with local residents",
        "media_url": "images/hq720.jpg",
        "media_type": "photo",
        "display_order": 2,
        "is_active": True
    },
    {
        "title": "Youth Program",
        "description": "Youth engagement program in Quthbullapur constituency",
        "media_url": "images/587850980_1428313072196603_8882777926802737058_n.jpg",
        "media_type": "photo",
        "display_order": 3,
        "is_active": True
    },
    {
        "title": "Community Service",
        "description": "Community service activity for local welfare",
        "media_url": "images/588266246_1428314585529785_7601836298558718966_n.jpg",
        "media_type": "photo",
        "display_order": 4,
        "is_active": True
    },
    {
        "title": "Health Camp",
        "description": "Health and wellness camp for underprivileged residents",
        "media_url": "images/608145349_1456202209407689_6360395274668037289_n.jpg",
        "media_type": "photo",
        "display_order": 5,
        "is_active": True
    },
    {
        "title": "Public Meeting",
        "description": "Public meeting event with constituency members",
        "media_url": "images/images.jpg",
        "media_type": "photo",
        "display_order": 6,
        "is_active": True
    }
]

# Sample video (you can add actual video URLs here)
gallery_videos = [
    {
        "title": "Community Development Initiative",
        "description": "Overview of community development programs in Quthbullapur",
        "media_url": "",  # Leave empty if using embed URL
        "video_embed_url": "",  # Add YouTube embed URL here when available
        "thumbnail_url": "images/video-thumbnail.jpg",  # Optional thumbnail
        "media_type": "video",
        "display_order": 1,
        "is_active": False  # Set to False until actual video is added
    }
]

def seed_gallery():
    """Seed gallery photos"""
    print("\n📸 Seeding Gallery Photos...")
    success_count = 0
    
    for item in gallery_photos:
        try:
            response = requests.post(f'{BASE_URL}/api/gallery', json=item)
            result = response.json()
            
            if result.get('success'):
                print(f"✓ Added photo: {item['title']}")
                success_count += 1
            else:
                print(f"✗ Failed: {item['title']} - {result.get('message')}")
        except Exception as e:
            print(f"✗ Error adding {item['title']}: {str(e)}")
    
    print(f"\n✅ Gallery photos seeded: {success_count}/{len(gallery_photos)}")

def seed_videos():
    """Seed sample video (optional)"""
    print("\n🎥 Seeding Sample Videos...")
    print("ℹ️  Sample video entry created (inactive until you add actual video URL)")
    
    success_count = 0
    for item in gallery_videos:
        try:
            response = requests.post(f'{BASE_URL}/api/gallery', json=item)
            result = response.json()
            
            if result.get('success'):
                print(f"✓ Added video placeholder: {item['title']}")
                success_count += 1
            else:
                print(f"✗ Failed: {item['title']} - {result.get('message')}")
        except Exception as e:
            print(f"✗ Error adding {item['title']}: {str(e)}")
    
    print(f"\n✅ Video entries seeded: {success_count}/{len(gallery_videos)}")

if __name__ == '__main__':
    print("=" * 60)
    print("GALLERY DATABASE SEEDING SCRIPT")
    print("=" * 60)
    print("\nMake sure the Flask backend is running on http://127.0.0.1:5000")
    print("Press Ctrl+C to cancel\n")
    
    try:
        # Test connection
        response = requests.get(f'{BASE_URL}/api/gallery/all')
        print("✓ Backend connection successful")
        
        # Seed data
        seed_gallery()
        seed_videos()
        
        print("\n" + "=" * 60)
        print("GALLERY SEEDING COMPLETED!")
        print("=" * 60)
        print("\n✓ You can now view the gallery in the admin dashboard")
        print("✓ The website will display photos and videos in separate tabs")
        print("\nTo add videos:")
        print("  1. Go to admin dashboard → Photo & Video Gallery")
        print("  2. Click 'Add Gallery Item'")
        print("  3. Select 'Video' type")
        print("  4. Provide video URL or YouTube embed URL")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend!")
        print("Make sure Flask server is running: python backend/app.py")
    except KeyboardInterrupt:
        print("\n\n⚠ Seeding cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
