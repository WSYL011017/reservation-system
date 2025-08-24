class Response:
    def __init__(self, code, msg, data):
        self.code = code
        self.msg = msg
        self.data = data
    def to_dict(self):
        return {
            'code': self.code,
            'msg': self.msg,
            'data': self.data
        }
    def to_json(self):
        return json.dumps(self.to_dict())