# 🌐 Indian Code-Mixed Language Converter

A full-stack web application that converts **Hinglish** (Hindi + English mixed) text into three formats:
1. **Hindi** (Devanagari script)
2. **Finglish** (Romanized Hindi)  
3. **English** (Translation)

Built with FastAPI backend and React frontend, this application runs **completely offline** without requiring any external APIs.

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Node](https://img.shields.io/badge/node-18+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## ✨ Features

### Backend
- ✅ **Fully Offline** - No external API calls
- ✅ **ML-Based Translation** - Uses Helsinki-NLP/opus-mt-hi-en transformer
- ✅ **250+ Phonetic Map** - Accurate Hinglish to Hindi conversion
- ✅ **Smart Punctuation** - Automatic comma and purna viram insertion
- ✅ **Natural Finglish** - Reverse lookup for readable Roman Hindi
- ✅ **FastAPI** - Modern, fast Python web framework
- ✅ **CORS Enabled** - Ready for frontend integration

### Frontend
- ✨ **Beautiful UI** - Gradient backgrounds & smooth animations
- ✨ **Motion Animations** - Powered by Framer Motion
- ✨ **Copy to Clipboard** - One-click copy for all outputs
- ✨ **Type-Safe** - Full TypeScript support
- ✨ **Fast Development** - Vite with instant HMR
- ✨ **Responsive Design** - Works on mobile & desktop

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)

### Installation

1. **Clone or Download** this project

2. **Run the launcher script** (Windows):

```powershell
.\run_servers.ps1
```

This script will:
- ✅ Check prerequisites
- ✅ Install dependencies (if needed)
- ✅ Start backend server at `http://127.0.0.1:8000` in a new window
- ✅ Start frontend server at `http://localhost:5173` in a new window
- ✅ Open the application in your browser

**Alternative**: Start servers individually:
```powershell
# Start only backend
.\start_backend.ps1

# Start only frontend  
.\start_frontend.ps1
```

### Manual Setup

#### Backend Setup

```powershell
cd language_converter_backend
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend Setup

```powershell
cd Frontend
npm install
npm run dev
```

---

## 📖 Usage

1. **Open** the application at `http://localhost:5173`
2. **Type** Hinglish text in the input box
   - Example: `"hello bhai kaise ho"`
3. **Click** the "Convert" button
4. **View** three outputs:
   - **Hindi**: हेलो भाई कैसे हो
   - **Finglish**: Hello bhai kaise ho
   - **English**: Hello, brother.
5. **Copy** any output using the copy button

---

## 📂 Project Structure

```
NLP_OPEN1/
├── language_converter_backend/     # FastAPI backend
│   ├── main.py                     # Entry point
│   ├── routes/                     # API endpoints
│   ├── services/                   # Conversion logic
│   ├── utils/                      # Tokenizer utilities
│   └── requirements.txt            # Python dependencies
│
├── Frontend/                       # React frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── App.tsx            # Main component
│   │   │   └── components/        # UI components
│   │   └── main.tsx               # Entry point
│   ├── vite.config.ts             # Vite configuration
│   └── package.json               # Node dependencies
│
├── run_servers.ps1                # Launcher script
├── test_translation.py            # Backend test script
└── README.md                      # This file
```

---

## 🔧 API Reference

### POST `/convert`

Convert Hinglish text to all three formats.

**Request:**
```json
{
  "text": "mujhe new laptop kharidna hai"
}
```

**Response:**
```json
{
  "hindi": "मुझे न्यू लैपटॉप खरीदना है",
  "finglish": "Mujhe new laptop kharidna hai",
  "english": "I want to buy a new laptop."
}
```

### GET `/`
Health check endpoint

### GET `/docs`
Interactive API documentation (Swagger UI)

---

## 📊 Example Outputs

