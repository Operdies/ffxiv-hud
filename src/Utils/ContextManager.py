import os

class ContextManager:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.old = os.getcwd()
        os.chdir(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.old)