from interface.abstract_handler import AbstractHandler


class RequestReformatLabelOutput(AbstractHandler):
    def __init__(self, request_id: str, payload: dict):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            return {"status": "SUCCESS"}
        except Exception as e:
            return {"status": "FAILED", "error": str(e)}