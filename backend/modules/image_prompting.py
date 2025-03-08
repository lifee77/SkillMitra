import os
import json
from typing import List, Dict
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

class SequentialImagePromptGenerator:
    def __init__(self, api_key: str = GOOGLE_API_KEY):
        """Initialize the generator with Google API key."""
        if api_key is None:
            raise ValueError("No API key provided. Set GOOGLE_API_KEY environment variable or pass directly.")
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        
    def generate_initial_prompt(self, scene_description: str) -> str:
        """Generate the first prompt based on a general scene description."""
        system_prompt = """
        You are an expert at creating detailed image prompts. 
        I need you to create the first image in a sequence of 60 images that will form a cohesive animation or video-like sequence.
        Your prompt should be detailed, visual, and set up a scene that can evolve over time.
        Respond with ONLY the image prompt text, nothing else.
        """
        
        prompt = f"Create an initial image prompt for the following scene: {scene_description}"
        
        response = self.model.generate_content([system_prompt, prompt])
        return response.text.strip()
    
    def generate_next_prompt(self, previous_prompt: str, frame_number: int, total_frames: int = 60) -> str:
        """Generate the next prompt in the sequence based on the previous one."""
        system_prompt = f"""
        You are an expert at creating sequential image prompts.
        I'm creating a series of {total_frames} images that will appear as a fluid video when viewed in sequence.
        
        This is frame {frame_number} of {total_frames}.
        
        The previous frame was described as: "{previous_prompt}"
        
        Create the next frame description that shows subtle but clear progression from the previous frame.
        Maintain visual consistency (same characters, setting, style) while showing movement or change.
        Motion should be smooth and incremental as if this were a frame in an animation.
        
        Respond with ONLY the image prompt text, nothing else.
        """
        
        response = self.model.generate_content(system_prompt)
        return response.text.strip()
    
    def generate_prompt_sequence(self, initial_scene: str, num_frames: int = 60) -> List[str]:
        """Generate a sequence of prompts that evolve like frames in a video."""
        prompts = []
        
        # Generate initial prompt
        current_prompt = self.generate_initial_prompt(initial_scene)
        prompts.append(current_prompt)
        
        # Generate subsequent prompts
        for i in range(2, num_frames + 1):
            current_prompt = self.generate_next_prompt(current_prompt, i, num_frames)
            prompts.append(current_prompt)
            print(f"Generated frame {i}/{num_frames}")
        
        return prompts
    
    def save_prompts(self, prompts: List[str], output_path: str = None) -> str:
        """Save the generated prompts to a JSON file."""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"/Users/jeevanbhatta/SkillMitra/generated_prompts_{timestamp}.json"
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "frame_count": len(prompts),
            "prompts": prompts
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return output_path

def generate_video_prompts(scene_description: str, num_frames: int = 60, api_key: str = GOOGLE_API_KEY) -> List[str]:
    """
    Convenience function to generate a sequence of image prompts for video-like effect.
    
    Args:
        scene_description: A description of the scene you want to create
        num_frames: Number of sequential frames to generate (default: 60)
        api_key: Google API key for Gemini (optional if set as environment variable)
    
    Returns:
        List of image prompts
    """
    generator = SequentialImagePromptGenerator(api_key)
    prompts = generator.generate_prompt_sequence(scene_description, num_frames)
    
    # Save the prompts
    output_path = generator.save_prompts(prompts)
    print(f"Prompts saved to {output_path}")
    
    return prompts

if __name__ == "__main__":
    # Example usage
    scene = "A dandelion seed slowly drifting through a meadow on a sunny day"
    prompts = generate_video_prompts(scene, num_frames=60)
