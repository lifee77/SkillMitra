import os
import json
import time
import random
from typing import List, Dict
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable

load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

class SequentialImagePromptGenerator:
    def __init__(self, api_key: str = GOOGLE_API_KEY):
        """Initialize the generator with Google API key."""
        if api_key is None:
            raise ValueError("No API key provided. Set GOOGLE_API_KEY environment variable or pass directly.")
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
        
    def _call_api_with_retry(self, content, max_retries=6, base_delay=3.0):
        """Call the API with exponential backoff retry logic."""
        retries = 0
        while retries <= max_retries:
            try:
                return self.model.generate_content(content)
            except (ResourceExhausted, ServiceUnavailable) as e:
                retries += 1
                if retries > max_retries:
                    raise Exception(f"Maximum retries exceeded. API quota limit reached: {e}")
                
                # Calculate delay with exponential backoff and jitter
                delay = base_delay * (2 ** retries) + random.uniform(0, 1)
                print(f"Rate limit hit. Retrying in {delay:.1f} seconds... (Attempt {retries}/{max_retries})")
                time.sleep(delay)
            except Exception as e:
                raise Exception(f"API Error: {str(e)}")
    
    def generate_initial_prompt(self, scene_description: str, total_frames: int = 60) -> str:
        """Generate the first prompt based on a general scene description."""
        system_prompt = f"""
        You are an expert at creating detailed image prompts. 
        I need you to create the first image in a sequence of {total_frames} images that will form a cohesive animation or video-like sequence.
        Your prompt should be detailed, visual, and set up a scene that can evolve over time.
        Respond with ONLY the image prompt text, nothing else.
        """
        
        prompt = f"Create an initial image prompt for the following scene: {scene_description}"
        
        response = self._call_api_with_retry([system_prompt, prompt])
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
        Motion should be smooth and incremental as if this were a frame in an animation. Do not change the scene abruptly. The movements should only be a few pixels at a time.
        
        Respond with ONLY the image prompt text, nothing else.
        """
        
        response = self._call_api_with_retry(system_prompt)
        return response.text.strip()
    
    def generate_prompt_sequence(self, initial_scene: str, num_frames: int = 60) -> List[str]:
        """Generate a sequence of prompts that evolve like frames in a video."""
        prompts = []
        
        # Generate initial prompt
        print(f"Generating initial frame...")
        current_prompt = self.generate_initial_prompt(initial_scene)
        prompts.append(current_prompt)
        
        # Generate subsequent prompts
        for i in range(2, num_frames + 1):
            # Add a small delay between requests to avoid rate limiting
            time.sleep(0.5)
            
            try:
                current_prompt = self.generate_next_prompt(current_prompt, i, num_frames)
                prompts.append(current_prompt)
                print(f"Generated frame {i}/{num_frames}")
            except Exception as e:
                print(f"\nError generating frame {i}: {str(e)}")
                print(f"Stopping sequence generation. {len(prompts)} frames were successfully generated.")
                break
        
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
    try:
        generator = SequentialImagePromptGenerator(api_key)
        prompts = generator.generate_prompt_sequence(scene_description, num_frames)
        
        if prompts:
            # Save the prompts
            output_path = generator.save_prompts(prompts)
            print(f"Prompts saved to {output_path}")
        
        return prompts
    except Exception as e:
        print(f"Error generating video prompts: {str(e)}")
        return []

if __name__ == "__main__":
    # Example usage
    scene = "A female plumber fixing a broken pipe under the kitchen sink"
    prompts = generate_video_prompts(scene, num_frames=100)
