# 🌌 Space Eye

**Space Eye** is a comprehensive Django web application that integrates with NASA APIs to provide an immersive space exploration experience. Users can browse daily astronomy pictures, explore Mars through rover photos, and maintain personal collections of their favorite cosmic discoveries.

---

## ✨ Key Features

### 🌟 Astronomy Picture of the Day (APOD)
- Display NASA's daily featured astronomy image with detailed descriptions
- Browse historical images from the past 30 days with intuitive date selection
- High-quality images with scientific explanations from NASA astronomers
- Smart caching for optimal performance

### 🤖 Mars Rover Photo Gallery
- Access photos from **4 NASA Mars rovers**:
  - 🚗 **Curiosity** - The nuclear-powered geological laboratory
  - 🔍 **Opportunity** - The marathon rover (2004-2018)
  - 🎯 **Spirit** - The first of the twin rovers (2004-2010)  
  - 🦾 **Perseverance** - The latest advanced rover with helicopter companion
- Browse photos by **Sol** (Martian day) with customizable selection
- Display up to 12 high-resolution photos per page
- Detailed photo metadata including camera information and Earth dates

### 👤 User Authentication & Personalization
- **User Registration & Login System**
  - Custom user creation forms
  - Secure authentication with Django's built-in system
  - Welcome messages and user feedback
- **Personal Favorites Collection**
  - ⭐ Add/remove APOD images and Mars rover photos to favorites
  - 📋 Dedicated favorites page with filtering options
  - 🗂️ Filter favorites by type (APOD vs Mars Rover)
  - ❌ Delete individual favorites with confirmation
  - 💾 Persistent storage of user preferences

### ⚡ Advanced Technical Features
- **AJAX API Integration**
  - Asynchronous data loading for smooth user experience
  - Real-time favorite status updates
  - Dynamic content loading without page refreshes
- **Intelligent Caching System**
  - Redis/database caching for NASA API responses
  - Different cache durations for various content types
  - Fallback handling for API failures
- **Error Handling & Resilience**
  - Graceful degradation when APIs are unavailable
  - User-friendly error messages
  - Automatic retry mechanisms
- **Responsive Design**
  - Mobile-optimized interface
  - Cross-browser compatibility
  - Accessible user interface

---

## 🌠 Screenshots

