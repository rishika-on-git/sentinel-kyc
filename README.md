
# Sentinel KYC

An autonomous AI agent for running real-time, randomized video liveness checks. Built with the `vision_agents` SDK (v0.3.8) using local Ollama models to bypass rate limits.

Read the full build breakdown and architecture decisions on the blog: [I built an autonomous video KYC agent using vision agents. Here's the full story.](https://localhost-101.hashnode.dev/i-built-an-autonomous-video-kyc-agent-using-vision-agents-here-s-the-full-story)

## The Stack

* **Transport:** WebRTC via GetStream Edge
* **Listening:** Deepgram STT
* **Thinking (Text):** `llama3.2:3b` via Ollama
* **Thinking (Vision):** `llama3.2-vision` via Ollama
* **Speaking:** ElevenLabs TTS

## Setup

### 1. Clone and setup virtual environment

```bash
git clone [https://github.com/rishika-on-git/sentinel_kyc.git](https://github.com/rishika-on-git/sentinel_kyc.git)
cd sentinel_kyc
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

```

### 2. Install dependencies

```bash
pip install -r requirements.txt

```

### 3. Pull local models

Make sure [Ollama](https://ollama.com/) is installed and running on your machine, then pull the required models for text and vision processing:

```bash
ollama pull llama3.2:3b
ollama pull llama3.2-vision

```

### 4. Environment Variables

Copy the example environment file and fill in your API keys for Deepgram, GetStream, and ElevenLabs.

```bash
cp .env.example .env

```

### 5. Run the Agent

Once your environment is configured and Ollama is running in the background, start the agent:

```bash
python main.py

```
