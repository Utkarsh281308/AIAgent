from uagents import Agent, Context
from pydantic import BaseModel

discharge_agent = Agent(name="DischargeAgent", seed="discharge", endpoint = "http://127.0.0.1:8000/submit", mailbox = True)

class DischargeInstructions(BaseModel):
    type: str
    instructions: str
    medications: list
    next_appointment: str

@discharge_agent.on_message(model = DischargeInstructions)
async def handle_message(ctx: Context, sender: str, message: dict):
    ctx.logger.info(f"Received message from {sender}: {message}")

    # Example: sending discharge instructions
    discharge_instructions = {
        "type": "discharge_instructions",
        "instructions": "You are discharged from the hospital. Please follow the instructions provided by your surgeon.",
        "medications": ["Painkillers", "Antibiotics"],
        "next_appointment": "2025-05-01 10:00 AM"
    }
    
    # Sending discharge instructions back to RecoveryCoachAgent
    await ctx.send(sender, discharge_instructions)

if __name__ == "__main__":
    discharge_agent.run()
