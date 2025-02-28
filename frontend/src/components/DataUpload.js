import React, { useState } from 'react';
import axios from 'axios';

function DataUpload() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('http://localhost:5000/data/preprocess', formData);
      setResponse(res.data);
    } catch (error) {
      console.error(error);
      setResponse({ error: 'Upload failed' });
    }
  };

  return (
    <div>
      <h2>Data Upload & Preprocessing</h2>
      <form onSubmit={handleUpload}>
        <input type="file" accept=".csv" onChange={handleFileChange} />
        <button type="submit">Upload and Preprocess</button>
      </form>
      {response && (
        <div>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default DataUpload;
