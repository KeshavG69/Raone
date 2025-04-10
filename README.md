# 🤖 Ra.One - Human-like AI WhatsApp Assistant

Ra.One is a sophisticated AI-powered WhatsApp assistant that delivers remarkably human-like conversations. Built on the [neural-maze/ava-whatsapp-agent-course](https://github.com/neural-maze/ava-whatsapp-agent-course) framework, Ra.One goes beyond basic chatbot functionality to provide natural, contextual, and emotionally intelligent interactions right in your WhatsApp conversations.

## ✨ Human-like Capabilities

- 🧠 **Contextual Understanding**: Maintains conversations across multiple messages
- 🗣️ **Natural Language**: Communicates with nuanced, human-like responses
- 🎭 **Emotional Intelligence**: Recognizes and responds appropriately to user emotions
- 🧩 **Personality**: Maintains a consistent, engaging personality throughout interactions
- 🤔 **Memory**: Remembers past conversations to provide personalized experiences

## 🚀 Key Features

- ✅ **WhatsApp Integration**: Seamless connection via WhatsApp Cloud API
- 💬 **Real-time AI Conversations**: Instant intelligent responses
- 🔊 **Voice Capabilities**: Converts voice messages to text and responds with natural voice
- 🔗 **Multi-turn Dialogues**: Maintains conversation context over time
- 📊 **Dual Memory System**: Postgres for short-term and Pinecone for long-term memory
- 🧰 **Extensible Architecture**: Easily add custom tools and capabilities
- 🔐 **Privacy-Focused**: Secure design with local-first approach

## 📱 Experience Ra.One

Chat with Ra.One like you would with a friend! It understands context, responds naturally, and gets smarter with every interaction.

![Ra.One in action](https://github.com/KeshavG69/RaOne/assets/your-user-id/raone-demo.mp4) <!-- Replace with actual demo video -->

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL database
- WhatsApp Business Account
- API keys (Groq, ElevenLabs, Pinecone, etc.)

### 1. Clone the Repository

```bash
git clone https://github.com/KeshavG69/RaOne.git
cd RaOne
```

### 2. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Edit the `.env` file with your API keys:

```
GROQ_API_KEY='your_groq_api_key'
ELEVENLABS_API_KEY='your_elevenlabs_key'
ELEVENLABS_VOICE_ID='your_voice_id'
PINECONE_API_KEY='your_pinecone_key'
PINECONE_ENVIRONMENT='your_pinecone_environment'
PINECONE_INDEX='your_pinecone_index'
TOGETHER_504='your_together_key'
WHATSAPP_TOKEN='your_whatsapp_token'
WHATSAPP_PHONE_NUMBER_ID='your_phone_number_id'
WHATSAPP_VERIFY_TOKEN='your_verify_token'
COHERE_API_KEY='your_cohere_key'
SHORT_TERM_MEMORY_DB_PATH='postgres-path'
```

### 4. Database Setup

Ra.One requires PostgreSQL for short-term memory storage. Ensure you have PostgreSQL installed and create a database for Ra.One to use. Configure the connection details in your `.env` file as shown above.

### 5. Launch the Webhook Server

```bash
uvicorn webhook_endpoint:app --host 0.0.0.0 --port 5000
```

### 6. Expose Your Webhook

Using Ngrok:

```bash
ngrok http 5000
```

### 7. Configure Meta Developer Portal

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Navigate to your app > WhatsApp > Configuration
3. Set your callback URL: `https://your-ngrok-url.ngrok.io/webhook`
4. Enter your verify token (same as `WHATSAPP_VERIFY_TOKEN`)

### 8. Start Chatting!

Your Ra.One assistant is now online and ready to engage in human-like conversations on WhatsApp.

## 🧠 Memory Architecture

Ra.One uses a sophisticated dual-memory system:

- **Short-term Memory (PostgreSQL)**: 
  Ra.One utilizes PostgreSQL as its short-term memory database to store recent conversations, user preferences, and contextual information. This relational database provides quick access to recent interactions, allowing Ra.One to maintain context during active conversations. The structured nature of PostgreSQL makes it perfect for storing conversation threads, user details, and immediate contextual data that Ra.One needs for responsive, coherent exchanges.

- **Long-term Memory (Pinecone)**:
  For deeper semantic understanding and long-term knowledge retention, Ra.One leverages Pinecone's vector database capabilities. Conversation histories are embedded into semantic vectors and stored in Pinecone, enabling Ra.One to retrieve relevant past interactions based on meaning rather than just keywords. This vector-based approach allows the assistant to maintain a more human-like memory of past conversations, recognizing patterns and recalling relevant information even months later.

- **Memory Integration**:
  The system seamlessly transitions information between short and long-term memory, with important conversational details gradually moving from PostgreSQL to Pinecone as they age. This dual-layer approach ensures Ra.One maintains both immediate responsiveness and long-term personalization, creating a more natural conversational experience.

## 🔧 Customization

Ra.One is designed to be highly customizable:

- **Personality Tuning**: Adjust conversation style in `prompt.py`
- **Memory Settings**: Configure memory retention periods and importance thresholds
- **Voice Characteristics**: Customize speech patterns via ElevenLabs
- **Custom Skills**: Add specialized capabilities through the modular architecture
- **Conversation Flow**: Design custom interaction patterns in `graph.py`

## 📁 Project Files

```
keshavg69-raone/
├── README.md               # Project documentation
├── app.py                  # Main application entry point
├── edges.py                # Connection definitions for graph
├── graph.py                # Conversation flow architecture
├── nodes.py                # Processing nodes for the graph
├── prompt.py               # Personality and instruction templates
├── requirements.txt        # Project dependencies
├── schedule.py             # Scheduled message functionality
├── schedule_manager.py     # Management of timed interactions
├── settings.py             # Configuration settings
├── speech_to_text.py       # Voice message processing
├── state.py                # Conversation state management
├── text_to_speech.py       # Voice response generation
├── utils.py                # Utility functions
├── webhook_endpoint.py     # WhatsApp webhook handler
├── whatsapp_response.py    # Response formatting for WhatsApp
├── memory/
│   ├── short_term.py       # PostgreSQL memory management
│   └── long_term.py        # Pinecone vector database interface
└── .env.example            # Environment variable template
```

## 👨‍💻 Contributing

Contributions are welcome to make Ra.One even more human-like and capable! Please feel free to:

- Submit pull requests with enhancements
- Report bugs or suggest features
- Share your custom personality configurations
- Add new integration modules

## 🚀 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Created with ❤️ by [Keshav Garg]gargkeshav504@gmail.com)

**"Ra.One: Your AI companion that feels like chatting with a friend"**
