# 🩺 RecoveryCoachAgent

**RecoveryCoachAgent** is a decentralized AI-powered healthcare agent designed to assist patients in their post-surgery recovery by sending daily check-ins, collecting health data, and collaborating with other specialized agents for holistic care.

---

##  Features

- ✅ **Automated Daily Check-ins**  
  Sends structured prompts to patients asking for updates on:
  - Pain level (scale of 1–10)
  - Mobility (e.g., walked, rested)
  - Medication taken (yes/no)

- ✅ **Patient Progress Monitoring**  
  Receives and validates patient responses, logs information, and sends acknowledgements.

- ✅ **Multi-Agent Collaboration**  
  Communicates with the following agents:
  - **DischargeAgent** – Provides discharge instructions.
  - **TherapyAgent** – Shares physical therapy schedules.
  - **WearableAgent** – Sends real-time wearable health data (e.g., step count, heart rate).

- ✅ **Schema Validation with Pydantic**  
  Ensures structured and reliable message exchange using strongly-typed models.

- ✅ **Asynchronous Execution**  
  Uses `asyncio` for efficient concurrency and background tasks.

---

## 📁 AI Agents Address

Recovery_Agent_Address = "agent1qv5hjv3pe23yuzds3kxeed20rf2ykjgzgwq6jsf05kp6wvs03p7rwpf0vee"

DISCHARGE_AGENT_ADDRESS = "agent1qdzv4083wsjvvpvz7gf085ugpqaky4uksz0jqlug93fsgxl3430scsw3208"
PHYSICAL_THERAPY_AGENT_ADDRESS = "agent1qghlew6r2yc2d80z4skgjkglznh7jqprvhlsxn5xq5myhnfeuzkzkt5ghml"
WEARABLE_AGENT_ADDRESS = "agent1q2r7aa9wamff4upkcnsa8tyrgsw65g7wlxhyfzhwhakg3gqrgrld7qx2lul"