# AI Chatbot with Particle Effects

A modern AI chat application with interactive particle background effects, featuring Google Gemini and Mistral AI integration.

## Features

- **Dual AI Support**: Google Gemini (primary) with automatic Mistral AI fallback
- **Interactive Particle Background**: WebGL-inspired canvas animation with anti-gravity effects
- **Email-based Chat Sessions**: Separate conversations for each user
- **Smart Date Separators**: Organized chat history with date markers
- **Mobile First Design**: Fully responsive for all devices
- **Custom Avatars**: Personalized AI and user avatars
- **Dark Theme**: Modern glass-morphism UI design
- **Real-time Updates**: Instant message delivery
- **Persistent Storage**: Supabase database integration

## Tech Stack

### Frontend
- React 19
- Vite 7
- Axios
- Canvas API (Particle System)
- CSS3 (Glass-morphism, Animations)

### Backend
- FastAPI
- Python 3.8+
- Supabase (PostgreSQL)
- Google Generative AI (Gemini)
- Mistral AI

## Installation

### Prerequisites
- Python 3.8+
- Node.js 18+
- Supabase account
- Google AI API key
- Mistral API key

### Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your API keys to .env
```

### Frontend Setup

```bash
cd frontend
npm install

# Create .env file (for production)
cp .env.example .env
# Add backend URL to .env
```

## 🏃 Running Locally

### Start Backend
```bash
cd backend
uvicorn main:app --reload
```
Backend runs at: http://localhost:8000

### Start Frontend
```bash
cd frontend
npm run dev
```
Frontend runs at: http://localhost:5173

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed Render deployment instructions.

### Quick Deploy Steps:
1. Push to GitHub
2. Connect to Render
3. Use `render.yaml` for automatic setup
4. Add environment variables
5. Deploy!

## Environment Variables

### Backend (.env)
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GOOGLE_API_KEY=your_google_api_key
MISTRAL_API_KEY=your_mistral_api_key
```

### Frontend (.env)
```env
VITE_API_URL=your_backend_url
```

## Database Schema

**Table: messages**
```sql
- id (UUID, Primary Key)
- role (TEXT) - 'user' or 'assistant'
- content (TEXT) - Message content
- email (TEXT) - User identifier
- created_at (TIMESTAMP) - Message timestamp
```

## Features Breakdown

### Particle Background
- 60fps canvas animation
- Anti-gravity mouse interaction
- Particle collision detection
- Ambient star field effect
- Pulsating radial gradient

### AI Integration
- Primary: Google Gemini 1.5 Flash
- Fallback: Mistral Medium
- Smart response formatting
- Context-aware replies

### User Experience
- Email-based sessions
- Date-separated history
- Typing indicators
- Error handling
- Auto-scroll
- Mobile optimized

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI app
│   ├── database.py          # Supabase operations
│   ├── ai_service.py        # AI model integration
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main app component
│   │   ├── App.css          # Styles
│   │   └── components/
│   │       └── ParticleBackground.jsx
│   ├── public/
│   │   └── assets/          # Avatar images
│   └── package.json
├── render.yaml              # Render deployment config
└── DEPLOYMENT.md            # Deployment guide
```

## Troubleshooting

**Backend not starting?**
- Check Python version (3.8+)
- Verify all environment variables
- Check Supabase connection

**Frontend not connecting?**
- Verify API_BASE_URL
- Check CORS settings
- Inspect browser console

**Particles not showing?**
- Check browser compatibility (Canvas API)
- Verify component import
- Check z-index layering

## API Endpoints

- `GET /api/messages?email={email}` - Fetch user's messages
- `POST /api/messages` - Send message and get AI response

## Future Enhancements

- [ ] Voice input/output
- [ ] File upload support
- [ ] Multi-language support
- [ ] Chat export/download
- [ ] User authentication
- [ ] Custom particle themes
- [ ] Message reactions

## License

MIT License - feel free to use for personal or commercial projects

## Author

Built by [Your Name]

## Acknowledgments

- Particle animation inspired by WebGL demos
- UI design influenced by modern chat applications
- Google Gemini & Mistral AI for powering conversations
