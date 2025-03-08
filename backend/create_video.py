import os
import argparse
from modules.video_compiler import create_video_from_frames

def main():
    parser = argparse.ArgumentParser(description="Create video from frames in the outputs directory")
    parser.add_argument("--fps", type=int, default=24, 
                        help="Frames per second (default: 24)")
    parser.add_argument("--output", default=None, 
                        help="Output video path (default: outputs/output.mp4)")
    parser.add_argument("--slowdown", type=int, default=1, 
                        help="Slow down factor, e.g. 2 means half speed (default: 1)")
    parser.add_argument("--width", type=int, default=None, 
                        help="Target width for output video")
    parser.add_argument("--height", type=int, default=None, 
                        help="Target height for output video")
    
    args = parser.parse_args()
    
    # Prepare parameters
    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    
    if args.output is None:
        output_path = os.path.join(output_dir, "output.mp4")
    else:
        output_path = args.output
        
    # Adjust FPS based on slowdown factor
    actual_fps = args.fps / args.slowdown
    
    # Determine resize settings
    resize = None
    if args.width and args.height:
        resize = (args.width, args.height)
    
    print("=== Creating Video from Image Frames ===")
    print(f"Looking for frames in: {output_dir}")
    print(f"Output video: {output_path}")
    print(f"FPS: {actual_fps} (original: {args.fps}, slowdown: {args.slowdown}x)")
    
    if resize:
        print(f"Resizing to: {resize[0]}x{resize[1]}")
        
    try:
        video_path = create_video_from_frames(
            output_dir,
            output_path,
            fps=actual_fps,
            resize=resize
        )
        print("=== Video Creation Complete! ===")
        print(f"Video saved to: {video_path}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
