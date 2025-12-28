"""
Quick script to regenerate Video 2 with proper PIL-based GIF
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

job_id = "f7719b59-0554-49c6-8f86-d22142c257d5"

def create_placeholder_video(job_id: str) -> Path:
    """Create a proper placeholder video file using PIL"""
    output_dir = Path("temp_videos")
    output_dir.mkdir(exist_ok=True)
    
    try:
        # Use PIL to create an animated GIF
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a purple image with text
        width, height = 640, 480
        frames = []
        
        for i in range(30):  # 30 frames = ~1 second at 30fps
            img = Image.new('RGB', (width, height), color=(128, 0, 128))  # Purple
            draw = ImageDraw.Draw(img)
            
            # Add text
            try:
                font_title = ImageFont.truetype("arial.ttf", 40)
                font_small = ImageFont.truetype("arial.ttf", 24)
            except:
                font_title = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Draw title
            title = "Antigravity AI"
            title_bbox = draw.textbbox((0, 0), title, font=font_title)
            title_width = title_bbox[2] - title_bbox[0]
            draw.text(((width - title_width) / 2, height / 2 - 50), title, fill=(255, 255, 255), font=font_title)
            
            # Draw subtitle
            subtitle = "Mock Video Generated"
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_small)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            draw.text(((width - subtitle_width) / 2, height / 2 + 20), subtitle, fill=(200, 200, 200), font=font_small)
            
            # Draw job ID
            job_text = f"Job: {job_id[:8]}"
            job_bbox = draw.textbbox((0, 0), job_text, font=font_small)
            job_width = job_bbox[2] - job_bbox[0]
            draw.text(((width - job_width) / 2, height / 2 + 60), job_text, fill=(180, 180, 180), font=font_small)
            
            frames.append(img)
        
        # Save as animated GIF
        gif_path = output_dir / f"{job_id}.gif"
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0
        )
        
        print(f"✅ Created GIF: {gif_path}")
        print(f"   Size: {gif_path.stat().st_size} bytes")
        return gif_path
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    path = create_placeholder_video(job_id)
    if path:
        print(f"\n🎉 Video 2 regenerated successfully!")
    else:
        print(f"\n❌ Failed to regenerate video")
