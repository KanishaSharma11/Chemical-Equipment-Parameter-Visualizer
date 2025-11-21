# 🧪 Chemical Equipment Parameter Visualizer

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![React](https://img.shields.io/badge/react-18.0+-61DAFB.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)

**A powerful full-stack analytics platform for chemical equipment data analysis**

[Features](#-key-features) • [Quick Start](#-quick-start) • [Documentation](#-project-structure) • [Demo](#-testing-with-sample-data)

</div>

---

## 🌟 Overview

Transform your chemical equipment data into actionable insights with this comprehensive full-stack system. Upload CSV files, generate automated statistical summaries, visualize trends with interactive charts, and export professional PDF reports—all through an intuitive web or desktop interface.

### 🎯 What Makes This Special?

- **🔄 Dual Interface**: Choose between a modern web app or a powerful desktop application
- **🤖 Automated Analytics**: Instant statistical summaries without manual calculations
- **📈 Rich Visualizations**: Interactive charts that bring your data to life
- **📄 Professional Reports**: One-click PDF generation for presentations and documentation
- **🕐 Smart History**: Automatically stores your last 5 uploads for quick reference
- **🔗 Universal Backend**: Single Django API powers both interfaces seamlessly

---

## 🚀 Tech Stack

<table>
<tr>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg" width="60" height="60" />
<br><strong>React.js</strong>
<br><sub>Web Frontend</sub>
</td>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="60" height="60" />
<br><strong>PyQt5</strong>
<br><sub>Desktop App</sub>
</td>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg" width="60" height="60" />
<br><strong>Django</strong>
<br><sub>Backend API</sub>
</td>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg" width="60" height="60" />
<br><strong>Pandas</strong>
<br><sub>Data Processing</sub>
</td>
</tr>
</table>

### 📦 Complete Technology Breakdown

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **🌐 Web Frontend** | React.js + Chart.js | Modern, responsive UI with interactive visualizations |
| **🖥️ Desktop App** | PyQt5 + Matplotlib | Native desktop experience with advanced plotting |
| **🛠️ Backend API** | Django + DRF | RESTful API with robust data handling |
| **📊 Analytics** | Pandas + NumPy | High-performance data processing and statistics |
| **🗄️ Database** | SQLite | Lightweight storage for upload history |
| **🔐 Security** | Django Auth | Token-based authentication |
| **📝 Reporting** | ReportLab | Professional PDF generation |

---

## ✨ Key Features

### 📤 **CSV Upload - Dual Interface**
Upload equipment data seamlessly from either the web browser or desktop application. Drag-and-drop support with real-time validation.

### 📊 **Automated Statistical Analysis**
Instantly receive comprehensive summaries including:
- 📈 Total equipment count and distribution
- 🌡️ Average temperature, pressure, and flowrate metrics
- 📉 Min/max ranges and standard deviations
- 🏷️ Equipment type categorization and breakdown

### 🎨 **Interactive Visualizations**
- **Web Interface**: Dynamic Chart.js bar charts and pie graphs with hover tooltips
- **Desktop App**: High-resolution Matplotlib plots with export capabilities
- Real-time updates as data changes

### 🕰️ **Smart History Management**
- Automatically stores your last 5 uploads
- Quick access to previous datasets
- Compare historical trends
- Retrieve summaries via `/api/history/` endpoint

### 📄 **Professional PDF Reports**
Generate publication-ready reports with:
- Executive summary statistics
- Embedded visualizations
- Custom branding options
- One-click download

### 🔐 **Secure Authentication**
- Token-based API protection
- Secure upload endpoints
- User session management
- Role-based access control

### 🎁 **Bonus Features**
- 📋 Sample CSV included for instant testing
- 🔄 Real-time data validation
- 💾 Export capabilities (CSV, JSON, PDF)
- 🌙 Dark mode support (web interface)

---

## 📁 Project Structure

```
Chemical-Equipment-Parameter-Visualizer/
│
├── 🔧 backend/                      # Django REST API
│   ├── api/                         # API endpoints
│   ├── core/                        # Business logic
│   ├── models.py                    # Data models
│   ├── serializers.py               # DRF serializers
│   ├── views.py                     # API views
│   └── requirements.txt             # Python dependencies
│
├── 🌐 web-frontend/                 # React.js Application
│   ├── public/                      # Static assets
│   ├── src/
│   │   ├── components/              # React components
│   │   ├── services/                # API integration
│   │   ├── styles/                  # CSS/styling
│   │   └── App.js                   # Main app component
│   └── package.json                 # Node dependencies
│
├── 🖥️ desktop-app/                  # PyQt5 Application
│   ├── ui/                          # UI components
│   ├── utils/                       # Helper functions
│   ├── main.py                      # Application entry
│   └── requirements.txt             # Python dependencies
│
├── 📊 sample_equipment_data.csv     # Demo dataset
├── 📋 requirements.txt              # Global dependencies
├── 🐳 docker-compose.yml            # Docker setup (optional)
└── 📖 README.md                     # You are here!
```

---

## 🚀 Quick Start

### 📋 Prerequisites

Before you begin, ensure you have:
- ✅ Python 3.11 or higher
- ✅ Node.js 16+ and npm
- ✅ Git installed
- ✅ Virtual environment tool (recommended)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/Chemical-Equipment-Parameter-Visualizer.git
cd Chemical-Equipment-Parameter-Visualizer
```

---

## 🛠️ Backend Setup (Django + DRF)

### Step 1: Navigate to Backend

```bash
cd backend
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### Step 5: Launch Backend Server

```bash
python manage.py runserver
```

✅ **Success!** Your API is now running at: **http://127.0.0.1:8000**

📌 **API Endpoints Available:**
- `POST /api/upload/` - Upload CSV files
- `GET /api/summary/<id>/` - Get data summary
- `GET /api/history/` - View upload history
- `GET /api/report/<id>/` - Generate PDF report

---

## 🌐 Web Frontend Setup (React.js)

### Step 1: Navigate to Frontend

```bash
cd ../web-frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Configure API Endpoint (Optional)

Edit `.env` file to point to your backend:

```env
REACT_APP_API_URL=http://127.0.0.1:8000
```

### Step 4: Launch Development Server

```bash
npm start
```

✅ **Live!** Open your browser to: **http://localhost:3000**

🎨 **Features Available:**
- 📤 Drag-and-drop CSV upload
- 📊 Real-time chart updates
- 📜 History browser
- 📄 PDF report download

---

## 🖥️ Desktop App Setup (PyQt5 + Matplotlib)

### Step 1: Navigate to Desktop App

```bash
cd ../desktop-app
```

### Step 2: Verify Dependencies

```bash
# If not already installed with backend
pip install -r requirements.txt
```

### Step 3: Launch Desktop Application

```bash
python main.py
```

✅ **Running!** The desktop GUI should appear with:
- 🗂️ File browser for CSV selection
- 📊 Matplotlib visualization panel
- 📈 Statistics dashboard
- 💾 Export options

---

## 🧪 Testing with Sample Data

### 📊 Sample Dataset Included

We've included `sample_equipment_data.csv` with realistic chemical equipment parameters:

```csv
Equipment_ID,Type,Temperature_C,Pressure_bar,Flowrate_L_min
EQ001,Reactor,85.3,12.5,450.2
EQ002,Heat Exchanger,62.1,8.3,320.5
...
```

### 🎯 Quick Test Steps

**Option 1: Web Interface**
1. Navigate to http://localhost:3000
2. Click "Upload CSV" button
3. Select `sample_equipment_data.csv`
4. View instant analytics and charts

**Option 2: Desktop App**
1. Launch the desktop application
2. Click "Open File" → Select sample CSV
3. Explore visualizations in Matplotlib
4. Export to PDF if desired

**Option 3: API Direct**
```bash
curl -X POST http://127.0.0.1:8000/api/upload/ \
  -F "file=@sample_equipment_data.csv" \
  -H "Authorization: Token YOUR_TOKEN"
```

---

## 📚 API Documentation

### Authentication

```bash
# Get auth token
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -d '{"username":"admin","password":"password"}'
```

### Upload CSV

```bash
POST /api/upload/
Content-Type: multipart/form-data

Response: {
  "id": 1,
  "summary": {...},
  "timestamp": "2025-11-21T10:30:00Z"
}
```

### Get Summary

```bash
GET /api/summary/1/

Response: {
  "total_equipment": 50,
  "avg_temperature": 75.4,
  "avg_pressure": 10.2,
  "equipment_distribution": {...}
}
```

---

## 🎨 Screenshots

> **Note**: Add screenshots of your application here to showcase the UI

```
[Web Interface]     [Desktop App]     [PDF Report]
    📱                  🖥️                 📄
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. ✅ Commit changes (`git commit -m 'Add AmazingFeature'`)
4. 📤 Push to branch (`git push origin feature/AmazingFeature`)
5. 🔃 Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Authors

**Your Name** - *Initial work* - [GitHub Profile](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- Chart.js for beautiful web visualizations
- Matplotlib for powerful desktop plotting
- Django REST Framework for robust API development
- The open-source community for inspiration

---

## 📧 Contact & Support

- 📫 Email: your.email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/Chemical-Equipment-Parameter-Visualizer/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/Chemical-Equipment-Parameter-Visualizer/discussions)

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

**Made with ❤️ and ☕ for the chemical engineering community**

</div>
