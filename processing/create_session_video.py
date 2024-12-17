import os
import traceback
from typing import List

from flask import current_app
from classes.video_writer import VideoWriter
from utility.error import ThrowError


class CreateSessionVideo:
    def __init__(self, video_list_path: str, output_file_path: str, fps: int, shape: tuple) -> None:
        self.video_list_path = video_list_path
        self.output_file_path = output_file_path
        self.fps = fps
        self.shape = shape

    def do_process(self):
        try:
            current_app.logger.info(f"{__class__.__name__} -- do_process")
            video_list = self.get_video_list(self.video_list_path)

            current_app.logger.info(f"{__class__.__name__} -- Concatenating videos: {video_list}")


            video_writer = VideoWriter()
            writer_instance = video_writer.get_writer_instance(self.output_file_path, self.fps, self.shape)
            video_writer.concatenate_videos(writer_instance, video_list)
            writer_instance.release()

            return os.path.exists(self.output_file_path)
        
        except Exception as e:
            current_app.logger.error(f"{__class__.__name__} -- {traceback.format_exc()} -- Error in creating session video: {e}")
            raise ThrowError(f"Error in creating session video: {e}", 500)


    def get_video_list(self, path) -> List[str]:
        try:
            files = os.listdir(path)
            video_files = [os.path.join(path,f) for f in files if f.endswith('.mp4')]
            return video_files
    
        except Exception as e:
            current_app.logger.error(f"{__class__.__name__} -- {traceback.format_exc()} -- Error in getting video list: {e}")