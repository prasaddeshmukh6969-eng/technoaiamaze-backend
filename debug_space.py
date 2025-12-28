import gradio_client
from gradio_client import Client
import sys

print(f"gradio_client version: {gradio_client.__version__}")

# Try alternative space
SPACE_URL = "KwaiVGI/LivePortrait"
print(f"Testing connection to {SPACE_URL}...")

try:
    # Try without token first (public space)
    client = Client(SPACE_URL)
    print("Success!")
    print("API Info:")
    api_info = client.view_api(return_format="dict")
    print("Named Endpoints:")
    endpoints = api_info.get("named_endpoints", {})
    if "/gpu_wrapped_execute_video" in endpoints:
        print("Endpoint: /gpu_wrapped_execute_video")
        ep = endpoints["/gpu_wrapped_execute_video"]
        print("Parameters:")
        for i, param in enumerate(ep.get("parameters", [])):
            print(f"{i}: {param.get('label')}")
            
        # Try calling it
        print("\nAttempting API call...")
        image_path = "tests/fixtures/test_face.jpg"
        audio_path = "test_audio.wav"
        
        result = client.predict(
            image_path, 	# source_image (0)
            audio_path,	# driving_audio (1)
            True,		# relative_motion (2)
            True,		# do_crop (3)
            True,		# paste_back (4)
            api_name="/gpu_wrapped_execute_video" 
        )
        print(f"API Call Result: {result}")
    else:
        print("Endpoint /gpu_wrapped_execute_video not found")
except Exception as e:
    print(f"Failed: {e}")
    print(f"Error type: {type(e)}")
    sys.exit(1)
