from moviepy import VideoFileClip
from PIL import Image


def cvtVideo_to_Audio(video_path:str, user_name: str):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(f"user_data/media/audio/{user_name}.mp3")

    return f"user_data/media/audio/{user_name}.mp3"

def cvtImg_to_pdf(img_path:str, user_name: str):
    img = Image.open(img_path)

    if img.mode in ("RGBA", "LA"):
        img = img.convert("RGB")
    
    img.save(f"user_data/media/pdfs/{user_name}.pdf", "PDF", resolution=100.0)

    return f"user_data/media/pdfs/{user_name}.pdf"

