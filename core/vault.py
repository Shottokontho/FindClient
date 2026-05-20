import json
import os

class VaultManager:
    def __init__(self, path):
        self.path = path

    def is_configured(self):
        return os.path.exists(self.path)

    def save(self, apify, email, password):
        data = {"apify_key": apify, "email": email, "password": password}
        with open(self.path, "w") as f:
            json.dump(data, f)
