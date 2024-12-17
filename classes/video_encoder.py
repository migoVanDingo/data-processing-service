import subprocess
import traceback

from flask import current_app

from utility.error import ThrowError


class VideoEncoder:
    def __init__(self):
        pass

    def process_video(self, input_path, output_path, preset="fast", crf=23) -> bool:
        """
        Generalized FFmpeg command to re-encode videos.
        
        Args:
            input_path (str): Path to the input video.
            output_path (str): Path to save the processed video.
            preset (str): Encoding speed/size tradeoff. Options: ultrafast, fast, medium, slow. Default: fast.
            crf (int): Quality factor (lower = better quality). Range: 0-51 (default 23).
        """
        try:
            command = [
                "ffmpeg", "-hide_banner", "-loglevel", "warning", "-y",
                "-i", input_path,
                "-c:v", "libx264",
                "-preset", preset,
                "-crf", str(crf),
                "-movflags", "faststart",
                output_path
            ]
            current_app.logger.info(f"Processing video with command: {' '.join(command)}")

            subprocess.run(command, check=True)
            return True
        except Exception as e:
            current_app.logger.error(f"{__class__.__name__} -- {traceback.format_exc()} -- Error in processing video: {e}")
            raise ThrowError(f"Error in processing video: {e}", 500)
