import uuid
from flask import Blueprint, request, jsonify
from modules.data_preprocessing import clean_and_preprocess_data

data_bp = Blueprint('data_bp', __name__)

@data_bp.route('/preprocess', methods=['POST'])
def preprocess():
    """
    Endpoint to upload and preprocess CSV data.
    Expects a file upload via a multipart/form-data POST.
    """
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    filename = f"temp/{uuid.uuid4()}_{file.filename}"
    file.save(filename)

    try:
        df = clean_and_preprocess_data(filename)
        cleaned_file = filename.replace('.csv', '_cleaned.csv')
        df.to_csv(cleaned_file, index=False)
        return jsonify({'message': 'Preprocessing complete', 'cleaned_data_path': cleaned_file})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
