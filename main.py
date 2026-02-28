import os
import random
import asyncio
from vision_agents.core.agent import Agent
from vision_agents.core.models import User
from vision_agents.plugins import getstream, deepgram, elevenlabs
from vision_agents.llms import openai
from vision_agents.core.stt.events import STTTranscriptEvent


LIVENESS_TASKS = [
    "hold a pen to your left cheek",
    "place your right hand on top of your head",
    "hold up two fingers on your left hand",
    "touch your right ear with your left hand",
    "hold a piece of paper with any number written on it up to the camera",
]

current_task = ""

agent = Agent(
    edge=getstream.Edge(),
    agent_user=User(
        name="Sentinel KYC",
        id="sentinel_kyc_agent"
    ),
    instructions=(
        "You are a KYC verification agent. "
        "Guide the user through a liveness check. "
        "Ask them to perform a physical task, wait for them to say Done, "
        "then verify they completed it. Be brief and clear."
    ),
    llm=openai.ChatCompletionsLLM(
        model="llama3.2:3b",
        base_url="http://127.0.0.1:11434/v1",
        api_key="local"
    ),
    vision_llm=openai.ChatCompletionsVLM(
        model="llama3.2-vision",
        base_url="http://127.0.0.1:11434/v1",
        api_key="local"
    ),
    stt=deepgram.STT(),
    tts=elevenlabs.TTS(),
)

# ---------------------------------------------------------
# Core Logic Functions
# ---------------------------------------------------------

async def start_kyc_session():
    global current_task
    current_task = random.choice(LIVENESS_TASKS)
    
    print(f"[SYSTEM] Assigned task: {current_task}")
    await agent.simple_response(
        f"To verify your identity, please {current_task}. Then say Done."
    )

async def trigger_kyc_check():
    global current_task
    print("[SYSTEM] Trigger word detected. Starting KYC check.")
    
    # Cut off whatever the agent is currently saying
    await agent.simple_response(
        "I heard you. Hold still for a moment.",
        interrupt=True
    )

    # Trigger frame capture and evaluate against the active task
    await agent.simple_response(
        "The user has completed the liveness task. "
        "Analyze their camera feed carefully. "
        f"Is the user clearly performing this action: {current_task}? "
        "Reply with ONLY one of these two strings: "
        "'SYSTEM: Verification successful' or "
        f"'SYSTEM: Please {current_task} and say Done again.'",
        interrupt=True
    )

@agent.events.subscribe
async def handle_transcript(event: STTTranscriptEvent):
    if event.participant.user.id == "sentinel_kyc_agent":
        return

    if event.is_final and event.confidence > 0.85 and "done" in event.text.lower():
        await trigger_kyc_check()


async def main():
    print("[SYSTEM] Initializing Sentinel KYC Agent...")
    
    await agent.start()
    
    await asyncio.sleep(2)
    await start_kyc_session()

    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[SYSTEM] Agent shut down safely.")