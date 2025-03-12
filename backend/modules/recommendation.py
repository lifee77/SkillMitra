import json
import numpy as np
import os
import logging
from typing import Dict, List, Any, Optional
from sentence_transformers import SentenceTransformer

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define the questions to ask users
USER_QUESTIONS = [
    {
        "id": "experience_level",
        "question": "What is your experience level with vocational skills?",
        "type": "select",
        "options": ["No experience", "Beginner", "Intermediate", "Advanced"]
    },
    {
        "id": "prior_experience",
        "question": "Please describe any relevant work experience you have:",
        "type": "textarea",
        "placeholder": "E.g., I worked as a carpenter's assistant for 6 months"
    },
    {
        "id": "interests",
        "question": "What skills or trades are you most interested in learning?",
        "type": "multiselect",
        "options": ["Carpentry", "Electrical", "Plumbing", "Welding", "Automotive", "Tailoring", "Other"]
    },
    {
        "id": "goals",
        "question": "What are your career goals?",
        "type": "textarea",
        "placeholder": "E.g., Start a furniture business, Get employment as an electrician"
    },
    {
        "id": "time_commitment",
        "question": "How much time can you commit to learning weekly?",
        "type": "select",
        "options": ["2-5 hours", "5-10 hours", "10-15 hours", "15+ hours"]
    }
]

# Initialize the embedding model - using a smaller model that works well on CPU
# In production, you might want to use a more powerful model like 'all-mpnet-base-v2'
_model = "paraphrase-MiniLM-L6-v2"

def get_embedding_model():
    """Lazy loading of the embedding model"""
    global _model
    if _model is None:
        try:
            logger.info("Loading embedding model...")
            _model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading embedding model: {str(e)}")
            # Fall back to random embeddings if model fails to load
            return None
    return _model

def vector_embed(text: str) -> np.ndarray:
    """
    Create vector embedding from text using sentence-transformers.
    
    Args:
        text: The text to embed
        
    Returns:
        numpy array containing the embedding
    """
    model = get_embedding_model()
    if model is None:
        # Fallback to random embeddings if model couldn't be loaded
        logger.warning("Using fallback random embeddings")
        return np.random.rand(384)  # Common embedding size
    
    try:
        return model.encode(text)
    except Exception as e:
        logger.error(f"Error generating embedding: {str(e)}")
        return np.random.rand(384)  # Fallback

def get_recommendations(user_responses: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    Get course recommendations based on user responses.
    
    Parameters:
    - user_responses: dict containing user answers to questions
      Example: {
        "experience_level": "Beginner",
        "prior_experience": "I worked in construction for a year",
        "interests": "Carpentry, Electrical",
        "goals": "I want to start my own home renovation business",
        "time_commitment": "5-10 hours"
      }
      
    Returns:
    - List of top 3 recommended courses as JSON-serializable objects
    """
    try:
        logger.info("Processing recommendation request")
        
        # 1. Combine user responses into a single text for embedding
        user_text = " ".join(user_responses.values())
        logger.info(f"User text prepared: {user_text[:100]}...")
        
        user_embedding = vector_embed(user_text)
        
        # 2. Load courses from courses.json
        courses_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "courses.json")
        try:
            with open(courses_path, "r") as f:
                courses_data = json.load(f)
            logger.info(f"Loaded {len(courses_data)} courses from JSON")
        except Exception as e:
            logger.error(f"Error loading courses data: {str(e)}")
            return []
        
        # 3. Compute similarity using cosine similarity
        def cosine_similarity(a, b):
            # Add small epsilon to avoid division by zero
            epsilon = 1e-8
            return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + epsilon))
        
        # 4. Rank courses based on similarity
        ranked_courses = []
        for course in courses_data:
            # Focus on relevant fields for matching
            course_text = f"{course.get('title', '')} {course.get('description', '')} " \
                         f"{' '.join(course.get('skills_covered', []))} " \
                         f"{course.get('difficulty', '')}"
            
            course_embedding = vector_embed(course_text)
            similarity = cosine_similarity(user_embedding, course_embedding)
            
            # Add course difficulty matching - prioritize appropriate difficulty level based on experience
            difficulty_bonus = 0
            user_exp = user_responses.get("experience_level", "").lower()
            course_diff = course.get("difficulty", "").lower()
            
            if (user_exp == "no experience" and course_diff == "beginner") or \
               (user_exp == "beginner" and course_diff in ["beginner", "intermediate"]) or \
               (user_exp == "intermediate" and course_diff in ["intermediate", "advanced"]) or \
               (user_exp == "advanced" and course_diff == "advanced"):
                difficulty_bonus = 0.1  # Boost courses with appropriate difficulty
            
            # Adjust similarity score with difficulty bonus
            adjusted_similarity = similarity + difficulty_bonus
            
            # Create a new dict to avoid modifying the original and ensure JSON serializability
            ranked_course = {
                "course_id": course.get("course_id", ""),
                "title": course.get("title", ""),
                "description": course.get("description", ""),
                "difficulty": course.get("difficulty", ""),
                "duration": course.get("duration", ""),
                "similarity_score": round(adjusted_similarity, 3),
                "image_url": course.get("image_url", ""),
                "skills_covered": course.get("skills_covered", [])
            }
            ranked_courses.append(ranked_course)
        
        # 5. Sort by similarity and return top 3
        top_recommendations = sorted(ranked_courses, key=lambda x: x["similarity_score"], reverse=True)[:3]
        logger.info(f"Generated {len(top_recommendations)} recommendations")
        
        return top_recommendations
        
    except Exception as e:
        logger.error(f"Error in recommendation system: {str(e)}")
        return []

def get_user_questions():
    """
    Return the questions that should be asked to the user.
    This can be called from an API endpoint to get the questions for the frontend.
    """
    return USER_QUESTIONS

# Example of API integration with Flask
"""
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

@app.route('/api/questions', methods=['GET'])
def get_questions_endpoint():
    return jsonify(get_user_questions())

@app.route('/api/recommendations', methods=['POST'])
def recommendations_endpoint():
    user_responses = request.json
    if not user_responses:
        return jsonify({"error": "No user responses provided"}), 400
        
    recommendations = get_recommendations(user_responses)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
"""

# Example user responses for testing
example_user_responses = {
    "experience_level": "Beginner",
    "prior_experience": "I helped my uncle with some home repairs and enjoyed working with wood.",
    "interests": "Carpentry, Welding",
    "goals": "I want to learn skills to renovate my home and possibly start a small business later.",
    "time_commitment": "5-10 hours"
}

# For testing the function directly
if __name__ == "__main__":
    print("Running recommendation test...")
    recommendations = get_recommendations(example_user_responses)
    print(f"Top recommendations for the user:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']} (Score: {rec['similarity_score']})")
        print(f"   {rec['description'][:100]}...")