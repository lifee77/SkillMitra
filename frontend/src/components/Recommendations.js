import React, { useState } from 'react';
import axios from 'axios';

function Recommendations() {
  const [userId, setUserId] = useState('');
  const [recommendations, setRecommendations] = useState([]);

  const fetchRecommendations = async () => {
    try {
      const res = await axios.get(`http://localhost:5000/recommendation/?user_id=${userId}`);
      setRecommendations(res.data.recommendations);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h2>Course Recommendations</h2>
      <div>
        <input
          type="text"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          placeholder="Enter your user ID"
        />
        <button onClick={fetchRecommendations}>Get Recommendations</button>
      </div>
      {recommendations.length > 0 && (
        <ul>
          {recommendations.map((rec, index) => (
            <li key={index}>
              {rec.course_id}: {rec.title}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Recommendations;
