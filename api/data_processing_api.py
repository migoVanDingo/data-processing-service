from flask import Blueprint, request, jsonify
import json

from processing.create_session_video import CreateSessionVideo
from processing.encode_video_for_label_studio import EncodeVideoForLabelStudio

data_processing_api = Blueprint('data_processing_api', __name__)

@data_processing_api.route('/processing/session_video', methods=['POST'])
def create_session_video():
    data = json.loads(request.data)

    
    api_request = CreateSessionVideo(data['video_list_path'], data['output_file_path'], data['fps'], data['shape'])
    response = api_request.do_process()
    return jsonify({'status': response})

@data_processing_api.route('/processing/encode/video/label-studio', methods=['POST'])
def encode_video():
    data = json.loads(request.data)
    api_request = EncodeVideoForLabelStudio(data['video_path'], data['output_path'])
    response = api_request.do_process()
    return jsonify({'status': response})
                           


@data_processing_api.route('/data', methods=['GET'])
def get_data():
    # Retrieve the data here
    return None

@data_processing_api.route('/data', methods=['PUT'])
def update_data():
    data = json.loads(request.data)
    # Update the data here
    return None

@data_processing_api.route('/data', methods=['DELETE'])
def delete_data():
    data = json.loads(request.data)
    # Delete the data here
    return None