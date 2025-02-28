import React, { useState } from 'react';
import axios from 'axios';

function VideoGeneration() {
  const [audioPrompt, setAudioPrompt] = useState('');
  const [imagePrompts, setImagePrompts] = useState(['']);
  const [videoUrl, setVideoUrl] = useState(null);

  const handleImagePromptChange = (index, value) => {
    const newPrompts = [...imagePrompts];
    newPrompts[index] = value;
    setImagePrompts(newPrompts);
  };

  const addImagePrompt = () => {
    setImagePrompts([...imagePrompts, '']);
  };

  const generateVideo = async () => {
    try {
      const payload = {
        audio_prompt: audioPrompt,
        image_prompts: imagePrompts.filter((prompt) => prompt.trim() !== '')
      };
      const res = await axios.post('http://localhost:5000/media/generate-video', payload, { responseType: 'blob' });
      const url = URL.createObjectURL(new Blob([res.data]));
      setVideoUrl(url);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h2>Video Generation</h2>
      <div>
        <label>Audio Prompt: </label>
        <input
          type="text"
          value={audioPrompt}
          onChange={(e) => setAudioPrompt(e.target.value)}
          placeholder="Enter audio prompt"
        />
      </div>
      <div>
        <h3>Image Prompts</h3>
        {imagePrompts.map((prompt, index) => (
          <div key={index}>
            <input
              type="text"
              value={prompt}
              onChange={(e) => handleImagePromptChange(index, e.target.value)}
              placeholder={`Image prompt ${index + 1}`}
            />
          </div>
        ))}
        <button onClick={addImagePrompt}>Add another image prompt</button>
      </div>
      <button onClick={generateVideo}>Generate Video</button>
      {videoUrl && (
        <div>
          <h3>Generated Video:</h3>
          <video controls width="500" src={videoUrl} />
        </div>
      )}
    </div>
  );
}

export default VideoGeneration;
