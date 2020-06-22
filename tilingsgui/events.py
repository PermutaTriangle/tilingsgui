class Observer:
    def __init__(self, dispatchers):
        for dispatcher in dispatchers:
            dispatcher.push_handlers(self)
