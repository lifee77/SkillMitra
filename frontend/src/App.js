import React from 'react';
import DataUpload from './components/DataUpload';
import MediaGeneration from './components/MediaGeneration';
import VideoGeneration from './components/VideoGeneration';
import Recommendations from './components/Recommendations';

function App() {
  return (
    <div className="App">
      <h1>SkillMitra - E-Learning Platform</h1>
      <hr />
      <DataUpload />
      <hr />
      <MediaGeneration />
      <hr />
      <VideoGeneration />
      <hr />
      <Recommendations />
    </div>
  );
}

export default App;
