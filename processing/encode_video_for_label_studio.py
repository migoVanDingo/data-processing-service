import traceback
from flask import current_app
from classes.video_encoder import VideoEncoder
from utility.error import ThrowError


class EncodeVideoForLabelStudio:
    def __init__(self, video_path, output_path):
        self.video_path = video_path
        self.output_path = output_path


    def do_process(self):
        try:
            current_app.logger.info(f"{__class__.__name__} -- do_process -- Encoding video for Label Studio -- {self.video_path} -- {self.output_path}")
            video_encoder = VideoEncoder()
            return video_encoder.process_video(self.video_path, self.output_path)

        except Exception as e:
            current_app.logger.error(f"{__class__.__name__} -- {traceback.format_exc()} -- Error in encoding video for Label Studio: {e}")
            raise ThrowError(f"Error in encoding video for Label Studio: {e}", 500)
  