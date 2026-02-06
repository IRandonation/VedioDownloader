
import yt_dlp
import sys
import json

def test_yt_dlp(url):
    print(f"Testing yt-dlp with URL: {url}")
    try:
        ydl_opts = {
            'quiet': False,
            'verbose': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Extracting info...")
            info = ydl.extract_info(url, download=False)
            
            print("-" * 20)
            print("Title:", info.get('title'))
            print("Duration:", info.get('duration'))
            print("Format Count:", len(info.get('formats', [])))
            
            # Print first 3 formats
            print("\nTop 3 Formats:")
            for f in info.get('formats', [])[:3]:
                print(f" - ID: {f.get('format_id')}, Ext: {f.get('ext')}, Res: {f.get('resolution')}")
            
            print("-" * 20)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Test with a YouTube video that is likely to work
    test_url = "https://www.youtube.com/watch?v=BaW_jenozKc" 
    if len(sys.argv) > 1:
        test_url = sys.argv[1]
    test_yt_dlp(test_url)
