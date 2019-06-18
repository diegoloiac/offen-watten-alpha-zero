from flask_restful import fields


class WattenResponse(fields.Raw):
    def __init__(self, message=None, body=None):
        super().__init__()
        self.message = message
        self.body = body
