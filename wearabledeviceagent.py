from uagents import Agent, Context
from pydantic import BaseModel
wearable_agent = Agent(name="WearableDeviceAgent", seed="wearable",  endpoint = "http://127.0.0.1:8000/submit", mailbox = True)

class HealthData(BaseModel):
    type: str
    pain_level: int
    steps: int
    heart_rate: int

@wearable_agent.on_message(model = HealthData)
async def handle_message(ctx: Context, sender: str, message: dict):
    ctx.logger.info(f"Received message from {sender}: {message}")

    # Example: sending health data (heart rate, activity)
    health_data = {
        "type": "health_data",
        "pain_level": 4,
        "steps": 1200,
        "heart_rate": 78
    }


    # Sending health data to RecoveryCoachAgent
    await ctx.send(sender, health_data)
    
if __name__ == "__main__":
    wearable_agent.run()

