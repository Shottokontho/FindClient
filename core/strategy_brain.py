import json
import pandas as pd
from typing import List, Dict

class StrategyBrain:
    def __init__(self, dna_path: str):
        self.dna_path = dna_path

    def _get_company_dna(self) -> Dict:
        with open(self.dna_path, "r") as f:
            return json.load(f)

    def generate_sequence(self, leads: List[Dict]) -> str:
        """
        Uses a simulated Claude call to generate a personalized 
        7-day strategy for the batch of leads.
        """
        dna = self._get_company_dna()
        usp = dna.get("usp", "AI Automation Services")
        
        print(f"Strategizing campaigns based on USP: {usp}...")
        
        results = []
        for lead in leads:
            # In a real production environment, this is where the Claude API call happens.
            # We generate a sequence that avoids "AI-isms" (Caveman Style).
            sequence = {
                "Name": lead["name"],
                "Email": lead["email"],
                "Company": lead["company"],
                "Day 1 (The Hook)": f"Hey {lead['name']}, saw {lead['company']} is doing great things. Curious if you handle your {usp} in-house?",
                "Day 3 (The Value)": f"Quick thought for {lead['company']}: most people in your niche lose X% because of Y. We solved this using {usp}.",
                "Day 7 (The Last Call)": f"Last try, {lead['name']}. If you're not interested in {usp} right now, no worries. Cheers!"
            }
            results.append(sequence)
        
        # Save to Excel for user approval
        df = pd.DataFrame(results)
        output_path = "data/strategy_approval.xlsx"
        df.to_excel(output_path, index=False)
        
        return output_path
