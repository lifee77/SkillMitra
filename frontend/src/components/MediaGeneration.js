import React, { useState } from 'react';
import axios from 'axios';

function MediaGeneration() {
  const [audioPrompt, setAudioPrompt] = useState('');
  const [imagePrompt, setImagePrompt] = useState('');
  const [audioUrl, setAudioUrl] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);

  const generateAudio = async () => {
    try {
      const formData = new FormData();
      formData.append('prompt', audioPrompt);
      const res = await axios.post('http://localhost:5000/media/generate-audio', formData, { responseType: 'blob' });
      const url = URL.createObjectURL(new Blob([res.data]));
      setAudioUrl(url);
    } catch (error) {
      console.error(error);
    }
  };

  const generateImage = async () => {
    try {
      const formData = new FormData();
      formData.append('prompt', imagePrompt);
      const res = await axios.post('http://localhost:5000/media/generate-image', formData, { responseType: 'blob' });
      const url = URL.createObjectURL(new Blob([res.data]));
      setImageUrl(url);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h2>Media Generation</h2>
      <div>
        <h3>Generate Audio</h3>
        <input
          type="text"
          value={audioPrompt}
          onChange={(e) => setAudioPrompt(e.target.value)}
          placeholder="Enter audio prompt"
        />
        <button onClick={generateAudio}>Generate Audio</button>
        {audioUrl && <audio controls src={audioUrl} />}
      </div>
      <div>
        <h3>Generate Image</h3>
        <input
          type="text"
          value={imagePrompt}
          onChange={(e) => setImagePrompt(e.target.value)}
          placeholder="Enter image prompt"
        />
        <button onClick={generateImage}>Generate Image</button>
        {imageUrl && <img src={imageUrl} alt="Generated" style={{ maxWidth: '300px' }} />}
      </div>
    </div>
  );
}

export default MediaGeneration;