| Input | Hindi | Finglish | English |
|-------|-------|----------|---------|
| hello bhai kaise ho | हेलो भाई कैसे हो | Hello bhai kaise ho | Hello, brother. |
| kal exam hai tayari kar lena | कल एग्ज़ाम है, तैयारी कर लेना | Kal exam hai tayari kar lena | Tomorrow, prepare. |
| mujhe chai chahiye | मुझे चाय चाहिए | Mujhe chai chahiye | I need tea. |
| office me meeting hai | ऑफिस में मीटिंग है | Office me meeting hai | There's a meeting in office. |

---

## 🧠 How It Works

### Pipeline Architecture

```
Input: "hello bhai kaise ho"
         ↓
[1] Normalization
    (lowercase, strip whitespace)
         ↓
[2] Hinglish → Hindi
    (Phonetic map + ITRANS transliteration)
         ↓
    "हेलो भाई कैसे हो"
         ↓
[3] Hindi → Finglish
    (Reverse phonetic lookup + ITRANS)
         ↓
    "Hello bhai kaise ho"
         ↓
[4] Hindi → English
    (MarianMT transformer with beam search)
         ↓
    "Hello, brother."
```

### Key Components

1. **Spelling Normalization** - Corrects common misspellings
2. **Phonetic Fixes Map** - 250+ entries for accurate conversion
3. **Hindi Punctuation** - Adds commas at clause boundaries
4. **Reverse Lookup** - Natural Finglish from phonetic map
5. **MarianMT Model** - Helsinki-NLP/opus-mt-hi-en for translation

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **HuggingFace Transformers** - ML models
- **PyTorch** - Deep learning backend
- **indic-transliteration** - ITRANS/IAST support
- **NLTK** - Natural language toolkit

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Motion (Framer Motion)** - Animations
- **Tailwind CSS** - Styling
- **Radix UI** - Accessible components
- **Lucide React** - Icons

---

## 📝 Testing

### Backend Tests

```powershell
python test_translation.py
```

### API Test

```powershell
curl -X POST http://127.0.0.1:8000/convert `
  -H "Content-Type: application/json" `
  -d '{"text": "hello bhai"}'
```

---

## 🐛 Known Limitations

1. **English Loanwords**: Technical terms transliterated to Devanagari may not translate perfectly (e.g., "laptop" → "flater")
2. **Slang**: Very informal slang may need manual phonetic map entries
3. **Code-switching**: Best results with Hindi-dominant sentences
4. **Model Size**: First run downloads ~300 MB translation model

---

## 🔧 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```powershell
uvicorn main:app --port 8001
```

**Model download fails:**
- Check internet connection (first run only)
- Download manually from [HuggingFace](https://huggingface.co/Helsinki-NLP/opus-mt-hi-en)

### Frontend Issues

**Port 5173 already in use:**
```powershell
npm run dev -- --port 3000
```

**Dependencies not found:**
```powershell
rm -rf node_modules package-lock.json
npm install
```

---

## 📄 Documentation

- **Backend README**: [language_converter_backend/README.md](language_converter_backend/README.md)
- **Frontend README**: [Frontend/README.md](Frontend/README.md)
- **Translation Fix Summary**: [TRANSLATION_FIX_SUMMARY.md](TRANSLATION_FIX_SUMMARY.md)

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📜 License

This project is licensed under the **MIT License** - free for personal and commercial use.

---

## 🙏 Credits

- **Helsinki-NLP** - opus-mt-hi-en translation model
- **HuggingFace** - Transformers library
- **indic-transliteration** - ITRANS support
- **Framer Motion** - Animation library
- **Radix UI** - Accessible components

---

## 📧 Support

For issues, questions, or feature requests:
- Create an issue on the project repository
- Check existing documentation
- Review troubleshooting section

---

## 🎯 Roadmap

- [ ] Support for more Indian languages (Marathi, Gujarati, Tamil)
- [ ] Better model for English loanwords
- [ ] Voice input support
- [ ] Save/export conversion history
- [ ] Dark mode support
- [ ] Mobile app version

---

**Made with ❤️ for Indian language processing**
