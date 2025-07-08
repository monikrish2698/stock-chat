# Stock Chat - Natural Language Interface for Tabular Data

Stock Chat is a powerful application that enables users to interact with tabular data using natural language. Built with FastAPI and leveraging large language models, it provides an intuitive way to query and analyze data through simple chat-like interactions.

## Features

- **Natural Language Queries**: Ask questions about your data in plain English
- **FastAPI Backend**: High-performance API built with Python's FastAPI framework
- **Trino Integration**: Connect to and query various data sources through Trino
- **Redis Caching**: Improve performance with Redis-based caching
- **OpenAI Integration**: Leverage advanced language models for query understanding

## Prerequisites

- Python 3.9+
- Redis server
- Trino server (or compatible data source)
- OpenAI API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stock-chat.git
   cd stock-chat
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   cd db_assistant_api
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   REDIS_URL=redis://localhost:6379
   TRINO_HOST=your_trino_host
   TRINO_PORT=8080
   TRINO_USER=your_username
   TRINO_CATALOG=your_catalog
   TRINO_SCHEMA=your_schema
   ```

## Running the Application

1. Start the FastAPI server:
   ```bash
   cd db_assistant_api
   uvicorn db_assistant.main:app --reload
   ```

2. The API will be available at `http://localhost:8000`

3. Test the connection:
   ```bash
   curl http://localhost:8000/hello
   ```

## API Endpoints

- `POST /chat` - Send natural language queries and receive structured responses
- `GET /hello` - Test endpoint to verify the API is running

## Project Structure

```
stock-chat/
├── db_assistant_api/
│   ├── db_assistant/
│   │   ├── database/       # Database connection and query logic
│   │   ├── models/         # Pydantic models
│   │   ├── routes/         # API routes
│   │   ├── services/       # Business logic and LLM services
│   │   ├── main.py         # FastAPI application entry point
│   │   └── common_helper.py # Utility functions
│   └── requirements.txt    # Python dependencies
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
