import os
import traceback
import cv2
from flask import current_app
import skvideo.io as skvio
from tqdm import tqdm
from typing import List

from utility.error import ThrowError

class VideoWriter:
    def __init__(self):
        pass

    def get_writer_instance(self, path, fps, shape):
        try:
            return cv2.VideoWriter(
                path,
                cv2.VideoWriter_fourcc(*'mp4v'),
                fps,
                shape
            )
        except Exception as e:
            current_app.logger.error(f"{__class__.__name__} -- {traceback.format_exc()} -- Error in getting writer instance: {e}")
            raise ThrowError(f"Error in getting writer instance: {e}", 500)


    def get_reader_instance(self, path):
        try:
            return cv2.VideoCapture(path)
        except Exception as e:
            current_app.logger.error(f"{__class__.__name__} -- {traceback.format_exc()} -- Error in getting reader instance: {e}")
            raise ThrowError(f"Error in getting reader instance: {e}", 500)
    


    def get_video_properties(self, video_path):
        """ Returns a dictionary with following video properties,
        1. video_name
        2. video_ext
        3. video_path
        4. frame_rate

        Parameters
        ----------
        video_path: str
            Video file path
        """
        try:
            # Get video file name and directory location
            video_dir = os.path.dirname(video_path)
            name, extension = os.path.splitext(os.path.basename(video_path))

            # Read video meta information
            metadata = skvio.ffprobe(video_path)
            
            print(f"Metadata: {metadata}")

            # If it is empty i.e. scikit video cannot read metadata
            # return empty stings and zeros
            if metadata == {}:
                video_properties = {
                    'islocal': False, 
                    'path': video_path,
                    'name': name,
                    'extension': extension,
                    'directory': video_dir,
                    'frame_rate': 0,
                    'duration': 0,
                    'num_frames': 0,
                    'width': 0,
                    'height': 0,
                    'frame_dim': None
                }

                return video_properties

            # Calculate average frame rate
            frame_rate = metadata['video']['@avg_frame_rate']
            print(f"Frame rate: {frame_rate}")
            frame_rate = round(int(frame_rate.split("/")[0]) / int(frame_rate.split("/")[1]))


            # Creating properties dictionary
            video_properties = {
                'islocal': True,
                'full_path': video_path,
                'name': name,
                'extension': extension,
                'directory': video_dir,
                'frame_rate': frame_rate,
                'duration': round(float(metadata['video']['@duration'])),
                'num_frames': int(metadata['video']['@nb_frames']),
                'width': int(metadata['video']['@width']),
                'height': int(metadata['video']['@height']),
                'frame_dim': (int(metadata['video']['@height']), int(metadata['video']['@width']), 3)
            }

            return video_properties
        except Exception as e:
            current_app.logger.error(f"{__class__.__name__} -- {traceback.format_exc()} -- Error in concatenating videos: {e}")
            raise ThrowError(f"Error in get_video_properties: {e}", 500)
    
    
    def get_frame(self, reader_instance: cv2.VideoCapture, frame_index: int) -> cv2.Mat:
        """
        Returns a frame from video using its frame number

        Parameters
        ----------
        frame_index: int
            Frame number
        """
        try:
            # Read video and seek to frame
            reader_instance.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            _, frame = reader_instance.read()

            # Reset the video reader to starting frame
            reader_instance.set(cv2.CAP_PROP_POS_FRAMES, 0)

            return frame
        except Exception as e:
            current_app.logger.error(f"{__class__.__name__} -- {traceback.format_exc()} -- Error in concatenating videos: {e}")
            raise ThrowError(f"Error in get_frame: {e}", 500)

    def concatenate_videos(self, writer_instance: cv2.VideoWriter, videos: List[str]) -> None:
        try:
            for video in videos:
                video_properties = self.get_video_properties(video)
                reader_instance = self.get_reader_instance(video)
                for frame_index in tqdm(range(0, video_properties['num_frames'], video_properties['frame_rate'])):
                    frame = self.get_frame(reader_instance, frame_index)
                    writer_instance.write(frame)

                reader_instance.release()
        except Exception as e:
            current_app.logger.error(f"{__class__.__name__} -- {traceback.format_exc()} -- Error in concatenating videos: {e}")
            raise ThrowError(f"Error in concatenating videos: {e}", 500)