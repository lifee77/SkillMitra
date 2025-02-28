# SkillMitra Backend

This repository contains the backend code for the SkillMitra project. SkillMitra is an e-learning application designed to leverage generative AI models for vocational training in developing economies. The backend is built using Flask and is structured in a modular way to keep functionality separate and maintainable.

## Overview

The backend provides endpoints for several core functionalities:
- **Data Preprocessing:** Uploading and cleaning CSV files containing personal and curriculum data.
- **Media Generation:** Generating audio and images based on text prompts using dummy (placeholder) functions. These functions can later be replaced with actual machine learning model integrations.
- **Video Generation:** Combining generated audio and images into a video story using MoviePy.
- **Course Recommendations:** A stub endpoint for returning course recommendations based on a user ID.

## Project Structure

```
SkillMitra/
└── Backend/
    ├── app.py                  # Main Flask application file
    ├── requirements.txt        # Python dependencies
    ├── routes/                 # HTTP endpoint definitions using Flask Blueprints
    │     ├── __init__.py       # Marks the folder as a Python package
    │     ├── data_routes.py    # Routes for data preprocessing
    │     ├── media_routes.py   # Routes for audio, image, and video generation
    │     └── recommendation_routes.py  # Routes for course recommendations
    └── modules/                # Business logic and ML-related functions
          ├── __init__.py       # Marks the folder as a Python package
          ├── data_preprocessing.py  # CSV file cleaning and preprocessing functions
          ├── audio_generation.py    # Dummy function to generate audio files
          ├── image_generation.py    # Dummy function to generate image files
          ├── video_generation.py    # Function to stitch together audio and images into a video
          └── recommendation.py      # Stub for the recommendation system
```

## Getting Started

### Prerequisites
- Python 3.7 or higher
- [pip](https://pip.pypa.io/en/stable/installation/)
- (Optional) A virtual environment tool such as `venv` or `virtualenv`

### Installation
1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/skillmitra-backend.git
   cd skillmitra-backend/Backend
   ```

2. **Create and Activate a Virtual Environment (Recommended):**

   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

From the `Backend` directory, start the Flask application with:

```bash
python app.py
```

By default, the app runs on [http://localhost:5000](http://localhost:5000). Endpoints are available under these URL prefixes:
- Data preprocessing: `/data/preprocess`
- Media generation: `/media/generate-audio`, `/media/generate-image`, `/media/generate-video`
- Recommendations: `/recommendation/`

## How the Backend is Structured

- **app.py:**  
  This is the entry point for the application. It creates a Flask app instance, registers blueprints for each group of endpoints, and ensures that required directories (`temp` and `outputs`) exist.

- **routes folder:**  
  Contains separate files for different endpoint groups:
  - **data_routes.py:** Handles file uploads and data preprocessing.
  - **media_routes.py:** Handles endpoints for generating audio, image, and video content.
  - **recommendation_routes.py:** Provides an endpoint for course recommendations.
  
  Blueprints are used to logically separate these routes and can be easily extended as new features are added.

- **modules folder:**  
  Contains the business logic and helper functions for each functionality:
  - **data_preprocessing.py:** Includes functions to load, clean, and preprocess CSV data.
  - **audio_generation.py & image_generation.py:** Currently include placeholder functions that simulate generating media content.
  - **video_generation.py:** Uses the MoviePy library to create a video by combining audio and images.
  - **recommendation.py:** Provides a dummy recommendation function which can later be replaced by actual recommendation logic.

## Adding New Features

As SkillMitra evolves, you might want to add new endpoints or functionalities. Here are some tips on how to expand the backend:

1. **Adding a New Module:**
   - Create a new Python file under the `modules/` folder for the business logic.
   - Write your functions or classes in that file.
   - Import and use these functions in your route files as needed.

2. **Adding New Routes:**
   - Create a new route file (e.g., `new_feature_routes.py`) under the `routes/` folder.
   - Define a Flask Blueprint in the file and add your endpoint definitions.
   - Register the blueprint in `app.py` with a suitable URL prefix.

3. **Improving Existing Functionality:**
   - Replace the dummy media generation functions in `modules/audio_generation.py` and `modules/image_generation.py` with actual integration of your ML models.
   - Enhance error handling and logging as you integrate with external services or databases.
   - Consider adding asynchronous processing (using Celery or Flask’s background tasks) for long-running tasks such as video generation.

4. **Testing and Deployment:**
   - Write unit tests for your new functionalities.
   - Look into containerization (using Docker) for easier deployment.
   - Set up continuous integration (CI) pipelines for automated testing.


This backend scaffold provides a starting point for developing the SkillMitra e-learning platform. The modular structure is designed to scale as you add more sophisticated machine learning integrations and additional features. For further details or support, please refer to the documentation of the tools and libraries used.

Happy coding!
