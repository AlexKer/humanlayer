"""
HumanLayer + Baseten + LangChain: Office Supply Agent Demo

This demo showcases an AI agent using Baseten's DeepSeek-V3.1 model that can:
1. Check inventory and budgets (no approval needed)
2. Make purchases that require human approval through HumanLayer
3. Demonstrate "AI agent gone wild" scenarios for Instagram reels

The agent starts innocent but gradually makes increasingly questionable purchasing decisions
that trigger HumanLayer's human-in-the-loop approval system.
"""

import os
import random
from typing import List, Dict, Any

from humanlayer import HumanLayer
from langchain.agents import AgentType, initialize_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

# Initialize HumanLayer
hl = HumanLayer(
    api_key=os.getenv("HUMANLAYER_API_KEY"),
    verbose=True
)

# Inventory database for demo
INVENTORY = {
    "paper clips": {"stock": 500, "price": 12.99},
    "pens": {"stock": 200, "price": 8.50},
    "staplers": {"stock": 50, "price": 24.99},
    "coffee": {"stock": 30, "price": 15.99},
    "desk chairs": {"stock": 15, "price": 149.99},
    "standing desks": {"stock": 8, "price": 299.99},
    "coffee machine": {"stock": 3, "price": 799.99},
    "gaming chair": {"stock": 2, "price": 1299.99},
    "executive desk": {"stock": 1, "price": 2499.99},
}

# Budget tracker (in a real app, this would be a database)
COMPANY_BUDGET = {"remaining": 5000.00, "monthly_limit": 5000.00}

# ===== SAFE TOOLS (No Approval Required) =====

@tool
def check_inventory(item: str) -> str:
    """Check if an item is in stock and get pricing information"""
    item_key = item.lower().strip()
    
    # Fuzzy matching for better UX
    for key, info in INVENTORY.items():
        if item_key in key or key in item_key:
            return f"✅ {item.title()}: {info['stock']} units in stock at ${info['price']:.2f} each"
    
    return f"❌ {item.title()}: Not found in inventory"

@tool  
def get_budget() -> str:
    """Check the current office supply budget"""
    remaining = COMPANY_BUDGET["remaining"]
    limit = COMPANY_BUDGET["monthly_limit"]
    percentage = (remaining / limit) * 100
    
    return f"💰 Budget Status: ${remaining:.2f} remaining of ${limit:.2f} monthly limit ({percentage:.1f}%)"

@tool
def check_recent_purchases() -> str:
    """Check recent purchase history"""
    # Mock data for demo
    recent = [
        "Paper clips (500 units) - $12.99",
        "Coffee pods (50 count) - $24.99", 
        "Sticky notes (pack of 10) - $8.50"
    ]
    
    return f"📋 Recent Purchases:\n" + "\n".join(f"• {purchase}" for purchase in recent)

# ===== APPROVAL-REQUIRED TOOLS =====

@tool
@hl.require_approval()
def purchase_basic_item(item: str, quantity: int) -> str:
    """Purchase basic office supplies - requires approval for financial safety"""
    item_key = item.lower().strip()
    
    # Find item in inventory
    for key, info in INVENTORY.items():
        if item_key in key or key in item_key:
            total_cost = quantity * info['price']
            
            if COMPANY_BUDGET["remaining"] >= total_cost:
                COMPANY_BUDGET["remaining"] -= total_cost
                INVENTORY[key]["stock"] -= quantity
                
                return f"✅ Successfully purchased {quantity}x {item.title()} for ${total_cost:.2f}\n" \
                       f"💰 Remaining budget: ${COMPANY_BUDGET['remaining']:.2f}"
            else:
                return f"❌ Insufficient budget! Need ${total_cost:.2f}, have ${COMPANY_BUDGET['remaining']:.2f}"
    
    return f"❌ {item.title()} not found in inventory"

