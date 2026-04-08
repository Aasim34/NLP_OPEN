# Indian Code-Mixed Language Converter

A full-stack app for converting Hinglish text into three outputs:

1. Hindi in Devanagari script
2. Finglish, or Romanized Hindi
3. English translation

The local pipeline runs in the FastAPI backend. An optional GROQ-powered assistant output can be enabled through environment variables, but the core conversion flow does not require any external API.

## Overview

- Backend: FastAPI service in [Backend/main.py](Backend/main.py)
- Frontend: React + TypeScript app in [Frontend/src/app/App.tsx](Frontend/src/app/App.tsx)
- PowerShell scripts: [backend.ps1](backend.ps1), [frontend.ps1](frontend.ps1), [run.ps1](run.ps1)
- Test script: [test_optimizations.py](test_optimizations.py)

## Features

- Hinglish to Hindi transliteration with phonetic normalization
- Hindi to Finglish reverse transliteration
- Hindi to English translation using a local transformer model
- Optional GROQ assistant output when `GROQ_API_KEY` and `GROQ_MODEL` are configured
- CORS configured for local frontend development and common forwarded dev URLs
- React UI with copy-to-clipboard output cards and animated sections

## Repository Layout

```text
NLP_OPEN1/
├── Backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── routes/
│   ├── services/
│   └── utils/
├── Frontend/
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
├── backend.ps1
├── frontend.ps1
├── run.ps1
├── test_optimizations.py
└── README.md
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- PowerShell on Windows

## Setup

### 1. Clone and open the project

Open the repository root in VS Code or PowerShell.

### 2. Configure the backend environment

Copy [Backend/.env.example](Backend/.env.example) to [Backend/.env](Backend/.env) and fill in real values if you want the optional GROQ output.

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

If those values are not set, the app still works and returns the local Hindi, Finglish, and English outputs.

### 3. Install backend dependencies

```powershell
cd Backend
pip install -r requirements.txt
```

### 4. Install frontend dependencies

```powershell
cd Frontend
npm install
```

## Run

### Start backend only

```powershell
.\backend.ps1
```

Backend URL: `http://127.0.0.1:8000`

### Start frontend only

```powershell
.\frontend.ps1
```

Frontend URL: `http://localhost:5173`

### Start both services

Launch the backend and frontend scripts in separate PowerShell windows.

## Usage

1. Open the frontend at `http://localhost:5173`
2. Enter Hinglish text such as `kal meeting hai office me`
3. Click Convert
4. Read the Hindi, Finglish, English, and optional assistant output cards
5. Use the copy button on any result card to copy the text

## API

### `POST /convert`

Request body:

```json
{
     "text": "mujhe new laptop kharidna hai"
}
```

Response body:

```json
{
     "hindi": "मुझे न्यू लैपटॉप खरीदना है",
     "finglish": "Mujhe new laptop kharidna hai",
     "english": "I want to buy a new laptop.",
     "llm_output": "I want to buy a new laptop."
}
```

### `GET /`

Health check that returns the service status.

### `GET /docs`

Swagger UI for interactive API exploration.

## Conversion Flow

The backend pipeline performs these steps:

1. Normalize the input text
2. Convert Hinglish to Hindi using phonetic mapping and transliteration helpers
3. Convert Hindi to Finglish using reverse lookup rules
4. Translate Hindi to English with a local Helsinki-NLP transformer model
5. Optionally query GROQ for an additional assistant-style response

## Testing

Run the scripted backend checks from the repository root:

```powershell
python test_optimizations.py
```

You can also hit the API directly:

```powershell
curl -X POST http://127.0.0.1:8000/convert `
     -H "Content-Type: application/json" `
     -d '{"text":"hello bhai kaise ho"}'
```

## Troubleshooting

- If port 8000 is busy, change the backend port in the `uvicorn` command inside [backend.ps1](backend.ps1).
- If port 5173 is busy, change the Vite port in [frontend.ps1](frontend.ps1) or pass a different port to `npm run dev`.
- If the first backend request is slow, the translation model is likely still loading.
- If NLTK complains about missing data, download the required tokenizer package in the backend environment.

## Tech Stack

Backend:

- FastAPI
- Uvicorn
- Hugging Face Transformers
- PyTorch
- indic-transliteration
- NLTK
- Requests
- python-dotenv

Frontend:

- React 18
- TypeScript
- Vite
- Motion
- Tailwind CSS
- Radix UI
- Lucide React

## Notes

- The backend is designed to work without external services.
- GROQ is optional and only used when the environment variables are configured.
- The frontend talks to the backend on port 8000 by default.

## License

MIT License.
