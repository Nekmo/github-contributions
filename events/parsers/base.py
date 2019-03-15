

class ParserBase:
    def __init__(self, event):
        self.event = event

    @property
    def payload(self):
        return self.event.payload