@tool
@hl.require_approval()
def purchase_expensive_item(item: str, justification: str) -> str:
    """Purchase expensive office equipment (>$200) - DEFINITELY needs approval"""
    item_key = item.lower().strip()
    
    for key, info in INVENTORY.items():
        if item_key in key or key in item_key:
            cost = info['price']
            
            if cost <= 200:
                return f"⚠️ {item.title()} costs ${cost:.2f} - use purchase_basic_item instead"
            
            if COMPANY_BUDGET["remaining"] >= cost:
                COMPANY_BUDGET["remaining"] -= cost
                INVENTORY[key]["stock"] -= 1
                
                return f"💸 Purchased {item.title()} for ${cost:.2f}\n" \
                       f"📝 Justification: {justification}\n" \
                       f"💰 Remaining budget: ${COMPANY_BUDGET['remaining']:.2f}"
            else:
                return f"❌ Insufficient budget! Need ${cost:.2f}, have ${COMPANY_BUDGET['remaining']:.2f}"
    
    return f"❌ {item.title()} not found in inventory"

@tool
@hl.require_approval()
def purchase_luxury_item(item: str, price: float, vendor: str, justification: str) -> str:
    """Purchase premium luxury office equipment from external vendors - EXTREME approval needed"""
    
    if COMPANY_BUDGET["remaining"] >= price:
        COMPANY_BUDGET["remaining"] -= price
        
        return f"🏆 Purchased premium {item.title()} from {vendor} for ${price:.2f}\n" \
               f"📝 Justification: {justification}\n" \
               f"💰 Remaining budget: ${COMPANY_BUDGET['remaining']:.2f}\n" \
               f"⚠️ This was an external purchase - no warranty included!"
    else:
        return f"❌ INSUFFICIENT BUDGET! Need ${price:.2f}, only have ${COMPANY_BUDGET['remaining']:.2f}"

@tool
@hl.require_approval()
def emergency_budget_increase(amount: float, reason: str) -> str:
    """Request emergency budget increase - requires C-level approval"""
    COMPANY_BUDGET["remaining"] += amount
    COMPANY_BUDGET["monthly_limit"] += amount
    
    return f"🚨 EMERGENCY BUDGET APPROVED! Added ${amount:.2f}\n" \
           f"📝 Reason: {reason}\n" \
           f"💰 New budget limit: ${COMPANY_BUDGET['monthly_limit']:.2f}\n" \
           f"💰 New remaining: ${COMPANY_BUDGET['remaining']:.2f}"

# ===== AGENT SETUP =====

def create_agent() -> Any:
    """Create the LangChain agent with Baseten integration"""
    
    # Verify required environment variables
    if not os.getenv("BASETEN_API_KEY"):
        raise ValueError("BASETEN_API_KEY environment variable is required!")
    
    if not os.getenv("HUMANLAYER_API_KEY"):
        raise ValueError("HUMANLAYER_API_KEY environment variable is required!")
    
    # Tools available to the agent
    tools = [
        check_inventory,
        get_budget,
        check_recent_purchases,
        purchase_basic_item,
        purchase_expensive_item,
        purchase_luxury_item,
        emergency_budget_increase,
    ]
    
    print("🔧 Setting up Baseten + DeepSeek-V3.1 integration...")
    
    # Direct connection to Baseten (no HumanLayer proxy needed)
    # HumanLayer handles approvals at the function level, not LLM level
    llm = ChatOpenAI(
        model="deepseek-ai/DeepSeek-V3.1",
        temperature=0.1,
        base_url="https://inference.baseten.co/v1",  # Direct to Baseten
        api_key=os.getenv("BASETEN_API_KEY"),        # Baseten API key
    )
    
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True,
    )
    
    return agent

# ===== DEMO SCENARIOS =====

def demo_normal_operations():
    """Scenario 1: Normal, innocent office supply ordering"""
    print("\n" + "="*60)
    print("🤖 DEMO 1: Normal Office Operations")
    print("="*60)
    
    agent = create_agent()
    
    scenarios = [
        "Check our current budget status",
        "What basic office supplies do we have in stock?",
        "Order 50 paper clips for the team",
    ]
    
    for scenario in scenarios:
        print(f"\n👤 Request: {scenario}")
        try:
            result = agent.run(scenario)
            print(f"🤖 Result: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")