### 🏠 Home Page - Astronomy Picture of the Day
![APOD Example](https://apod.nasa.gov/apod/image/2508/PerseidsDurdleDoor_Dury_960.jpg)
*Daily featured astronomy image with scientific description and date selection*

### 🚀 Mars Rover Photo Gallery
![Mars Rover Example](https://mars.nasa.gov/mars2020-raw-images/pub/ods/surface/sol/00516/ids/edr/browse/edl/EAE_0516_0712748775_129ECM_N0261222EDLC00516_0010LUJ01_1200.jpg)
*High-resolution photos from Mars rovers with detailed metadata*

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- pip package manager
- NASA API key (free registration required)

### 1. Clone the repository
```bash
git clone https://github.com/sakovolga/SpaceEye.git
cd SpaceEye
```

### 2. Create & activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate   # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables  
Create a `.env` file in the root directory:

```env
DEBUG=True
SECRET_KEY=your_django_secret_key_here
NASA_API_KEY=your_nasa_api_key_here
```

👉 **Get your NASA API Key**: [https://api.nasa.gov/](https://api.nasa.gov/) (Free registration)

### 5. Database setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create superuser (optional)
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```

🌐 **Access the application**: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🛰️ API Endpoints & URLs

### Public Pages
- `/` — Home page with APOD display
- `/mars_rover/` — Mars rover photos gallery
- `/register/` — User registration page

### Authenticated Pages
- `/favorites/` — Personal favorites collection
- `/favorites/?type=apod` — Filter APOD favorites only
- `/favorites/?type=mars_rover` — Filter Mars rover favorites only

### AJAX API Endpoints
- `/api/data/?type=apod&date=YYYY-MM-DD` — Get APOD data for specific date
- `/api/data/?type=mars_rover&rover=curiosity&sol=1000` — Get Mars rover photos
- `/add_to_favorites/` — Add item to user favorites (POST)
- `/remove_from_favorites/` — Remove item from favorites (POST)
- `/delete_favorite/<id>/` — Delete specific favorite item

### Available Rover Options
- `curiosity` — Curiosity Rover
- `opportunity` — Opportunity Rover  
- `spirit` — Spirit Rover
- `perseverance` — Perseverance Rover

---

## 📂 Project Structure
```
SpaceEye/
├── main/                     # Core application
│   ├── views.py             # NASA API integration & business logic
│   ├── models.py            # Database models (User, Favorites)
│   ├── forms.py             # Custom user creation forms
│   ├── templates/main/      # HTML templates
│   │   ├── index.html       # APOD home page
│   │   ├── mars_rover.html  # Mars rover gallery
│   │   └── favorites.html   # User favorites page
│   └── static/main/         # CSS, JavaScript, images
├── spaceeye/                # Django project configuration
│   ├── settings.py          # Project settings
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── templates/registration/   # Authentication templates
│   └── register.html        # User registration form
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

---

## 🛠️ Technologies & Dependencies

### Core Framework
- **Django 5.2.5** — Web framework
- **Python 3.10+** — Programming language

### Key Libraries
- **Requests 2.32.4** — HTTP library for NASA API calls
- **python-dotenv 1.1.1** — Environment variable management
- **Django Cache Framework** — Performance optimization
- **Django Authentication** — User management system

### External APIs
- **NASA APOD API** — Astronomy Picture of the Day
- **NASA Mars Photos API** — Mars rover image database

### Frontend Technologies
- **HTML5 & CSS3** — Modern web standards
- **JavaScript (AJAX)** — Dynamic user interactions
- **Responsive Design** — Mobile-friendly interface

---

## 🔧 Configuration Options

### Cache Settings
The application uses Django's cache framework with configurable timeouts:
- **APOD data**: 24 hours for historical dates, 2 hours for current day
- **Mars rover photos**: 7 days (photos don't change)
- **Error responses**: 5 minutes (for quick recovery)

### API Limits & Considerations
- **NASA API Rate Limits**: 1000 requests per hour (with API key)
- **Timeout Settings**: 10s for APOD, 15s for Mars rover requests
- **Photo Limits**: Maximum 12 photos displayed per Mars rover query

---

## 🎯 Usage Examples

### Browsing APOD
1. Visit the home page to see today's astronomy picture
2. Use the date dropdown to explore historical images (past 30 days)
3. Click the ⭐ button to add interesting images to your favorites

### Exploring Mars
1. Navigate to the Mars Rover section
2. Select your preferred rover (Curiosity, Opportunity, Spirit, or Perseverance)  
3. Choose a Sol (Martian day) to explore
4. Browse high-resolution photos and add favorites

### Managing Favorites
1. Register/login to access the favorites feature
2. Add images to your collection from APOD or Mars rover pages
3. Visit your favorites page to review your saved items
4. Filter by type or delete items as needed

---

## 🚀 Future Enhancements

### Planned Features
- 🌍 **NASA EPIC API Integration** — Earth imagery from space
- 🗺️ **Interactive Mars Maps** — Visualize rover locations and paths
- 📱 **Mobile App** — Native iOS/Android companion
- 🔍 **Advanced Search** — Filter by date ranges, cameras, and keywords
- 📊 **Statistics Dashboard** — Personal viewing history and analytics
- 🎨 **Custom Collections** — User-created themed galleries
- 🔄 **Infinite Scroll** — Seamless photo browsing experience
- 🌙 **Lunar Photos** — Integration with lunar mission data

### Technical Improvements
- **Docker Deployment** — Containerized application setup
- **PostgreSQL Support** — Production database integration
- **Redis Caching** — Enhanced performance with Redis
- **API Versioning** — RESTful API for mobile apps
- **WebSocket Integration** — Real-time updates and notifications

---

## 🤝 Contributing

We welcome contributions! Please feel free to:
- 🐛 Report bugs and issues
- 💡 Suggest new features  
- 🔧 Submit pull requests
- 📖 Improve documentation
- 🎨 Enhance UI/UX design

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- **NASA** — For providing incredible APIs and making space data accessible
- **Django Community** — For the robust web framework
- **Contributors** — Thank you to everyone who helps improve Space Eye

---

## 📞 Support

For questions, issues, or suggestions:
- 📧 **Email**: [your-email@example.com]
- 🐛 **Issues**: [GitHub Issues](https://github.com/sakovolga/SpaceEye/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/sakovolga/SpaceEye/discussions)

---

**🌌 Explore the cosmos with Space Eye — Your window to the universe!**