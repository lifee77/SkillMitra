import os
import re
import glob
from moviepy.editor import ImageSequenceClip
from PIL import Image

def natural_sort_key(s):
    """Sort strings with embedded numbers in natural order"""
    return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', s)]

def get_frame_files(directory, pattern="frame_*.png"):
    """Find all frame files matching the pattern and sort them naturally"""
    frames = glob.glob(os.path.join(directory, pattern))
    return sorted(frames, key=natural_sort_key)

def get_image_dimensions(image_path):
    """Get the dimensions of an image"""
    with Image.open(image_path) as img:
        return img.size

def create_video_from_frames(
    frames_dir,
    output_path=None,
    fps=12,
    pattern="frame_*.png",
    resize=None
):
    """
    Create a video from a sequence of image frames.
    
    Args:
        frames_dir: Directory containing the frame images
        output_path: Path to save the output video (default: in frames_dir as 'output.mp4')
        fps: Frames per second (default: 24)
        pattern: File pattern to match frame images (default: "frame_*.png")
        resize: Optional tuple (width, height) to resize frames (default: None)
        
    Returns:
        Path to the created video file
    """
    if not os.path.exists(frames_dir):
        raise ValueError(f"Frames directory not found: {frames_dir}")
        
    # Find and sort frames
    frame_files = get_frame_files(frames_dir, pattern)
    
    if not frame_files:
        raise ValueError(f"No frames found in {frames_dir} matching pattern {pattern}")
        
    print(f"Found {len(frame_files)} frames")
    
    # Default output path if not provided
    if output_path is None:
        output_path = os.path.join(frames_dir, "output.mp4")
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Get dimensions of first frame for consistency check
    first_frame_dimensions = get_image_dimensions(frame_files[0])
    
    # Check if all frames have the same dimensions
    consistent_dimensions = True
    for frame in frame_files[1:]:
        if get_image_dimensions(frame) != first_frame_dimensions:
            print(f"Warning: Inconsistent frame dimensions detected. {frame} differs from the first frame.")
            consistent_dimensions = False
            break
            
    if not consistent_dimensions and resize is None:
        # Default to the dimensions of the first frame if frames are inconsistent
        resize = first_frame_dimensions
        print(f"Setting all frames to consistent size: {resize}")
    
    # Create video clip from image sequence
    clip = ImageSequenceClip(frame_files, fps=fps)
    
    # Resize if needed
    if resize:
        clip = clip.resize(width=resize[0], height=resize[1])
    
    # Write video file
    print(f"Creating video at {fps} FPS...")
    clip.write_videofile(
        output_path,
        fps=fps,
        codec="libx264",
        audio=False,
        preset="medium",
        threads=4
    )
    
    print(f"Video saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create a video from sequential image frames")
    parser.add_argument("--frames_dir", default="/Users/jeevanbhatta/SkillMitra/backend/outputs", 
                        help="Directory containing the frame images")
    parser.add_argument("--output", default=None, 
                        help="Output video path (default: frames_dir/output.mp4)")
    parser.add_argument("--fps", type=int, default=10, 
                        help="Frames per second (default: 10)")
    parser.add_argument("--pattern", default="frame_*.png", 
                        help="File pattern to match frame images (default: frame_*.png)")
    parser.add_argument("--width", type=int, default=None, 
                        help="Resize video width")
    parser.add_argument("--height", type=int, default=None, 
                        help="Resize video height")
    
    args = parser.parse_args()
    
    resize = None
    if args.width and args.height:
        resize = (args.width, args.height)
    
    try:
        video_path = create_video_from_frames(
            args.frames_dir,
            args.output,
            args.fps,
            args.pattern,
            resize
        )
        print(f"Video creation successful!")
    except Exception as e:
        print(f"Error creating video: {str(e)}")
