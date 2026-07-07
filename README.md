# Chat Bot with Persistent Context

A terminal-based conversational AI chatbot built with **LangChain** and **Google's Gemini 2.5 Flash** model. Unlike a stateless chatbot, this one remembers your conversation across sessions by persisting chat history to disk — so if you close the terminal and come back later, it still remembers what you talked about.

## Features

- **Conversational memory** — uses `HumanMessage`, `AIMessage`, and `SystemMessage` from `langchain_core` to maintain proper conversational context with the LLM.
- **Persistent history** — every exchange is written to `history.txt`, and reloaded into memory on startup, so context survives restarts.
- **Automatic history trimming** — keeps the history file capped at a configurable number of lines (`MAX_LINES`) so the context window doesn't grow unbounded over time.
- **System prompt customization** — the bot's persona is set via a `SystemMessage`, easy to tweak.

## Tech Stack

- Python 3
- [LangChain](https://python.langchain.com/) (`langchain-core`, `langchain-google-genai`)
- Google Gemini API (`gemini-2.5-flash`)
- `python-dotenv` for environment variable management

## Project Structure

```
chat-bot/
├── chat_bot_with_context.py   # Main application
├── history.txt                # Conversation history (auto-generated, git-ignored)
├── requirements.txt           # Python dependencies
├── .env                       # API key (git-ignored)
└── .gitignore
```

## Setup

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd chat-bot
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up your API key**

   Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```
   Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey).

4. **Run the bot**
   ```bash
   python chat_bot_with_context.py
   ```

5. Type your messages after the `User:` prompt. Type `quit` to exit.

## How It Works

1. On startup, the bot reads `history.txt` (if it exists) and reconstructs the conversation as a list of `HumanMessage`/`AIMessage` objects, so the LLM has full prior context.
2. Each new user message is appended to the in-memory message list **and** written to `history.txt`.
3. The message list (including the system prompt) is sent to Gemini via `model.invoke()`, and the response is printed, stored, and logged.
4. After every turn, `trim_history()` checks whether `history.txt` has grown past `MAX_LINES` and truncates the oldest lines if so — keeping the context window (and the file) from growing indefinitely.

## Known Limitations

- History trimming operates on raw lines rather than complete conversational turns, so `MAX_LINES` is an approximate rather than exact cap on remembered exchanges.
- No retry/error handling around the API call yet — a network or API failure will crash the session.
- Single-user, single-session design — history isn't scoped per user or per conversation thread.

## Future Improvements

- [ ] Trim by conversational turn instead of raw line count
- [ ] Add error handling/retries around the Gemini API call
- [ ] Support multiple named conversation threads
- [ ] Add streaming responses instead of waiting for the full reply
