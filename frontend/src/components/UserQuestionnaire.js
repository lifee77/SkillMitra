import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api';

const UserQuestionnaire = () => {
  const [questions, setQuestions] = useState([]);
  const [responses, setResponses] = useState({});
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [submitted, setSubmitted] = useState(false);

  // Fetch questions from backend
  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`${API_BASE_URL}/questions`);
        setQuestions(response.data);
        
        // Initialize empty responses object
        const initialResponses = {};
        response.data.forEach(q => {
          initialResponses[q.id] = q.type === 'multiselect' ? [] : '';
        });
        setResponses(initialResponses);
        
        setLoading(false);
      } catch (err) {
        setError('Failed to load questions. Please try again later.');
        setLoading(false);
        console.error('Error fetching questions:', err);
      }
    };

    fetchQuestions();
  }, []);

  const handleChange = (questionId, value) => {
    setResponses(prev => ({
      ...prev,
      [questionId]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Convert multiselect arrays to strings for the backend
      const processedResponses = {};
      Object.entries(responses).forEach(([key, value]) => {
        processedResponses[key] = Array.isArray(value) ? value.join(', ') : value;
      });

      const response = await axios.post(`${API_BASE_URL}/recommendations`, processedResponses);
      setRecommendations(response.data);
      setSubmitted(true);
      setLoading(false);
    } catch (err) {
      setError('Failed to get recommendations. Please try again.');
      setLoading(false);
      console.error('Error getting recommendations:', err);
    }
  };

  const renderQuestion = (question) => {
    switch (question.type) {
      case 'select':
        return (
          <select 
            className="form-select"
            value={responses[question.id] || ''}
            onChange={(e) => handleChange(question.id, e.target.value)}
            required
          >
            <option value="">Select an option</option>
            {question.options.map((option, index) => (
              <option key={index} value={option}>{option}</option>
            ))}
          </select>
        );

      case 'multiselect':
        return (
          <div>
            {question.options.map((option, index) => (
              <div className="form-check" key={index}>
                <input
                  className="form-check-input"
                  type="checkbox"
                  id={`${question.id}-${index}`}
                  value={option}
                  checked={responses[question.id]?.includes(option) || false}
                  onChange={(e) => {
                    const currentSelections = [...(responses[question.id] || [])];
                    if (e.target.checked) {
                      currentSelections.push(option);
                    } else {
                      const optionIndex = currentSelections.indexOf(option);
                      if (optionIndex !== -1) {
                        currentSelections.splice(optionIndex, 1);
                      }
                    }
                    handleChange(question.id, currentSelections);
                  }}
                />
                <label className="form-check-label" htmlFor={`${question.id}-${index}`}>
                  {option}
                </label>
              </div>
            ))}
          </div>
        );

      case 'textarea':
        return (
          <textarea
            className="form-control"
            rows="3"
            placeholder={question.placeholder || ''}
            value={responses[question.id] || ''}
            onChange={(e) => handleChange(question.id, e.target.value)}
            required
          />
        );

      default:
        return (
          <input
            type="text"
            className="form-control"
            placeholder={question.placeholder || ''}
            value={responses[question.id] || ''}
            onChange={(e) => handleChange(question.id, e.target.value)}
            required
          />
        );
    }
  };

  if (loading && !submitted) {
    return <div className="text-center mt-5"><div className="spinner-border" role="status"></div></div>;
  }

  if (submitted) {
    return (
      <div className="container my-4">
        <h2 className="mb-4">Your Recommended Courses</h2>
        
        {recommendations.length === 0 ? (
          <div className="alert alert-info">
            No courses match your profile. Please try adjusting your responses.
          </div>
        ) : (
          <div className="row">
            {recommendations.map((course, index) => (
              <div className="col-md-4 mb-4" key={course.course_id}>
                <div className="card h-100">
                  <img 
                    src={course.image_url || '/images/course-placeholder.jpg'} 
                    className="card-img-top" 
                    alt={course.title} 
                    style={{ height: '180px', objectFit: 'cover' }}
                  />
                  <div className="card-body">
                    <span className="badge bg-primary mb-2">{course.difficulty}</span>
                    <h5 className="card-title">{course.title}</h5>
                    <p className="card-text">{course.description}</p>
                    <p><small className="text-muted">Duration: {course.duration}</small></p>
                    
                    <h6 className="mt-3">Skills you'll learn:</h6>
                    <div className="d-flex flex-wrap">
                      {course.skills_covered?.map((skill, i) => (
                        <span key={i} className="badge bg-secondary me-1 mb-1">{skill}</span>
                      ))}
                    </div>
                  </div>
                  <div className="card-footer">
                    <button className="btn btn-primary w-100">Enroll Now</button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
        
        <button 
          className="btn btn-secondary mt-3" 
          onClick={() => setSubmitted(false)}
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="container my-4">
      <h2 className="mb-4">Find Your Perfect Course</h2>
      <p className="lead mb-4">
        Answer a few questions to help us recommend the best vocational courses for you.
      </p>

      {error && <div className="alert alert-danger">{error}</div>}

      <form onSubmit={handleSubmit}>
        {questions.map((question, index) => (
          <div className="mb-4" key={question.id}>
            <label className="form-label fw-bold">
              {index + 1}. {question.question}
            </label>
            {renderQuestion(question)}
          </div>
        ))}

        <button 
          type="submit" 
          className="btn btn-primary btn-lg mt-3"
          disabled={loading}
        >
          {loading ? 'Getting Recommendations...' : 'Get Recommendations'}
        </button>
      </form>
    </div>
  );
};

export default UserQuestionnaire;