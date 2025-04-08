from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from datetime import datetime
from pydantic import BaseModel

# Define your agent
recovery_agent = Agent(name="RecoveryCoachAgent", seed="recovery")

# Ensure the agent has tokens to send messages (for testing)
fund_agent_if_low(recovery_agent.wallet.address())

# Define the patient agent's address (replace with real one in production)
PATIENT_AGENT_ADDRESS = "agent1qxyz...abc"  # Replace with actual DID/address


# ✅ Define the expected structure of the incoming check-in response
class CheckInResponse(BaseModel):
    type: str
    pain_level: int
    mobility: str
    medication: str


# 📩 Daily check-in message template
def create_checkin_message():
    return {
        "type": "check_in_prompt",
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "message": "🩺 Hello! How are you feeling today after your surgery?\n\nPlease reply with:\n- Pain level (1-10)\n- Mobility (e.g., walked, rested)\n- Medication taken (yes/no)\n\nWe're tracking your progress 💪"
    }


# 🕒 Send daily check-in prompt
@recovery_agent.on_interval(period=86400)  # Every 24 hours
async def check_in(ctx: Context):
    message = create_checkin_message()
    ctx.logger.info(f"Sending daily check-in to patient: {message}")
    await ctx.send(PATIENT_AGENT_ADDRESS, message)


# ✅ Handle incoming responses
@recovery_agent.on_message(model=CheckInResponse)
async def handle_message(ctx: Context, sender: str, message: CheckInResponse):
    ctx.logger.info(f"Received message from {sender}: {message}")

    if message.type == "check_in_response":
        ctx.logger.info(
            f"Check-In Details - Pain Level: {message.pain_level}, Mobility: {message.mobility}, Medication Taken: {message.medication}"
        )

        # Send acknowledgement
        ack_message = {
            "type": "acknowledgement",
            "status": "received",
            "details": "Your daily recovery update has been recorded. Thank you!"
        }
        await ctx.send(sender, ack_message)
    else:
        ctx.logger.warning("Received an unknown message type.")
