# Sentinel KYC

An autonomous AI agent for running real-time, randomized video liveness checks. Built with the `vision_agents` SDK (v0.3.8) using local Ollama models to bypass rate limits.

Read the full build breakdown and architecture decisions on the blog: **[https://localhost-101.hashnode.dev/i-built-an-autonomous-video-kyc-agent-using-vision-agents-here-s-the-full-story]**

## The Stack
* **Transport:** WebRTC via GetStream Edge
* **Listening:** Deepgram STT
* **Thinking (Text):** `llama3.2:3b` via Ollama
* **Thinking (Vision):** `llama3.2-vision` via Ollama
* **Speaking:** ElevenLabs TTS

## Setup

1. **Clone and setup virtual environment**
   ```bash
   git clone [https://github.com/rishika-on-git/sentinel_kyc.git](https://github.com/rishika-on-git/sentinel_kyc.git)
   cd sentinel_kyc
   python -m venv .venv
   source .venv/Scripts/activate    # Windows: .venv\Scripts\activate