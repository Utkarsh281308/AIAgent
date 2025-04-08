import asyncio
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from datetime import datetime
from pydantic import BaseModel

# Define your agent
recovery_agent = Agent(name="RecoveryCoachAgent", seed="recovery")

# Ensure the agent has tokens to send messages (for testing)
fund_agent_if_low(recovery_agent.wallet.address())

# Define the patient agent's address (replace with real one in production)
PATIENT_AGENT_ADDRESS = "agent1qv5hjv3pe23yuzds3kxeed20rf2ykjgzgwq6jsf05kp6wvs03p7rwpf0vee"  # Replace with actual DID/address

# Addresses for supporting agents
DISCHARGE_AGENT_ADDRESS = "agent1qdzv4083wsjvvpvz7gf085ugpqaky4uksz0jqlug93fsgxl3430scsw3208"
PHYSICAL_THERAPY_AGENT_ADDRESS = "agent1qghlew6r2yc2d80z4skgjkglznh7jqprvhlsxn5xq5myhnfeuzkzkt5ghml"
WEARABLE_AGENT_ADDRESS = "agent1q2r7aa9wamff4upkcnsa8tyrgsw65g7wlxhyfzhwhakg3gqrgrld7qx2lul"

# ✅ Define the expected structure of the incoming check-in response
class CheckInResponse(BaseModel):
    type: str
    pain_level: int
    mobility: str
    medication: str
    
class HealthData(BaseModel):
    type: str
    pain_level: int
    steps: int
    heart_rate: int
    
class DischargeInstructions(BaseModel):
    type: str
    instructions: str
    medications: list
    next_appointment: str

class TherapySchedule(BaseModel):
    type: str
    session_date: str
    exercises: list
    instructor: str

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

    # Also send a prompt to the supporting agents for periodic updates
    discharge_message = {
        "type": "request_discharge_info",
        "message": "Please provide the discharge instructions for the patient."
    }
    await ctx.send(DISCHARGE_AGENT_ADDRESS, discharge_message)

    therapy_message = {
        "type": "request_therapy_schedule",
        "message": "Please provide the patient's physical therapy schedule."
    }
    await ctx.send(PHYSICAL_THERAPY_AGENT_ADDRESS, therapy_message)

    wearable_message = {
        "type": "request_health_data",
        "message": "Please provide the patient's latest health data."
    }
    await ctx.send(WEARABLE_AGENT_ADDRESS, wearable_message)

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

# ✅ Handle discharge response from DischargeAgent
@recovery_agent.on_message(model = DischargeInstructions)
async def handle_discharge_message(ctx: Context, sender: str, message: dict):
    if message.get("type") == "discharge_instructions":
        ctx.logger.info(f"Received discharge instructions: {message}")
        # Process the discharge instructions and send them to the patient agent or log
        discharge_ack_message = {
            "type": "acknowledgement",
            "status": "received",
            "details": "Discharge instructions have been noted."
        }
        await ctx.send(sender, discharge_ack_message)

# ✅ Handle therapy schedule response from TherapyAgent
@recovery_agent.on_message(model = TherapySchedule)
async def handle_therapy_schedule(ctx: Context, sender: str, message: dict):
    if message.get("type") == "therapy_schedule":
        ctx.logger.info(f"Received therapy schedule: {message}")
        # Process the therapy schedule and send them to the patient agent or log
        therapy_ack_message = {
            "type": "acknowledgement",
            "status": "received",
            "details": "Therapy schedule has been noted."
        }
        await ctx.send(sender, therapy_ack_message)

# ✅ Handle health data response from WearableAgent
@recovery_agent.on_message(model = HealthData)
async def handle_health_data(ctx: Context, sender: str, message: dict):
    if message.get("type") == "health_data":
        ctx.logger.info(f"Received health data: {message}")
        # Process the health data and send them to the patient agent or log
        health_data_ack_message = {
            "type": "acknowledgement",
            "status": "received",
            "details": "Health data has been recorded."
        }
        await ctx.send(sender, health_data_ack_message)

# async def main():
#     # Start both agents concurrently
#     await asyncio.gather(
#         recovery_agent.run(),
#         discharge_agent.run(),
#         physical_therapy_agent.run(),
#         wearable_agent.run(),
        
#         patient_agent.run(),
        
#     )


# if __name__ == "__main__":
#     asyncio.run(main())
if __name__ == "__main__":
    recovery_agent.run()
