import os
import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from core.dna_collector import DNACollector
from core.vault import VaultManager
from core.lead_hunter import LeadHunter
from core.strategy_brain import StrategyBrain
from core.drip_sender import DripSender
from core.crm_manager import CRMManager

console = Console()

class FindClientApp:
    def __init__(self):
        self.config_path = "config.json"
        self.dna_path = "data/company_dna.json"
        self.vault = VaultManager(self.config_path)
        self.dna = DNACollector(self.dna_path)
        self.crm = CRMManager()

    def header(self, text):
        console.print(Panel(f"[bold blue]{text}[/bold blue]", expand=False))

    def setup(self):
        self.header("SYSTEM ONBOARDING")
        if not self.dna.exists():
            console.print("[yellow]Company DNA missing.[/yellow]")
            choice = input(" (1) PDF/Doc Path or (2) Website URL: ")
            if choice == "1":
                self.dna.process_file(input("Path: "))
            else:
                self.dna.process_url(input("URL: "))
        
        if not self.vault.is_configured():
            console.print("[yellow]Vault not configured.[/yellow]")
            self.vault.save(input("Apify Key: "), input("Email: "), input("Pass: "))
        
        console.print("[green]✅ System Ready.[/green]")

    def run(self):
        self.header("FINDCLIENT HUNT MODE")
        
        target = input("🎯 Target Persona (or Enter for Auto-Predict): ")
        if not target:
            target = self.dna.predict_target()
            console.print(f"[cyan]AI Prediction: {target}[/cyan]")
            
        count_input = input("🔢 Lead Count: ")
        count = int(count_input) if count_input.isdigit() else 10
        platform = input("🌐 Platform (Google/LinkedIn): ")

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task(description="Hunting leads...", total=None)
            
            apify_key = self.vault.get_key("apify_key")
            hunter = LeadHunter(apify_key)
            actor_id = "apify/google-maps-scraper" if "google" in platform.lower() else "apify/linkedin-scraper"
            
            raw_leads = hunter.run_actor(actor_id, {"search": target, "maxItems": count})
            leads = hunter.clean_leads(raw_leads)
            progress.update(task, completed=True)

        self.crm.add_leads(leads)
        
        table = Table(title="Hunted Leads")
        table.add_column("Name", style="cyan")
        table.add_column("Email", style="magenta")
        for l in leads[:5]: table.add_row(l["name"], l["email"])
        console.print(table)

        brain = StrategyBrain(self.dna_path)
        path = brain.generate_sequence(leads)
        console.print(f"\n[bold green]Strategy Generated: {path}[/bold green]")
        
        if input("Approve and Drip? (y/n): ").lower() == 'y':
            limit_input = input("Max emails/day: ")
            limit = int(limit_input) if limit_input.isdigit() else 20
            sender = DripSender(self.vault.get_key("email"), self.vault.get_key("password"))
            sender.execute_drip(path, limit, (15, 30))
            
            for lead in leads:
                self.crm.update_status(lead["email"], "CONTACTED")
            console.print("[bold green]Drip Sequence Live![/bold green]")

if __name__ == "__main__":
    app = FindClientApp()
    app.setup()
    app.run()
