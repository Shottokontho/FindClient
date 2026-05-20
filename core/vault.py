import json
import os

class VaultManager:
    def __init__(self, path):
        self.path = path

    def exists(self):
        return os.path.exists(self.path)
        self.path = path

    def is_configured(self):
        return os.path.exists(self.path)

    def save(self, apify, email, password):
        data = {"apify_key": apify, "email": email, "password": password}
        with open(self.path, "w") as f:
            json.dump(data, f)

    def get_key(self, key_name):
        if not self.exists(): return None
        with open(self.path, "r") as f:
            data = json.load(f)
        return data.get(key_name)
        data = {"apify_key": apify, "email": email, "password": password}
        with open(self.path, "w") as f:
            json.dump(data, f)
