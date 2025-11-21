# 🧪 Chemical Equipment Parameter Visualizer

<div align="center">

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

---

## 📁 Project Structure

```
Chemical-Equipment-Parameter-Visualizer/
│
├── 🔧 backend/                      # Django REST API
│   ├── core/                        # Business logic
│   ├── equipment
│   ├── media
│   ├── manage.py
│
├── 🌐 web-frontend/                 # React.js Application
│   ├── public/                      # Static assets
│   ├── src/
│   │   ├── api.js
│   │   ├── App.css                  # CSS/styling
│   │   └── App.js                   # Main app component
│   └── package.json                 # Node dependencies
│
├── 🖥️ desktop-app/                  # PyQt5 Application
│   ├── main.py                      # Application entry
│
├── 📊 sample_equipment_data.csv     # Demo dataset
├── 📋 requirements.txt              # Global dependencies
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
git clone https://github.com/KanishaSharma11/Chemical-Equipment-Parameter-Visualizer/tree/main.git
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
GEMINI_API= API_KEY
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

---

## 🧪 Testing with Sample Data

### 📊 Sample Dataset Included

We've included `sample_equipment_data.csv` with realistic chemical equipment parameters:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
Valve-1,Valve,60,4.1,105
...
```


## 👨‍💻 Authors

**Kanisha Ravindra Sharma** - *Initial work* - [GitHub Profile](https://github.com/KanishaSharma11)

---

## 🙏 Acknowledgments

- Chart.js for beautiful web visualizations
- Matplotlib for powerful desktop plotting
- Django REST Framework for robust API development

---


<div align="center">

### ⭐ Star this repository if you find it helpful!

**Made with ❤️ and ☕ for the chemical engineering community**

</div>
