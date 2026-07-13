# ScriptFlow

The world's most beautiful AI-ready creator platform with an advanced teleprompter.

![ScriptFlow](https://img.shields.io/badge/Version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11+-green.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey.svg)

## Features

- **Ultra Smooth Scrolling** - GPU-accelerated 60 FPS scrolling
- **AI Ready** - Powered by advanced AI features
- **Offline Mode** - Works completely offline as a PWA
- **Cloud Sync** - Your scripts are automatically backed up
- **Premium Design** - Apple/Linear-inspired beautiful interface
- **Responsive** - Works on desktop, tablet, and mobile
- **PWA Install** - Install as a native app on any device
- **Camera Mode** - Record video with teleprompter overlay
- **Multiple Themes** - Dark, Light, OLED, Ocean, Emerald, and more

## Tech Stack

### Backend
- Flask 3.0
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- SQLite (easily scalable to PostgreSQL/MySQL)

### Frontend
- HTML5
- Tailwind CSS (CDN)
- Vanilla JavaScript ES6+
- GSAP Animations
- Inter Font Family
- PWA with Service Worker

## Deployment

This application is designed to deploy directly to **cPanel/Shared Hosting** with **Passenger WSGI**.

### Requirements
- Python 3.11+
- Apache with Passenger
- No Docker, VPS, or complex setup required

### Deployment Steps

1. **Upload Files**
   ```bash
   # Upload all files to your cPanel public_html or subdomain directory
   ```

2. **Create Python Application**
   - In cPanel, go to "Setup Python App"
   - Click "Create Application"
   - Set the App directory to your uploaded files
   - Python version: 3.11+

3. **Install Dependencies**
   ```bash
   # SSH into your hosting or use cPanel terminal
   pip install -r requirements.txt
   ```

4. **Restart Application**
   - Click "Restart" in the Python App setup

That's it! Your app should be live.

## Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/scriptflow.git
cd scriptflow

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit `http://localhost:5000` in your browser.

### Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

## Project Structure

```
ScriptFlow/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── passenger_wsgi.py      # cPanel Passenger WSGI handler
├── .env                   # Environment variables
├── .env.example           # Example environment file
│
├── blueprints/            # Flask blueprints
│   ├── auth.py           # Authentication routes
│   ├── dashboard.py      # Dashboard routes
│   ├── api.py            # API endpoints
│   └── admin.py         # Admin panel
│
├── models/               # Database models
│   ├── user.py          # User model
│   └── script.py         # Script model
│
├── services/             # Business logic
│   ├── auth_service.py  # Authentication service
│   └── script_service.py # Script service
│
├── utils/               # Utility functions
│   └── logging.py       # Application logging
│
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── landing.html     # Landing page
│   ├── errors/          # Error pages (404, 500)
│   ├── auth/            # Auth templates
│   └── dashboard/       # Dashboard templates
│
├── static/              # Static files
│   ├── css/            # CSS files
│   ├── js/             # JavaScript files
│   └── images/         # Images
│
├── tests/               # Test suite
│   ├── unit/          # Unit tests
│   ├── integration/    # Integration tests
│   └── fixtures/      # Test fixtures
│
└── instance/            # Instance files
    └── database.db      # SQLite database
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `development` |
| `SECRET_KEY` | Flask secret key | (change in production) |
| `DATABASE_URL` | Database connection | SQLite path |

### Database Scalability

The application uses SQLAlchemy, making it easy to migrate from SQLite to PostgreSQL or MySQL:

```python
# For PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/scriptflow

# For MySQL
DATABASE_URL=mysql://user:password@localhost/scriptflow
```

## PWA Features

ScriptFlow includes full PWA support:

- **manifest.json** - App manifest with icons and shortcuts
- **service-worker.js** - Offline caching and background sync
- **Install Prompt** - Elegant in-app install banner
- **Offline Mode** - Works without internet connection

## API Endpoints

### Scripts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/scripts` | List all scripts |
| POST | `/api/scripts` | Create a script |
| GET | `/api/scripts/<id>` | Get a script |
| PUT | `/api/scripts/<id>` | Update a script |
| DELETE | `/api/scripts/<id>` | Delete a script |
| POST | `/api/scripts/<id>/favorite` | Toggle favorite |
| POST | `/api/scripts/<id>/duplicate` | Duplicate a script |

### User

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/user/stats` | Get user statistics |
| PUT | `/api/user/theme` | Update user theme |

### Admin

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin` | Admin dashboard |
| GET | `/admin/users` | List all users |
| GET | `/admin/scripts` | List all scripts |
| GET | `/admin/database` | Database stats |
| GET | `/admin/export` | Export database |

## Keyboard Shortcuts

### Teleprompter Mode

| Shortcut | Action |
|----------|--------|
| `Space` | Play/Pause |
| `↑` / `W` | Increase speed |
| `↓` / `S` | Decrease speed |
| `←` / `→` | Adjust font size |
| `F` | Fullscreen |
| `M` | Mirror mode |
| `R` | Restart |
| `Esc` | Exit |

### Global

| Shortcut | Action |
|----------|--------|
| `⌘K` | Command palette |
| `⌘S` | Save (in editor) |

## Touch Gestures

| Gesture | Action |
|---------|--------|
| Single Tap | Show/hide controls |
| Double Tap | Toggle play/pause |
| Swipe Up | Increase speed |
| Swipe Down | Decrease speed |
| Pinch | Adjust font size |

## Troubleshooting

### Database Issues

If you encounter database errors:
```bash
# Recreate the database
rm instance/database.db
python -c "from app import create_app; app = create_app()"
```

### Import Errors

If modules can't be found:
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### cPanel Deployment Issues

1. Ensure Python version is 3.11+
2. Check the error log in cPanel Python App settings
3. Verify the application directory path is correct
4. Make sure passenger_wsgi.py is in the root directory

## Performance

- Lighthouse Score: 95+
- Supports 100,000+ word scripts
- 60 FPS scrolling using requestAnimationFrame
- Optimized for mobile devices
- Service Worker caching for offline use

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Security

- CSRF Protection on all forms
- Secure session cookies
- Password hashing with Werkzeug
- Input validation with WTForms
- SQL injection protection via SQLAlchemy

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting a PR.

---

Built with ❤️ by ScriptFlow Team