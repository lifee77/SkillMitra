import os
import sys
import argparse
from modules.image_prompting import generate_video_prompts
from modules.together_image_generator import generate_images_from_prompts

def main():
    parser = argparse.ArgumentParser(description='Generate a video animation from a text description')
    parser.add_argument('scene', help='Description of the scene to animate')
    parser.add_argument('--frames', type=int, default=10, help='Number of frames to generate (default: 10)')
    parser.add_argument('--steps', type=int, default=4, help='Number of diffusion steps for image generation (default: 4, max 4 for FLUX models)')
    parser.add_argument('--model', type=str, default="black-forest-labs/FLUX.1-schnell-Free", 
                        help='Model to use for image generation')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"== Generating prompts for scene: {args.scene} ==")
    # Generate prompts
    prompts = generate_video_prompts(args.scene, num_frames=args.frames)
    
    # Find the latest generated prompts file
    prompt_files = [f for f in os.listdir('/Users/jeevanbhatta/SkillMitra') 
                   if f.startswith('generated_prompts_') and f.endswith('.json')]
    if not prompt_files:
        print("No prompt files found. Exiting.")
        sys.exit(1)
    
    # Get the most recent file
    latest_prompt_file = sorted(prompt_files)[-1]
    prompt_path = os.path.join('/Users/jeevanbhatta/SkillMitra', latest_prompt_file)
    
    print(f"== Generating images from prompts in {prompt_path} ==")
    # Generate images
    image_paths = generate_images_from_prompts(
        prompt_path, 
        output_dir=output_dir,
        model=args.model,
        steps=args.steps
    )
    
    print(f"\n== Generation complete! ==")
    print(f"Generated {len(image_paths)} images in {output_dir}")

if __name__ == "__main__":
    main()
