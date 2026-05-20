import os
import json
from core.dna_collector import DNACollector
from core.vault import VaultManager
from core.lead_hunter import LeadHunter
from core.strategy_brain import StrategyBrain

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
        
        apify_key = self.vault.get_key("apify_key")
        hunter = LeadHunter(apify_key)
        actor_id = "apify/google-maps-scraper" if "google" in platform.lower() else "apify/linkedin-scraper"
        raw_leads = hunter.run_actor(actor_id, {"search": target, "maxItems": int(count)})
        leads = hunter.clean_leads(raw_leads)
        print(f"Found {len(leads)} viable leads.")
        with open("data/raw_leads.json", "w") as f:
            json.dump(leads, f)
        
        confirm = input("Proceed with hunt? (y/n): ")
        if confirm.lower() == 'y':
            print("Hunting leads... generating strategy... please wait.")
            # This will connect to Modules 3 & 4 in future updates
            # 3. Strategy Generation
        brain = StrategyBrain("data/company_dna.json")
        excel_path = brain.generate_sequence(leads)
        
        print(f"\n✅ STRATEGY GENERATED: {excel_path}")
        print("Please review the Excel sheet. If approved, we proceed to the Drip-Sender.")
        
        approval = input("Approved? (y/n): ")
        if approval.lower() == 'y':
            print("Scheduling emails in Module 4... (Pending implementation)")
        else:
            print("Strategy rejected. Please tweak the Excel file manually.")

if __name__ == "__main__":
    agent = FindClient()
    agent.setup()
    agent.run()
