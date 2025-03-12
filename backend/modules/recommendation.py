import json
import numpy as np
import os

def vector_embed(text):
    """
    Dummy embedding function: replace with a real embedding approach.
    """
    # In production, replace with actual embedding model
    # For example, using sentence-transformers or OpenAI embeddings
    return np.random.rand(128)  # Example vector size

def get_recommendations(user_responses):
    """
    Recommendation system using vector embeddings.
    
    Parameters:
    - user_responses: dict containing user answers to questions
      Example: {
        "experience": "2 years as a carpenter assistant",
        "goals": "Learn advanced woodworking techniques",
        "interests": "Furniture making, home renovation"
      }
      
    Returns:
    - List of top 3 recommended courses as JSON-serializable objects
    """
    try:
        # 1. Combine user responses into a single text for embedding
        user_text = " ".join(user_responses.values())
        user_embedding = vector_embed(user_text)
        
        # 2. Load courses from courses.json
        courses_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "courses.json")
        with open(courses_path, "r") as f:
            courses_data = json.load(f)
        
        # 3. Compute similarity using cosine similarity
        def cosine_similarity(a, b):
            return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
        
        # 4. Rank courses based on similarity
        ranked_courses = []
        for course in courses_data:
            course_text = f"{course.get('title', '')} {course.get('description', '')}"
            course_embedding = vector_embed(course_text)
            similarity = cosine_similarity(user_embedding, course_embedding)
            
            # Create a new dict to avoid modifying the original and ensure JSON serializability
            ranked_course = {
                "course_id": course.get("course_id", ""),
                "title": course.get("title", ""),
                "description": course.get("description", ""),
                "similarity_score": similarity,
                "image_url": course.get("image_url", "")
            }
            ranked_courses.append(ranked_course)
        
        # 5. Sort by similarity and return top 3
        return sorted(ranked_courses, key=lambda x: x["similarity_score"], reverse=True)[:3]
        
    except Exception as e:
        # Return empty list and log error (in production, use proper logging)
        print(f"Error in recommendation system: {str(e)}")
        return []

# Example of how this would be called from a Flask/FastAPI route handler:
# @app.route('/api/recommendations', methods=['POST'])
# def recommendations_endpoint():
#     user_responses = request.json
#     recommendations = get_recommendations(user_responses)
#     return jsonify(recommendations)