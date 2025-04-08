from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from pydantic import BaseModel
import random
import time

# Replace with the actual address of your RecoveryCoachAgent
RECOVERY_AGENT_ADDRESS = "agent1qxyz...abc"  # <-- Replace with actual

# Initialize PatientAgent
patient_agent = Agent(name="PatientAgent", seed="patient", endpoint="https://abc123.ngrok.io/submit", publish_agent_details=True, mailbox=True)

# Fund the agent (useful for local or testnet)
fund_agent_if_low(patient_agent.wallet.address())


# Define the expected check-in prompt message format
class CheckInPrompt(BaseModel):
    type: str
    date: str
    message: str


# Handle messages from RecoveryCoachAgent
@patient_agent.on_message(model=CheckInPrompt)
async def handle_check_in(ctx: Context, sender: str, message: CheckInPrompt):
    ctx.logger.info(f"Received check-in prompt from {sender}: {message.message}")

    if message.type == "check_in_prompt":
        # Simulate delay and patient input
        time.sleep(2)
        response = {
            "type": "check_in_response",
            "pain_level": random.randint(1, 10),
            "mobility": random.choice(["rested", "walked", "used wheelchair"]),
            "medication": random.choice(["yes", "no"])
            
        }

        ctx.logger.info(f"Sending check-in response: {response}")
        await ctx.send(sender, response)


if __name__ == "__main__":
    patient_agent.run()

