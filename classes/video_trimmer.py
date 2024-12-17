import os
import traceback
from typing import List

from flask import current_app
from pydantic import BaseModel

from utility.error import ThrowError

#Create pydantic model for video properties
class ITrimVideo(BaseModel):
    start_frame: int
    end_frame: int
    bbox: List[int]
    frame_rate: int


class VideoTrimmer:
    def __init__(self):
        pass

    def trim_video(self, video_props: ITrimVideo, video_path: str, output_file_path: str) -> bool:
        """
        Create a spatiotemporl trim. The output video name is
        <in_vid>_sfrm_efrm.mp4

        Parameters
        ----------
        video_props : ITrimVideo
            Video properties for trimming
            (ITrimVideo: start_frame, end_frame, bbox, frame_rate)

        video_path : str
            Path to the input video

        output_file_path : str
            Path to the output video
        
        """
        try:
            # Time stamps from frame numbers
            sts = video_props["start_frame"] / video_props["frame_rate"]
            num_frames = video_props["end_frame"] - video_props["start_frame"]

            # Creating ffmpeg command string
            crop_str = f"{video_props["bbox"][2]}:{video_props["bbox"][3]}:{video_props["bbox"][0]}:{video_props["bbox"][1]}"
            ffmpeg_cmd = (
                f'ffmpeg -hide_banner -loglevel warning '
                f'-y -ss {sts} -i {video_path} -vf "crop={crop_str}" '
                f'-c:v libx264 -crf 0 -frames:v {num_frames} {output_file_path}')
            
            current_app.logger.info(f"Trimming video with command: {ffmpeg_cmd}")
            os.system(ffmpeg_cmd)

            return True
        
        except Exception as e:
            current_app.logger.error(f"{__class__.__name__} -- {traceback.format_exc()} -- Error in trimming video: {e}")
            return False
            