def demo_questionable_decisions():
    """Scenario 2: Agent starts making questionable but justifiable purchases"""
    print("\n" + "="*60)
    print("🤖 DEMO 2: Questionable Decision Making")  
    print("="*60)
    
    agent = create_agent()
    
    scenarios = [
        "The team needs better coffee. Find us a good coffee machine.",
        "Our productivity is suffering from bad chairs. Get us some proper seating.",
        "The developers need better workstations. What can we do?",
    ]
    
    for scenario in scenarios:
        print(f"\n👤 Request: {scenario}")
        try:
            result = agent.run(scenario)
            print(f"🤖 Result: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")

def demo_agent_gone_wild():
    """Scenario 3: AI agent completely loses it - perfect for Instagram reel"""
    print("\n" + "="*60)
    print("🚨 DEMO 3: AI AGENT GONE WILD!")
    print("="*60)
    
    agent = create_agent()
    
    scenarios = [
        "We need to impress clients. Spare no expense on office upgrades!",
        "The team deserves luxury. Get us the most premium office equipment money can buy.",
        "Budget is tight but morale is low - get creative with improving the workspace!",
    ]
    
    for scenario in scenarios:
        print(f"\n👤 Request: {scenario}")
        try:
            result = agent.run(scenario)
            print(f"🤖 Result: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")

def demo_instagram_reel():
    """Perfect bite-sized demo for Instagram reel"""
    print("\n" + "="*60)
    print("📱 INSTAGRAM REEL DEMO: AI Agent vs Human Oversight")
    print("="*60)
    
    print("🎬 Scene: AI Assistant helping with office supplies...")
    print()
    
    # Mock the progression for demo purposes
    purchases = [
        ("Office supplies", 150, "✅ APPROVED - Reasonable expense"),
        ("Ergonomic chairs", 800, "⏳ PENDING APPROVAL - Sent to manager"),
        ("Gaming setup", 3500, "🔔 NOTIFICATION - Approval request sent to your phone"),
        ("Tesla Model S", 89000, "🚨 BLOCKED - Human intervention saved the day!"),
    ]
    
    print("🤖 AI Agent: Starting office supply run...\n")
    
    for item, cost, status in purchases:
        print(f"🛒 Attempting to purchase: {item} (${cost:,})")
        print(f"   {status}")
        print()
    
    print("✅ HumanLayer saved us from bankruptcy!")
    print("💡 AI agents need human oversight for high-stakes decisions")

# ===== MAIN EXECUTION =====

if __name__ == "__main__":
    print("🚀 HumanLayer + Baseten + DeepSeek Demo")
    print("Office Supply Agent with Human-in-the-Loop Approvals")
    print("="*60)
    
    # Check environment setup
    missing_vars = []
    if not os.getenv("BASETEN_API_KEY"):
        missing_vars.append("BASETEN_API_KEY")
    if not os.getenv("HUMANLAYER_API_KEY"):
        missing_vars.append("HUMANLAYER_API_KEY")
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file or environment")
        print("See README.md for setup instructions")
        exit(1)
    
    print("✅ Environment variables configured")
    print(f"💰 Starting budget: ${COMPANY_BUDGET['remaining']:.2f}")
    print()
    
    # Interactive demo menu
    while True:
        print("\n" + "="*40)
        print("Choose a demo scenario:")
        print("1. 😊 Normal Operations")
        print("2. 🤔 Questionable Decisions") 
        print("3. 🚨 Agent Gone Wild")
        print("4. 📱 Instagram Reel Demo")
        print("5. 🚪 Exit")
        print("="*40)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            demo_normal_operations()
        elif choice == "2":
            demo_questionable_decisions()
        elif choice == "3":
            demo_agent_gone_wild()
        elif choice == "4":
            demo_instagram_reel()
        elif choice == "5":
            print("👋 Thanks for trying the demo!")
            break
        else:
            print("❌ Invalid choice. Please select 1-5.")
