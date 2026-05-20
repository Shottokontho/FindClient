# 🎯 FindClient: The Autonomous Client Acquisition Engine

**FindClient** is not just a scraper; it is a persistent agency agent. It transforms your business identity into a lead-generation machine by combining deep business intelligence with automated outreach strategies.

## 🌟 Why FindClient?
Most lead-gen tools are "dumb"—they find emails but don't know *why* they are emailing. **FindClient** starts by learning your business DNA, then hunts for high-probability matches and crafts a psychological 7-day drip campaign.

## 🛠 The Workflow

### 1. Onboarding (The DNA Phase)
The agent starts by understanding you. Provide a company PDF or a Website URL. FindClient scrapes, analyzes, and stores your **Company DNA** (USP, Tone, Target Audience) persistently.

### 2. Vault Setup
Securely connect your Apify and Gmail/SMTP credentials. These are stored locally and never asked for again.

### 3. The Hunt (Sourcing)
Define your target persona, quantity, and platform. 
- **Auto-Pilot:** If you're unsure, FindClient predicts your ideal client based on your DNA.
- **Cost Transparency:** Get an estimate of Apify credits and time before spending.

### 4. The Strategy (Claude Brain)
The system doesn't send generic spam. It uses Claude to generate a **7-Day Cold Outreach Sequence** in a structured Excel sheet for your approval.

### 5. The Drip (Anti-Ban Execution)
Once approved, the agent schedules the emails using a "Human-Mimic" drip system to avoid spam filters and account bans.

## 🚀 Installation
```bash
git clone https://github.com/Shottokontho/FindClient.git
cd FindClient
pip install -r requirements.txt
python main.py
```

## 🛡 Privacy & Security
- **Local-First:** Your company DNA and API keys are stored on your machine.
- **Human-in-the-Loop:** No email is sent without your explicit approval of the Excel strategy.

## 📈 roadmap
- [ ] **Deep LinkedIn Integration** (via browser-use)
- [ ] **Multi-Channel Sequence** (Email $ightarrow$ LinkedIn $ightarrow$ Twitter)
- [ ] **A/B Testing** for outreach templates
