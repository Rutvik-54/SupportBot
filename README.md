# Emotional Support AI ChatBot

A modern, empathetic AI chatbot designed to provide emotional support and understanding through conversation. The chatbot features a beautiful, responsive interface and uses advanced AI to provide meaningful emotional support.

## Features

- Modern, responsive chat interface
- Real-time emotional analysis
- Empathetic AI responses
- Secure and private conversations
- Easy to use and intuitive design

## Prerequisites

- Python 3.7 or higher
- Gemin API key 
- Modern web browser

## Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd emotional-support-chatbot
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your Gemini API key:
```
Gemini_API_KEY=your_api_key_here
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Type your message in the chat input field
2. Press Enter or click the send button to send your message
3. The AI will analyze your message and respond with emotional support
4. Continue the conversation naturally

## Security and Privacy

- All conversations are processed in real-time and are not stored
- The application uses HTTPS for secure communication
- Your Gemini API key is kept secure in the `.env` file

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Gemini for providing the gemini-2.0-flash API
- Flask for the web framework
- NLTK for natural language processing capabilities 
