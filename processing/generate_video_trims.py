import os
from flask import current_app
import pandas as pd
from classes.video_trimmer import ITrimVideo, VideoTrimmer
from utility.error import ThrowError


class GenerateVideoTrims:
    def __init__(self, ground_truth_path: str, video_dir: str, trim_output_dir: str) -> None:
        self.ground_truth_path = ground_truth_path
        self.video_dir = video_dir
        self.trim_output_dir = trim_output_dir
        

    def do_process(self):
        """
            Generate video trims based on the ground truth csv file.
            The output will be saved in the trim_output_dir
            Returns the list of files and paths of the generated trims

            Response:
            {
                "name": str (filename_startframe_endframe.ext)
                "output_dir": str (directory component of the output file)
            }
        """
        try:
            current_app.logger.info(f"{__class__.__name__} -- Generating video trims for {self.ground_truth_path}")

            created_files = []

            # Read csv file from ground truth path
            df = pd.read_csv(self.ground_truth_path)
            video_trimmer = VideoTrimmer()
            
            # Iterate over the rows of the dataframe
            for index, row in df.iterrows():

                payload = self.form_payload(row)
                output_file_path, output_file_name = self.form_file_path(row, self.trim_output_dir)

                result = video_trimmer.trim_video(payload, os.path.join(self.video_dir, row['name']), output_file_path)

                if not result:
                    current_app.logger.error(f"{__class__.__name__} -- Error in trimming video: {row['name']}")
                    raise ThrowError(f"Error in trimming video: {row['name']}")
                else:
                    current_app.logger.info(f"{__class__.__name__} -- Trimmed video: {output_file_path}")
                    
                    created_files.append(self.form_response(output_file_name, self.trim_output_dir))

        
            return created_files


        except Exception as e:
            current_app.logger.error(f"{__class__.__name__} -- Error in generating video trims: {e}")
            raise ThrowError(f"Error in generating video trims: {e}")
        


    def form_payload(self, row):
        return {
                    "start_frame": row['start_frame'],
                    "end_frame": row['end_frame'],
                    "bbox": [row['w0'], row['h0'], row['w'], row['h']],
                    "frame_rate": row['frame_rate']
        }
    

    def form_file_path(self, row, dir):
        file_name, extension = row['name'].split('.')
        output_file_name = f"{file_name}_{row['start_frame']}_{row['end_frame']}.{extension}"
        output_file_path = os.path.join(dir, output_file_name)

        return output_file_path, output_file_name
    

    def form_response(self, file, dir):
        return {
            "name": file,
            "output_dir": dir
        }