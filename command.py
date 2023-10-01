class Command:
    def __init__(self, message, args, client):
        self.message = message
        self.args = args
        self.client = client