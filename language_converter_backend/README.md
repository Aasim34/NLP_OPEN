# Indian Code-Mixed Language Converter - Backend

A FastAPI-based backend service that converts Hinglish (Hindi + English mixed) text into three formats:
1. **Hindi** (Devanagari script)
2. **Finglish** (Roman Hindi/Romanized Hindi)
3. **English** (Translation)

## Features

✅ **Fully Offline** - No external APIs required  
✅ **ML-Based** - Uses HuggingFace transformers for translation  
✅ **Phonetic Correction** - 250+ entry phonetic map for accurate transliteration  
✅ **Natural Output** - Reverse lookup for natural Finglish output  
✅ **Smart Punctuation** - Automatic comma and purna viram insertion for better translations  

## Tech Stack

- **Python 3.11+**
- **FastAPI** - Modern web framework
- **Transformers** - Helsinki-NLP/opus-mt-hi-en model
- **indic-transliteration** - ITRANS/IAST schemes
- **PyTorch** - ML model backend
- **NLTK** - Tokenization

## Installation

### 1. Install Dependencies

```powershell
cd language_converter_backend
pip install -r requirements.txt
```

### 2. Download NLTK Data (First Run Only)

```python
python -c "import nltk; nltk.download('punkt')"
```

## Running the Server

### Development Mode (Auto-reload)

```powershell
uvicorn main:app --reload
```

### Production Mode

```powershell
uvicorn main:app --host 0.0.0.0 --port 8000
```

Server will start at: **http://127.0.0.1:8000**

## API Documentation

### POST `/convert`

Convert Hinglish text to Hindi, Finglish, and English.

**Request:**
```json
{
  "text": "hello bhai kaise ho"
}
```

**Response:**
```json
{
  "hindi": "हेलो भाई कैसे हो",
  "finglish": "Hello bhai kaise ho",
  "english": "Hello, brother."
}
```

### GET `/`

Health check endpoint - returns service status.

### Interactive API Docs

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Project Structure

```
language_converter_backend/
├── main.py                      # FastAPI app entry point
├── requirements.txt             # Python dependencies
├── routes/
│   └── convert.py              # /convert endpoint
├── services/
│   ├── hinglish_to_hindi.py    # Hinglish → Hindi conversion
│   ├── hindi_to_finglish.py    # Hindi → Roman Hindi
│   └── hindi_to_english.py     # Hindi → English translation
└── utils/
    └── tokenizer.py            # Text normalization & tokenization
```

## Pipeline Architecture

```
Input: "mujhe new laptop kharidna hai"
         ↓
[1] Normalization (lowercase, strip)
         ↓
[2] Hinglish → Hindi (phonetic map + ITRANS)
         ↓ "मुझे न्यू लैपटॉप खरीदना है"
         ↓
[3] Hindi → Finglish (reverse lookup)
         ↓ "Mujhe new laptop kharidna hai"
         ↓
[4] Hindi → English (MarianMT transformer)
         ↓ "I want to buy a new laptop."
```

## Model Information

**Translation Model**: Helsinki-NLP/opus-mt-hi-en  
**Size**: ~300 MB  
**First Run**: Model downloads automatically from HuggingFace  
**Location**: `~/.cache/huggingface/transformers/`

## Testing

### Quick Test

```powershell
python -c "import requests; r = requests.post('http://127.0.0.1:8000/convert', json={'text': 'kal exam hai tayari kar lena'}); print(r.json())"
```

### Test Script

```powershell
python test_translation.py
```

## Example Outputs

| Input | Hindi | Finglish | English |
|-------|-------|----------|---------|
| hello bhai kaise ho | हेलो भाई कैसे हो | Hello bhai kaise ho | Hello, brother. |
| kal exam hai tayari kar lena | कल एग्ज़ाम है, तैयारी कर लेना | Kal exam hai tayari kar lena | Tomorrow, prepare. |
| mujhe chai chahiye | मुझे चाय चाहिए | Mujhe chai chahiye | I need tea. |

## CORS Configuration

The backend allows requests from:
- `http://localhost:5173` (Vite default)
- `http://localhost:3000` (React default)
- `http://127.0.0.1:5173`
- `http://127.0.0.1:3000`

To add more origins, edit `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://your-frontend-domain.com",  # Add here
    ],
    ...
)
```

## Known Limitations

1. **English Loanwords**: Words like "laptop" transliterated to Devanagari may not translate perfectly due to model vocabulary constraints
2. **Slang**: Very informal slang may need manual phonetic map entries
3. **Code-switching**: Best results with Hindi-dominant sentences

## Troubleshooting

### Model Download Fails
- Check internet connection
- Manually download from: https://huggingface.co/Helsinki-NLP/opus-mt-hi-en

### Import Errors
```powershell
pip install --upgrade -r requirements.txt
```

### Port Already in Use
```powershell
uvicorn main:app --port 8001
```

## Performance

- **Average Response Time**: 200-500ms
- **First Request**: 2-3s (model loading)
- **Concurrent Requests**: Supported via async FastAPI

## License

MIT License - Free for personal and commercial use

## Credits

- **Helsinki-NLP** for opus-mt-hi-en translation model
- **HuggingFace** for transformers library
- **indic-transliteration** for ITRANS support
