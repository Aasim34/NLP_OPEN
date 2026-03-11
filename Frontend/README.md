
# Indian Code-Mixed Language Converter - Frontend

A modern, animated React + TypeScript frontend for converting Hinglish (Hindi + English mixed) text into Hindi, Finglish, and English.

## Features

✨ **Beautiful UI** - Gradient backgrounds with smooth animations  
🎨 **Motion Animations** - Powered by Framer Motion  
📋 **Copy to Clipboard** - One-click copy for all outputs  
⚡ **Fast & Responsive** - Built with Vite for instant HMR  
🎯 **Type-Safe** - Full TypeScript support  

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool & dev server
- **Motion (Framer Motion)** - Animations
- **Tailwind CSS** - Utility-first styling
- **Radix UI** - Accessible components
- **Lucide React** - Icons

## Installation

### 1. Install Dependencies

```powershell
cd Frontend
npm install
```

## Running the Dev Server

```powershell
npm run dev
```

Frontend will start at: **http://localhost:5173**

## Building for Production

```powershell
npm run build
```

Build output goes to `dist/` folder.

### Preview Production Build

```powershell
npm run preview
```

## Project Structure

```
Frontend/
├── src/
│   ├── app/
│   │   ├── App.tsx              # Main application component
│   │   └── components/
│   │       ├── Navigation.tsx   # Top navigation bar
│   │       ├── OutputCard.tsx   # Output display cards
│   │       └── FeatureCard.tsx  # Feature highlights
│   ├── main.tsx                 # App entry point
│   └── index.css                # Global styles
├── public/                      # Static assets
├── vite.config.ts              # Vite configuration
├── tailwind.config.ts          # Tailwind configuration
├── tsconfig.json               # TypeScript configuration
└── package.json                # Dependencies
```

## API Integration

The frontend calls the FastAPI backend at:
```
POST http://localhost:8000/convert
```

**Request:**
```typescript
{
  text: string  // Hinglish input
}
```

**Response:**
```typescript
{
  hindi: string     // Devanagari output
  finglish: string  // Roman Hindi
  english: string   // English translation
}
```

## Key Components

### App.tsx
Main application with:
- Input textarea for Hinglish text
- Convert button with loading state
- Three output cards (Hindi, Finglish, English)
- Error handling

### OutputCard.tsx
Reusable card component with:
- Title and gradient background
- Copy to clipboard button
- Motion animations
- Tooltip on copy

### Navigation.tsx
Top navigation bar with:
- App title and logo
- Gradient text effect

## Customization

### Colors
Edit gradients in `src/app/App.tsx`:

```typescript
// Hindi Card
gradient="from-blue-500 to-purple-600"

// Finglish Card
gradient="from-green-500 to-teal-600"

// English Card
gradient="from-orange-500 to-red-600"
```

### Animations
Edit motion settings in `src/app/components/OutputCard.tsx`:

```typescript
initial={{ opacity: 0, y: 20 }}
animate={{ opacity: 1, y: 0 }}
transition={{ duration: 0.3, delay }}
```

## Environment Configuration

Create `.env` file for custom backend URL:

```env
VITE_API_URL=http://localhost:8000
```

Then use in code:
```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

## Proxy Configuration

The Vite config includes a proxy for `/api` routes:

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, ''),
    },
  },
}
```

Use with:
```typescript
fetch('/api/convert', { ... })  // Proxies to http://localhost:8000/convert
```

## Error Handling

The app handles:
- **Backend Offline**: Shows error message in output cards
- **Empty Input**: Convert button disabled
- **Network Errors**: Displays user-friendly error message

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Performance

- **Build Size**: ~150 KB (gzipped)
- **First Paint**: < 1s
- **Animations**: 60 FPS

## Keyboard Shortcuts

- **Ctrl/Cmd + Enter** - Submit input (future feature)
- **Ctrl/Cmd + C** - Copy output (future feature)

## Accessibility

- Semantic HTML
- ARIA labels on buttons
- Keyboard navigation support
- Screen reader friendly

## Troubleshooting

### Port 5173 Already in Use
```powershell
npm run dev -- --port 3000
```

### Module Not Found
```powershell
rm -rf node_modules package-lock.json
npm install
```

### Tailwind Not Working
```powershell
npm run dev
# Vite will rebuild Tailwind
```

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint (if configured) |

## License

MIT License - Free for personal and commercial use

## Credits

- **Radix UI** for accessible primitives
- **Lucide** for beautiful icons
- **Framer Motion** for smooth animations
- **Tailwind CSS** for utility classes
  