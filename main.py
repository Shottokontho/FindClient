import os
import json
from core.dna_collector import DNACollector
from core.vault import VaultManager

class FindClient:
    def __init__(self):
        self.config_path = "config.json"
        self.dna_path = "data/company_dna.json"
        self.vault = VaultManager(self.config_path)
        self.dna = DNACollector(self.dna_path)

    def setup(self):
        print("\n--- [ ONBOARDING MODE ] ---")
        if not self.dna.exists():
            print("Company DNA not found. Let's build it.")
            choice = input("Enter (1) PDF/Doc Path or (2) Website URL: ")
            if choice == "1":
                path = input("File Path: ")
                self.dna.process_file(path)
            else:
                url = input("Website URL: ")
                self.dna.process_url(url)
        
        if not self.vault.is_configured():
            printP("\n--- [ CREDENTIAL VAULT ] ---")
            apify_key = input("Apify API Key: ")
            email_user = input("Gmail/Email User: ")
            email_pass = input("App Password/API Key: ")
            self.vault.save(apify_key, email_user, email_pass)
        
        print("\n✅ Setup Complete. System is now Persistent.")

    def run(self):
        print("\n--- [ HUNT MODE ] ---")
        target = input("Who do you want to reach? (or press Enter to auto-predict): ")
        if not target:
            target = self.dna.predict_target()
            print(f"Predicted Target: {target}")
            
        count = input("How many leads? ")
        platform = input("Platform (GoogleMaps/LinkedIn/etc): ")
        
        print("\nCalculating Apify credits and time...")
        # Mock calculation
        print(f"Est. Cost: 0.5 Credits | Time: 8 mins")
        
        confirm = input("Proceed with hunt? (y/n): ")
        if confirm.lower() == 'y':
            print("Hunting leads... generating strategy... please wait.")
            # This will connect to Modules 3 & 4 in future updates
            print("Success! Excel strategy generated: data/strategy.xlsx")

if __name__ == "__main__":
    agent = FindClient()
    agent.setup()
    agent.run()
