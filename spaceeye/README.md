# 🌌 Space Eye

**Space Eye** is a Django application that integrates with NASA APIs to display:  
- 📷 **Astronomy Picture of the Day (APOD)**  
- 🤖 **Mars Rover Photos** (*Curiosity, Opportunity, Spirit, Perseverance*)  

The app caches API responses for better performance and supports date/sol selection.  

---

## 🚀 Features
- Home Page:
  - Astronomy Picture of the Day (APOD).  
  - Selectable date for the past 30 days.  
- Mars Rover Page:
  - Support for 4 NASA rovers.  
  - Select sol (Martian day).  
  - Up to 12 photos per page.  
- AJAX API for async data loading.  
- Caching for optimization.  

---
## 🌠 Screenshots

### Astronomy Picture of the Day (APOD)
![APOD Example](https://apod.nasa.gov/apod/image/2508/PerseidsDurdleDoor_Dury_960.jpg)

### Mars Rover Photos
![Mars Rover Example](https://mars.nasa.gov/mars2020-raw-images/pub/ods/surface/sol/00516/ids/edr/browse/edl/EAE_0516_0712748775_129ECM_N0261222EDLC00516_0010LUJ01_1200.jpg)

---
## ⚙️ Installation & Setup

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
Create a `.env` file in the root directory and add:  

```
DEBUG=True
SECRET_KEY=your_django_secret_key
NASA_API_KEY=your_nasa_api_key
```

👉 [Get a NASA API Key](https://api.nasa.gov/)  

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Run the development server
```bash
python manage.py runserver
```

App will be available at:  
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)  

---

## 📡 API Endpoints
- `/` — home page (APOD).  
- `/mars_rover/` — Mars rover photos page.  
- `/api/data/` — AJAX API:  
  - `?type=apod&date=YYYY-MM-DD`  
  - `?type=mars_rover&rover=curiosity&sol=1000`  

---

## 📂 Project Structure
```
SpaceEye/
│── main/                # Core application
│   ├── views.py          # NASA API logic
│   ├── templates/main/   # HTML templates
│── spaceeye/            # Django project configuration
│── manage.py
│── requirements.txt
│── README.md
```

---

## 🛰 Technologies
- **Python 3.10+**
- **Django 5.2.5**
- **Requests 2.32.4**
- **python-dotenv 1.1.1**
- **NASA Open APIs**
- **Django Cache**

---

## 📌 Roadmap
- Support for **EPIC (Earth Polychromatic Imaging Camera)** API.  
- Visualization of photos on an interactive map.  
- Infinite scrolling for rover photos.  
