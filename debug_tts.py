import asyncio
import edge_tts

TEXT = "Hello, this is a test of the Edge TTS service."
VOICE = "en-US-AriaNeural"
OUTPUT_FILE = "test_tts.mp3"

async def main():
    print(f"Testing Edge-TTS with voice: {VOICE}")
    try:
        communicate = edge_tts.Communicate(TEXT, VOICE)
        await communicate.save(OUTPUT_FILE)
        print(f"Success! Audio saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
