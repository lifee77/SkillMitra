import os
import uuid
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

def create_video_story(audio_path, image_paths):
    """
    Creates a video by stitching together an audio track with a sequence of images.
    Each image is shown for an equal portion of the audio's duration.
    """
    try:
        audio_clip = AudioFileClip(audio_path)
        num_images = len(image_paths)
        image_duration = audio_clip.duration / num_images

        clips = []
        for img in image_paths:
            clip = ImageClip(img).set_duration(image_duration)
            clips.append(clip)

        video = concatenate_videoclips(clips, method="compose")
        video = video.set_audio(audio_clip)
        video_path = f"outputs/video_{uuid.uuid4()}.mp4"
        video.write_videofile(video_path, fps=24, codec="libx264", audio_codec="aac")
        return video_path
    except Exception as e:
        raise ValueError(f"Error creating video: {e}")
