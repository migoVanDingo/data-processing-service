class IInsert:
    table_name: str
    service: str
    payload: dict
    request_id: str

class IRead:
    table_name: str
    service: str
    filters: dict
    request_id: str

class IReadList:
    table_name: str
    service: str
    field: str
    value: str
    request_id: str

class IUpdate:
    table_name: str
    service: str
    key: str
    value: str
    data: dict
    request_id: str

class IDelete:
    table_name: str
    service: str
    id: str
    request_id: str

class RequestPayload:
    
    @staticmethod
    def form_insert_payload( request_id, table_name, service, data) -> IInsert:
        payload = {
            "table_name": table_name,
            "payload": data,
            "service": service,
            "request_id": request_id
        }
        return payload
    
    @staticmethod
    def form_read_payload( request_id, table_name, service, filters) -> IRead:
        payload = {
            "table_name": table_name,
            "filters": filters,
            "service": service,
            "request_id": request_id
        }
        return payload
    
    @staticmethod
    def read_list( request_id, table_name, service, data) -> IReadList:
        payload = {
            "table_name": table_name,
            "filters": data,
            "service": service,
            "request_id": request_id
        }
        return payload
    
    @staticmethod
    def form_update_payload(request_id, table_name, service, key, value, data) -> IUpdate:
        payload = {
            "table_name": table_name,
            "key": key,
            "value": value,
            "data": data,
            "service": service,
            "request_id": request_id
        }
        return payload
    
    @staticmethod
    def form_delete_payload( request_id, table_name, service, id) -> IDelete:
        payload = {
            "table_name": table_name,
            "id": id,
            "service": service,
            "request_id": request_id
        }
        return payload
    
    @staticmethod
    def form_query_payload( request_id, service, query) -> IRead:
        payload = {
            "query": query,
            "service": service,
            "request_id": request_id
        }
        return payload