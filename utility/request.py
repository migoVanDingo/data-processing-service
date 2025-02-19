import traceback
import requests

from flask import current_app, request
from utility.constant import Constant
from utility.error import ThrowError
from utility.payload.request_payload import RequestPayload

class IInsert:
    table_name: str
    service: str
    payload: dict
    request_id: str


class Request:
    def __init__(self):
        self.service = Constant.service
        self.headers = self.get_headers()
        
    
    def get_headers(self):
        return {
            "Content-Type": "application/json"
        }


    def insert(self, request_id, table_name, data):
        """Insert data into the database
        Args:
            request_id (str): Request ID
            table_name (str): Table name
            data (dict): Data to be inserted
        
        Returns:
            response: record dictionary
        """
        try:
            url = Constant.base_url + Constant.dao_port + Constant.dao["create"]
            payload = RequestPayload.form_insert_payload(request_id, table_name, self.service, data)
            current_app.logger.info(f"{request_id} --- {self.__class__.__name__} --- URL: {url} --- INSERT PAYLOAD: {payload}")
            response = requests.post(url, headers=self.headers, json=payload)
            return response.json()
        
        except Exception as e:
            current_app.logger.error(f"{request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError("Failed to insert data", 500)
        


    def read(self, request_id, table_name, data):
        """Read data from the database
        Args:
            request_id (str): Request ID
            table_name (str): Table name
            data (dict): Data to be read
            
            Returns:
                response: Response from the DAO
        """
        try:
            url = Constant.base_url + Constant.dao_port + Constant.dao["read"]
            payload = RequestPayload.form_read_payload(request_id, table_name, self.service, data)
            current_app.logger.info(f"{request_id} --- {self.__class__.__name__} --- READ PAYLOAD: {payload}")
            response = requests.post(url, headers=self.headers, json=payload)
            return response.json()
        
        except Exception as e:
            current_app.logger.error(f"{request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError("Failed to read data", 500)
        

    def read_list(self, request_id, table_name, data):
        """Read list of data from the database
        Args:
            request_id (str): Request ID
            table_name (str): Table name
            field (str): Field to be used for filtering
            value (str): Value to be used for filtering
            
            Returns:
                response: Response from the DAO
        """
        try:
            url = Constant.base_url + Constant.dao_port + Constant.dao["list"]
            payload = RequestPayload.read_list(request_id, table_name, self.service, data)
            current_app.logger.info(f"{request_id} --- {self.__class__.__name__} --- READ_LIST PAYLOAD: {payload}")
            response = requests.post(url, headers=self.headers, json=payload)
            return response.json()
        
        except Exception as e:
            current_app.logger.error(f"{request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError("Failed to read data", 500)
        
    def read_all(self, request_id="READ_ALL", query=None):
        try:
            url = Constant.base_url + Constant.dao_port + Constant.dao["read_all"]
           
            payload={"query":query}
      
            response = requests.post(url, headers=self.headers, json=payload)
            return response.json()
        except Exception as e:
            current_app.logger.error(f"{request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")

    def update(self, request_id, table_name, key, value, data):
        """Update data in the database
        Args:
            request_id (str): Request ID
            table_name (str): Table name
            key (str): Key to be used for filtering
            value (str): Value to be used for filtering
            data (dict): Data to be updated
            
            Returns:
                response: Response from the DAO
        """
        try:
            url = Constant.base_url + Constant.dao_port + Constant.dao["update"]
            payload = RequestPayload.form_update_payload(request_id, table_name, self.service, key, value, data)
            current_app.logger.info(f"{request_id} --- {self.__class__.__name__} --- UPDATE PAYLOAD: {payload}")
            response = requests.post(url, headers=self.headers, json=payload)
            return response.json()
        
        except Exception as e:
            current_app.logger.error(f"{request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
        
    
    def delete(self, request_id, table_name, id):
        """Delete data from the database
        Args:
            request_id (str): Request ID
            table_name (str): Table name
            id (str): ID of the data to be deleted
            
            Returns:
                response: Response from the DAO
        """
        try:
            url = Constant.base_url + Constant.dao_port + Constant.dao["delete"]
            payload = RequestPayload.form_delete_payload(request_id, table_name, self.service, id)
            current_app.logger.info(f"{request_id} --- {self.__class__.__name__} --- DELETE PAYLOAD: {payload}")
            response = requests.post(url, headers=self.headers, json=payload)
            return response.json()
        
        except Exception as e:
            current_app.logger.error(f"{request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
    

        
    def query(self, request_id, query):
        """Query data from the database
        Args:
            request_id (str): Request ID
            table_name (str): Table name
            query (str): Query to be executed
            
            Returns:
                response: Response from the DAO
        """
        try:
            url = Constant.base_url + Constant.dao_port + Constant.dao["query"]
            payload = RequestPayload.form_query_payload(request_id, self.service, query)
            current_app.logger.info(f"{request_id} --- {self.__class__.__name__} --- QUERY PAYLOAD: {payload}")
            response = requests.post(url, headers=self.headers, json=payload)
            return response.json()
        
        except Exception as e:
            current_app.logger.error(f"{request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")