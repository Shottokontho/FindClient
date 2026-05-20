import json
import requests
import time
from typing import List, Dict

class LeadHunter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.apify.com/v2"

    def run_actor(self, actor_id: str, search_params: Dict) -> List[Dict]:
        """
        Triggers an Apify actor and waits for the output.
        """
        print(f"Triggering Apify Actor: {actor_id}...")
        
        # Start actor
        run_url = f"{self.base_url}/actors/{actor_id}/runs"
        response = requests.post(run_url, json=search_params, params={"token": self.api_key})
        
        if response.status_code != 201:
            print(f"Error starting actor: {response.text}")
            return []

        run_data = response.json()
        run_id = run_data["data"]["id"]
        
        # Poll for completion
        while True:
            status_url = f"{self.base_url}/runs/{run_id}"
            status_resp = requests.get(status_url, params={"token": self.api_key})
            status = status_resp.json()["data"]["status"]
            
            if status == "SUCCEEDED":
                break
            elif status == "FAILED":
                print("Apify Run failed.")
                return []
            
            print("Hunting... waiting for results...")
            time.sleep(10)

        # Get dataset
        dataset_url = f"{self.base_url}/dataset/{run_data["data"]["defaultDatasetId"]}/items"
        dataset_resp = requests.get(dataset_url, params={"token": self.api_key})
        
        return dataset_resp.json()

    def clean_leads(self, raw_data: List[Dict]) -> List[Dict]:
        """
        Filters for valid emails and essential contact info.
        """
        cleaned = []
        for item in raw_data:
            email = item.get("email") or item.get("contactEmail")
            if email:
                cleaned.append({
                    "name": item.get("name", "Target"),
                    "email": email,
                    "company": item.get("company", "Unknown"),
                    "platform": item.get("platform", "Organic")
                })
        return cleaned
