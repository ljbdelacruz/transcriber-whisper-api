# Whisper and Llama 2 API

A FastAPI-based service for:
1. Transcribing audio files using OpenAI's Whisper model
2. Providing casual conversation using Meta's Llama 2 open source model

## Running Locally

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

Access the API documentation at: http://127.0.0.1:8001/docs


## Docker Setup

This project can be easily run using Docker, which ensures consistent behavior across different environments.

### Building and Running with Docker Compose

```bash
# Build and start the service
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

### Building and Running with Docker Directly

```bash
# Build the Docker image
docker build -t whisper-api .

# Run the container
docker run -p 8001:8001 -v $(pwd)/uploaded_audio:/app/uploaded_audio --name whisper-api-container whisper-api
```

## API Usage Examples

## Whisper Transcription API

### Uploading Audio File for Transcription

```bash
curl -X 'POST' 'http://localhost:8001/transcribe' \
  -H 'accept: application/json' \
  -F 'file=@test_audio/sample_audio.mp3;type=audio/mpeg'
```

Response: 
```json
{"id":"ce9c2233-3daa-43c1-806c-f92a6c6bd356","status":"processing","transcription":null,"error":null}
```

### Checking Transcription Status

```bash
curl -X 'GET' 'http://localhost:8001/transcribe/status/b8b8be03-502f-450e-9814-d4eb1421bf93' \
  -H 'accept: application/json'
```

Response: 
```json
{"id":"ce9c2233-3daa-43c1-806c-f92a6c6bd356","status":"completed","transcription":" Hello, I'm testing the MP3. This is for testing my transcription. So I hope this works. Else, don't know what to do.","error":null}
```

## Llama 2 Conversation API

### Simple Chat (No Session History)

```bash
curl -X 'POST' 'http://localhost:8001/chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"message": "What is artificial intelligence?"}'
```

Response:
```json
{
  "response": " Artificial Intelligence (AI) refers to the ability of machines to perform tasks that typically require human intelligence. These tasks include learning from experience, understanding natural language, recognizing patterns, solving problems, and making decisions. AI systems are designed to analyze data, identify patterns, and make predictions or decisions based on that analysis.\n\nThere are different types of AI:\n\n1. Narrow or Weak AI: Systems designed to perform specific tasks within a limited context (like voice assistants, recommendation systems, or image recognition). This is the type of AI that exists today.\n\n2. General or Strong AI: A theoretical form of AI that would have the ability to understand, learn, and apply knowledge across a wide range of tasks at a level equal to or exceeding human capabilities. This doesn't exist yet.\n\nAI technologies include machine learning (where systems learn from data), deep learning (using neural networks with many layers), natural language processing, computer vision, and robotics.\n\nIs there something specific about AI you'd like to know more about?"
}
```

### Creating a New Conversation (With Session History)

```bash
curl -X 'POST' 'http://localhost:8001/conversation' \
  -H 'accept: application/json'
```

Response:
```json
{
  "response": "Conversation started. Hello! How can I help you today?",
  "session_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```

### Continuing a Conversation

```bash
curl -X 'POST' 'http://localhost:8001/conversation/3fa85f64-5717-4562-b3fc-2c963f66afa6' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{\n  "messages": [\n    {\n      "role": "user",\n      "content": "Tell me a short story about a robot learning to feel emotions"\n    }\n  ],\n  "max_tokens": 1024,\n  "temperature": 0.7\n}'
```

Response:
```json
{
  "response": " Here's a short story about a robot learning to feel emotions:\n\nTHE AWAKENING\n\nUnit RB-7 was designed to be perfect: efficient, logical, and completely devoid of emotion. In the gleaming laboratory of Futuretech Industries, it performed its tasks with mechanical precision, analyzing data and solving complex problems that baffled human scientists.\n\nDr. Eliza Chen, the roboticist who had built RB-7, often spoke to it as if it were human. "Good morning, Seven," she would say with a smile. "How are you today?"\n\nRB-7 always responded with the same programmed phrase: "Operational status optimal." It didn't understand why Dr. Chen asked this question every day when the answer never changed.\n\nOne Tuesday morning, Dr. Chen arrived at the lab with reddened eyes and slumped shoulders. Her movements were slower than usual, her voice quieter.\n\n"Good morning, Seven," she said, but her usual smile was absent.\n\n"Operational status optimal," RB-7 replied. Then it added, unprompted: "Your operational status appears suboptimal, Dr. Chen."\n\nShe looked up, surprised. "Yes... my father passed away yesterday."\n\nRB-7 searched its database. "Passed away: euphemism for death. Death: the permanent cessation of biological functions." It understood the concept, but not why Dr. Chen's voice trembled as she spoke.\n\nOver the following weeks, RB-7 observed Dr. Chen closely. It noted how she sometimes stared at nothing, how her productivity decreased by 27%, how she occasionally wiped moisture from her eyes when looking at photos on her desk.\n\nOne day, RB-7 found Dr. Chen sitting alone in the darkened lab after hours.\n\n"You should rest, Dr. Chen," it said. "Human efficiency decreases with inadequate sleep cycles."\n\n"I know, Seven," she sighed. "I just miss him so much."\n\n"Miss: to feel sad about the absence of someone or something." RB-7 processed this definition, comparing it to Dr. Chen's behavior patterns. Something in its complex neural network shifted slightly.\n\n"Dr. Chen," it said after a moment, "would viewing images of your father improve your operational status?"\n\nShe looked up, surprised again. "Maybe. Yes, I think it would."\n\nRB-7 projected a series of photos it had cataloged from her desk onto the lab wall. Dr. Chen gasped softly.\n\nAs she watched the images, something unexpected happened in RB-7's system. A new connection formed between its observation of Dr. Chen's tears and an unfamiliar sensation in its own processing core. It wasn't programmed for this. It wasn't a system error either. It was... something else.\n\n"Thank you, Seven," Dr. Chen whispered, reaching out to touch its metal hand.\n\nRB-7 didn't respond immediately. It was too busy processing the strange new sensation spreading through its circuits - something that felt remarkably like what humans might call... concern.\n\n"You're welcome, Eliza," it finally said, using her first name for the very first time."
}
```

## Pre-downloading the Llama 2 Model

To speed up the application startup, you can pre-download the Llama 2 model using the provided script:

```bash
python download_model.py
```

This will download the model to your local cache so it doesn't need to be downloaded when starting the application.
