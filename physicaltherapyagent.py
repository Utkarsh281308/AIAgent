from uagents import Agent, Context
from pydantic import BaseModel

therapy_agent = Agent(name="PhysicalTherapyAgent", seed="therapy", endpoint=("http://127.0.0.1:8000/submit"), mailbox=True)

class TherapySchedule(BaseModel):
    type: str
    session_date: str
    exercises: list
    instructor: str

@therapy_agent.on_message(model=TherapySchedule)
async def handle_message(ctx: Context, sender: str, message: dict):
    ctx.logger.info(f"Received message from {sender}: {message}")

    # Example: sending therapy session details
    therapy_details = {
        "type": "therapy_schedule",
        "session_date": "2025-04-10 09:00 AM",
        "exercises": ["Leg lifts", "Knee stretches"],
        "instructor": "John Doe, PT"
    }

    # Sending therapy session details to RecoveryCoachAgent
    await ctx.send(sender, therapy_details)
    
    
if __name__ == "__main__":
    therapy_agent.run()

