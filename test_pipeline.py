import requests
import json
import time
import os
from pathlib import Path

BASE_URL = "http://localhost:8000"
AVATAR_DIR = "assets/avatars"

def test_health():
    print("\n--- Testing Health Check ---")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Failed: {e}")
        return False

def test_list_avatars():
    print("\n--- Testing List Avatars ---")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/avatars")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            avatars = data.get("avatars", [])
            print(f"Found {len(avatars)} avatars")
            if len(avatars) > 0:
                print(f"Sample: {avatars[0]}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Failed: {e}")
        return False

# ... (skip to generate video)

def test_generate_video():
    # ... (setup code remains same)
    
    # ... (inside try block)
        print(f"Status: {response.status_code} (took {duration:.2f}s)")
        if response.status_code == 200:
            task = response.json()
            task_id = task.get("job_id")  # Use job_id
            print(f"Job ID: {task_id}")
            
            # Poll for status
            if task_id:
                return poll_task_status(task_id)
            return True
        else:
            print(f"Error: {response.text}")
            return False

def test_generate_anime_avatar():
    print("\n--- Testing Anime Avatar Generation ---")
    payload = {
        "prompt": "cute anime girl with blue hair, portrait",
        "style": "anime"
    }
    try:
        print(f"Sending request: {payload}")
        # Note: This might take time as it calls HF Space
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/api/v1/avatars/generate", json=payload)
        duration = time.time() - start_time
        
        print(f"Status: {response.status_code} (took {duration:.2f}s)")
        if response.status_code == 200:
            result = response.json()
            print(f"Result: {result}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Failed: {e}")
        return False

def test_generate_video():
    print("\n--- Testing Video Generation ---")
    
    # First get an avatar image path (or use a placeholder)
    # We'll try to use one from the gallery if available, or a default
    avatar_path = None
    
    # Check if we have any avatars in gallery
    try:
        response = requests.get(f"{BASE_URL}/api/v1/avatars")
        if response.status_code == 200:
            avatars = response.json()
            if avatars:
                # We need the full URL or path. The API returns 'filename'.
                # The server expects an 'image' file upload or 'image_url' if we modify it.
                # But the current v1_generation.py expects 'image' as UploadFile.
                pass
    except:
        pass

    # Create a dummy image for testing if needed
    dummy_image = "test_avatar.png"
    if not os.path.exists(dummy_image):
        from PIL import Image
        img = Image.new('RGB', (512, 512), color = 'red')
        img.save(dummy_image)

    data = {
        'text': 'Hello, this is a test of the video generation system.',
        'mode': 'anime', 
        'style': 'anime'
    }
    
    try:
        print(f"Sending video generation request...")
        start_time = time.time()
        
        # Open file within the request context or close explicitly
        with open(dummy_image, 'rb') as f:
            files = {'image': ('test_avatar.png', f, 'image/png')}
            response = requests.post(f"{BASE_URL}/api/v1/generate", files=files, data=data)
            
        duration = time.time() - start_time
        
        print(f"Status: {response.status_code} (took {duration:.2f}s)")
        if response.status_code == 200:
            task = response.json()
            task_id = task.get("job_id")
            print(f"Job ID: {task_id}")
            
            # Poll for status
            if task_id:
                return poll_task_status(task_id)
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Failed: {e}")
        return False
    finally:
        if os.path.exists(dummy_image):
            os.remove(dummy_image)

def poll_task_status(task_id):
    print(f"Polling status for task {task_id}...")
    for i in range(30): # Wait up to 30 seconds (it might fail fast or succeed fast)
        try:
            response = requests.get(f"{BASE_URL}/api/v1/status/{task_id}")
            if response.status_code == 200:
                status = response.json()
                state = status.get("status")
                print(f"State: {state}")
                if state == "completed":
                    print(f"Result: {status.get('result')}")
                    return True
                elif state == "failed":
                    print(f"Failure: {status.get('error')}")
                    return False
            time.sleep(2)
        except Exception as e:
            print(f"Polling failed: {e}")
            return False
    print("Timeout waiting for task completion")
    return False

if __name__ == "__main__":
    print("Starting API Tests...")
    
    health_ok = test_health()
    if not health_ok:
        print("Health check failed. Aborting.")
        exit(1)
        
    avatars_ok = test_list_avatars()
    
    # Uncomment to test generation (might be slow/expensive on quotas if not unlimited)
    # anime_gen_ok = test_generate_anime_avatar()
    
    video_ok = test_generate_video()
    
    print("\nTests Completed.")
