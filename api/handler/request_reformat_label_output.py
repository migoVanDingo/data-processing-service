import csv
import json
import os
import traceback
from flask import current_app
from interface.abstract_handler import AbstractHandler
import pandas as pd

from utility.request import Request


class RequestReformatLabelOutput(AbstractHandler):
    def __init__(self, request_id: str, payload: dict):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- RequestReformatLabelOutput PAYLOAD: {self.payload}")

            # Check if annotation path is in payload
            if "annotation_destination_path" not in self.payload or self.payload["annotation_destination_path"] == "":
                raise Exception("annotation_destination_path is required")
            
            # Check if annotation file exists
            if os.path.exists(self.payload["annotation_destination_path"]) is False:
                raise Exception("annotation_destination_path does not exist")
            
            with open(self.payload["annotation_destination_path"], "r") as file:
                annotation_data = json.loads(file.read())  
            
            # Use first element only
            annotation_data = annotation_data[0]

            data = []
            labels = []

            lock = True
            for annotation in annotation_data["annotations"]:
                for result in annotation["result"]:
                    value = result["value"]
                    labels.append(value["labels"][0])
                    for seq in value["sequence"]:

                        if seq['enabled'] == lock:
                            
                            data.append({"target_id": result["id"], "label": value["labels"][0], "coordinates": seq, "enabled": lock})
                            lock = not lock 


            processed_path = os.path.join(self.payload["processed_directory"], self.payload["file_name"].split(".")[0] + ".csv")

            with open(processed_path, mode="w", newline="") as file:
            # Extract the keys from the first dictionary as column headers
                fieldnames = data[0].keys()
                
                # Create a DictWriter object
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                # Write the header row
                writer.writeheader()
                
                # Write the data rows
                writer.writerows(data)



            metadata = {
                "label_studio_internal_id": annotation_data["project"],
                "video": annotation_data["data"]["video"],
                "frames": annotation_data["annotations"][0]["result"][0]["value"]["framesCount"],
                "duration": annotation_data["annotations"][0]["result"][0]["value"]["duration"],
                "labels": labels,
                "activity_start_stop_data": data,
                "tasks": [annotation["task"] for annotation in annotation_data["annotations"]],
                "processed_annotation_path": processed_path,
                "raw_annotation_path": self.payload["annotation_destination_path"],
                "set_name": self.payload["set_name"],
                "set_id": self.payload["set_id"],
                "project_name": self.payload["project_name"],
                "label_project_id": self.payload["label_project_id"],

            }

            # Use file_id to update the metadata
            dao_request = Request()
            update_metadata = dao_request.update(self.request_id, "files", "file_id", self.payload["file_id"], {"metadata": json.dumps(metadata)})

            if "response" not in update_metadata:
                raise Exception("Failed to update metadata")
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- Reformated label output")

            return {"status": "SUCCESS", "data": { "processed_path": processed_path}}
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            return {"status": "FAILED", "error": str(e)}