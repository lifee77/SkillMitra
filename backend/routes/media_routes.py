import uuid
from flask import Blueprint, request, jsonify, send_file
from modules.audio_generation import generate_audio
from modules.image_generation import generate_image
from modules.video_generation import create_video_story

media_bp = Blueprint('media_bp', __name__)

@media_bp.route('/generate-audio', methods=['POST'])
def generate_audio_route():
    """
    Endpoint to generate audio from a given prompt.
    Expects a form parameter 'prompt'.
    """
    prompt = request.form.get('prompt')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        audio_file = generate_audio(prompt)
        return send_file(audio_file, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@media_bp.route('/generate-image', methods=['POST'])
def generate_image_route():
    """
    Endpoint to generate an image from a given prompt.
    Expects a form parameter 'prompt'.
    """
    prompt = request.form.get('prompt')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        image_file = generate_image(prompt)
        return send_file(image_file, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@media_bp.route('/generate-video', methods=['POST'])
def generate_video_route():
    """
    Endpoint to generate a video story.
    Expects a JSON payload with:
      - audio_prompt: text prompt for audio generation.
      - image_prompts: list of text prompts for image generation.
    """
    data = request.get_json()
    if not data or 'audio_prompt' not in data or 'image_prompts' not in data:
        return jsonify({'error': 'Invalid payload. "audio_prompt" and "image_prompts" are required.'}), 400

    try:
        # Generate audio from the prompt
        audio_file = generate_audio(data['audio_prompt'])
        # Generate images for each provided image prompt
        image_files = [generate_image(prompt) for prompt in data['image_prompts']]
        # Create the video story using generated audio and images
        video_file = create_video_story(audio_file, image_files)
        return send_file(video_file, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
