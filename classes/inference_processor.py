import traceback
from flask import current_app
import pandas as pd


class InferenceProcessor:
    def __init__(self):
        pass

    def filter_predictions(predictions_file_path: str, output_file_path: str) -> None:
        try:
            # Load csv file into dataframe
            df = pd.read_csv(predictions_file_path)
            
            # Return Filtered predictions on field class_prob != 0
            return df[df['class_prob'] != 0]
        
        except Exception as e:
            print(f"{__class__.__name__} -- {traceback.format_exc()} -- Error: {e}")
            current_app.logger.error(f"{__class__.__name__} -- {traceback.format_exc()} - {e} Error: {e}")


 
