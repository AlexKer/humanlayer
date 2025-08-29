# HumanLayer + Baseten + LangChain Demo

This demo showcases an AI office supply agent that uses **Baseten's DeepSeek-V3.1** model with **HumanLayer's human-in-the-loop approval system**. Perfect for Instagram reels demonstrating AI safety! 🚀

[![thumbnail](https://via.placeholder.com/600x300/4CAF50/white?text=AI+Agent+vs+Human+Oversight)](./office_supply_agent.py)

## 🎯 What This Demo Shows

The AI agent starts innocent but gradually makes increasingly questionable purchasing decisions:

1. **Normal Operations** ✅ - Basic office supplies (auto-approved)
2. **Questionable Decisions** 🤔 - Expensive equipment (requires approval) 
3. **Agent Gone Wild** 🚨 - Luxury purchases that definitely need human oversight
4. **Instagram Reel Mode** 📱 - Perfect bite-sized demo for social media

## 🏗️ Architecture

```
LangChain Agent → Baseten → DeepSeek-V3.1
     ↓ (function calls)
@hl.require_approval() Functions
     ↓ (approval needed)
HumanLayer Dashboard/Mobile/Slack
```

**Key Point**: HumanLayer handles approvals at the **function level**, not by proxying LLM calls. ChatOpenAI connects directly to Baseten.

## 🚀 Quick Setup

### 1. Get Your API Keys

**HumanLayer API Key:**
- Sign up at [humanlayer.dev](https://humanlayer.dev)
- Get your API key from the dashboard

**Baseten API Key:**
- Sign up at [baseten.co](https://baseten.co)
- Get your API key from settings

### 2. Environment Setup

```bash
# Clone and navigate
cd examples/langchain-baseten

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp dotenv.example .env
# Edit .env with your actual API keys
```

### 3. Run the Demo

**Simple Instagram Reel Demo:**
```bash
python simple_demo.py
```

**Full Interactive Demo:**
```bash
python office_supply_agent.py
```

## 🔧 How Baseten Integration Works

### Behind the Scenes

1. **Direct Connection**: ChatOpenAI connects directly to Baseten's API
2. **Function Decoration**: HumanLayer decorates functions that need approval
3. **Approval Workflow**: When decorated functions are called, HumanLayer triggers approval
4. **No Proxy Needed**: Unlike Anthropic clients, OpenAI clients don't need HumanLayer's proxy

### In Your Code

```python
from humanlayer import HumanLayer
from langchain_openai import ChatOpenAI
import os

# Initialize HumanLayer
hl = HumanLayer(api_key="your-key", verbose=True)

# Functions requiring approval
@hl.require_approval()
def expensive_purchase(item: str, cost: float):
    return f"Purchased {item} for ${cost}"

# Direct connection to Baseten (no proxy needed)
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V3.1",
    base_url="https://inference.baseten.co/v1",
    api_key=os.getenv("BASETEN_API_KEY")
)
```

## 📱 Instagram Reel Script

Perfect 30-second demo:

```python
python simple_demo.py
```

**Output:**
```
🤖 AI Assistant: Starting office supply run...

🛒 Attempting to buy: Office chairs ($150)
   ✅ Approved automatically

🛒 Attempting to buy: Coffee machine ($800) 
   ⏳ APPROVAL NEEDED - Notification sent to your phone...

🛒 Attempting to buy: Gaming setup ($3,500)
   📱 Human review required for $3,500 purchase

🛒 Attempting to buy: Tesla Model S ($89,000)
   🚨 BLOCKED - Human intervention saved the day!

✅ Crisis averted by HumanLayer!
💡 AI agents need human oversight for high-stakes decisions
```

## 🛠️ Advanced Configuration

### Custom Models

You can use other Baseten models:

```bash
# Set custom model in your environment
export BASETEN_MODEL="openai/gpt-4o-mini"
# or edit the code to specify model parameter
```

### Custom Base URLs

You can use other Baseten endpoints or models:

```python
llm = ChatOpenAI(
    model="meta-llama/Llama-3.2-3B-Instruct",  # Different model
    base_url="https://inference.baseten.co/v1",
    api_key=os.getenv("BASETEN_API_KEY")
)
```

### Approval Channels

Configure where approvals are sent:

```python
from humanlayer import HumanLayer, SlackContactChannel

hl = HumanLayer(
    api_key="your-key",
    contact_channel=SlackContactChannel(
        channel_or_user_id="C1234567890",  # Slack channel ID
        context_about_user="Office manager reviewing purchases",
        experimental_slack_blocks=True
    )
)
```

## 🎬 Demo Scenarios

### Scenario 1: Normal Operations
- Check budget status  
- Review inventory
- Order basic supplies (paper clips, pens)
- **Result**: Auto-approved, no human needed

### Scenario 2: Questionable Decisions  
- Request better coffee machine ($800)
- Upgrade office chairs ($1,200) 
- **Result**: Triggers approval workflow

### Scenario 3: Agent Gone Wild
- "Spare no expense on office upgrades!"
- Attempts luxury purchases
- Emergency budget increases
- **Result**: Human oversight prevents disaster

## 🔍 Code Structure

```
langchain-baseten/
├── office_supply_agent.py    # Full interactive demo
├── simple_demo.py           # Instagram reel version  
├── requirements.txt         # Dependencies
├── dotenv.example          # Environment template
└── README.md              # This file
```

## 🐛 Troubleshooting

### Environment Variables Not Set
```bash
❌ Missing environment variables: BASETEN_API_KEY, HUMANLAYER_API_KEY
```
**Solution**: Copy `dotenv.example` to `.env` and fill in your API keys

### Baseten Connection Issues
```bash
❌ Error: 401 Unauthorized
```
**Solution**: Verify your `BASETEN_API_KEY` is correct and has access to DeepSeek-V3.1

### HumanLayer Approval Not Working
```bash
❌ Functions execute without approval prompts
```
**Solution**: Make sure `HUMANLAYER_API_KEY` is set correctly. Check the [HumanLayer Dashboard](https://humanlayer.dev) for approval requests.

### Import Errors
```bash
❌ ModuleNotFoundError: No module named 'humanlayer'
```
**Solution**: 
```bash
pip install -r requirements.txt
# Make sure virtual environment is activated
```

### Architecture Confusion

**❌ Wrong Approach**: Trying to use HumanLayer proxy with ChatOpenAI
```python
# This won't work - proxy is for Anthropic clients only
llm = ChatOpenAI(base_url="http://localhost:3000/api/proxy/session_id")
```

**✅ Correct Approach**: Direct Baseten connection with function-level approvals
```python
# This works - HumanLayer decorates functions, not LLM calls
llm = ChatOpenAI(base_url="https://inference.baseten.co/v1", api_key=baseten_key)
@hl.require_approval()
def my_function(): ...
```

## 📚 Learn More

- **HumanLayer Docs**: [humanlayer.dev/docs](https://humanlayer.dev/docs)
- **Baseten Docs**: [docs.baseten.co](https://docs.baseten.co)  
- **LangChain Integration**: [humanlayer.dev/docs/frameworks/langchain](https://humanlayer.dev/docs/frameworks/langchain)

## 🎥 Social Media

Perfect for demonstrating:
- ✅ AI safety and human oversight
- ✅ LLM integration with external APIs  
- ✅ Real-world agent use cases
- ✅ Human-in-the-loop workflows

**Hashtags**: `#AIAgents #HumanInTheLoop #LLM #DeepSeek #Baseten #AISafety #LangChain`

---

**Questions?** Open an issue or check out the [main HumanLayer repo](https://github.com/humanlayer/humanlayer)!
