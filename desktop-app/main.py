import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog,
    QLabel, QLineEdit, QHBoxLayout, QMessageBox, QListWidget, QDialog,
    QFrame, QGraphicsOpacityEffect, QScrollArea, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QPoint, QSize
from PyQt5.QtGui import QFont, QPalette, QColor, QLinearGradient, QPainter, QBrush, QPen
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

API_BASE = "http://127.0.0.1:8000/api"


# ================================================================
# ANIMATED BUTTON WITH HOVER EFFECTS
# ================================================================
class AnimatedButton(QPushButton):
    def __init__(self, text, icon=""):
        super().__init__(f"{icon}  {text}")
        self.setFixedHeight(55)
        self.setMinimumWidth(220)
        self.setCursor(Qt.PointingHandCursor)
        self.default_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 27px;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 35px;
                text-align: center;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #764ba2, stop:1 #667eea);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #5a4a8a, stop:1 #4a5fa0);
            }
            QPushButton:disabled {
                background: #cbd5e0;
                color: #a0aec0;
            }
        """
        self.setStyleSheet(self.default_style)
        
    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
        super().enterEvent(event)


# ================================================================
# STYLED INPUT FIELD
# ================================================================
class StyledLineEdit(QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(50)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #f7fafc;
                border: 2px solid #e2e8f0;
                border-radius: 25px;
                padding: 12px 25px;
                font-size: 15px;
                color: #2d3748;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
            }
        """)


# ================================================================
# HISTORY POPUP WINDOW
# ================================================================
class HistoryWindow(QDialog):
    def __init__(self, parent, auth):
        super().__init__(parent)
        self.setWindowTitle("📊 Upload History")
        self.setFixedSize(750, 600)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f7fafc, stop:1 #edf2f7);
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(25)
        
        # Title
        title = QLabel("📜 Recent Uploads")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2d3748;")
        layout.addWidget(title)

        subtitle = QLabel("Click on any item to load its visualization")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #718096;")
        layout.addWidget(subtitle)

        # List widget with styling
        self.list = QListWidget()
        self.list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 15px;
                padding: 15px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 18px;
                margin: 5px 0px;
                border-radius: 10px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:hover {
                background-color: #edf2f7;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
            }
        """)
        layout.addWidget(self.list)

        self.setLayout(layout)
        self.auth = auth
        self.parent = parent

        self.load_history()
        self.list.itemClicked.connect(self.open_history_item)

    def load_history(self):
        try:
            r = requests.get(f"{API_BASE}/history/", auth=self.auth)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not fetch history:\n{str(e)}")
            return

        if r.status_code != 200:
            QMessageBox.critical(self, "Error", "Failed to load history")
            return

        self.history = r.json()["history"]

        for item in self.history:
            self.list.addItem(f"📄  {item['original_filename']}\n     Uploaded: {item['uploaded_at']}")

    def open_history_item(self, item):
        index = self.list.currentRow()
        summary = self.history[index]["summary_json"]
        self.parent.draw_summary(summary)
        self.parent.show_success_message(f"✅ Loaded: {self.history[index]['original_filename']}")
        self.accept()


# ================================================================
# MAIN DESKTOP APPLICATION
# ================================================================
class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🧪 Chemical Equipment Visualizer")
        self.setMinimumSize(1400, 950)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fdfeff, stop:1 #f7fafc);
            }
        """)

        # Create a scroll area for the entire content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        # Container widget for scroll area
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(60, 40, 60, 40)
        main_layout.setSpacing(30)

        # ============ HEADER ============
        header_frame = QFrame()
        header_frame.setFixedHeight(140)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(102, 126, 234, 0.15), 
                    stop:1 rgba(118, 75, 162, 0.15));
                border-radius: 20px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(12)
        header_layout.setContentsMargins(30, 25, 30, 25)
        
        header = QLabel("🧪 Chemical Equipment Visualizer")
        header.setFont(QFont("Segoe UI", 32, QFont.Bold))
        header.setStyleSheet("color: #2d3748; background: transparent;")
        header.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(header)
        
        subheader = QLabel("Advanced Data Analytics & Visualization Platform")
        subheader.setFont(QFont("Segoe UI", 14))
        subheader.setStyleSheet("color: #718096; background: transparent;")
        subheader.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subheader)
        
        main_layout.addWidget(header_frame)

        # ============ LOGIN PANEL ============
        self.login_container = QWidget()
        
        login_outer_layout = QVBoxLayout(self.login_container)
        login_outer_layout.setContentsMargins(0, 40, 0, 40)
        login_outer_layout.setSpacing(0)
        
        # Horizontal centering
        h_center = QHBoxLayout()
        h_center.addStretch(1)
        
        # Login frame with fixed size
        self.login_frame = QFrame()
        self.login_frame.setFixedSize(650, 550)
        self.login_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 30px;
                border: 2px solid #e2e8f0;
            }
        """)
        
        # Login form layout
        login_form = QVBoxLayout(self.login_frame)
        login_form.setContentsMargins(60, 55, 60, 55)
        login_form.setSpacing(20)
        
        # Title
        login_title = QLabel("🔐 Secure Login")
        login_title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        login_title.setStyleSheet("color: #2d3748;")
        login_title.setAlignment(Qt.AlignCenter)
        login_form.addWidget(login_title)
        
        # Subtitle
        login_subtitle = QLabel("Enter your credentials to access the dashboard")
        login_subtitle.setFont(QFont("Segoe UI", 13))
        login_subtitle.setStyleSheet("color: #a0aec0;")
        login_subtitle.setAlignment(Qt.AlignCenter)
        login_subtitle.setWordWrap(True)
        login_form.addWidget(login_subtitle)
        
        login_form.addSpacing(25)
        
        # Username
        user_label = QLabel("Username")
        user_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        user_label.setStyleSheet("color: #4a5568;")
        login_form.addWidget(user_label)
        
        self.user = StyledLineEdit("Enter your username")
        login_form.addWidget(self.user)
        
        login_form.addSpacing(8)
        
        # Password
        pwd_label = QLabel("Password")
        pwd_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        pwd_label.setStyleSheet("color: #4a5568;")
        login_form.addWidget(pwd_label)
        
        self.pwd = StyledLineEdit("Enter your password")
        self.pwd.setEchoMode(QLineEdit.Password)
        login_form.addWidget(self.pwd)
        
        login_form.addSpacing(25)
        
        # Login button
        self.btnLogin = AnimatedButton("Sign In", "🔐")
        self.btnLogin.clicked.connect(self.login_user)
        login_form.addWidget(self.btnLogin)
        
        # Add some spacing at bottom
        login_form.addStretch()
        
        h_center.addWidget(self.login_frame)
        h_center.addStretch(1)
        
        login_outer_layout.addLayout(h_center)
        
        main_layout.addWidget(self.login_container)

        # ============ MAIN CONTROLS (Hidden initially) ============
        self.controls_frame = QFrame()
        self.controls_frame.setVisible(False)
        self.controls_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                border: 2px solid #e2e8f0;
            }
        """)
        
        controls_layout = QHBoxLayout(self.controls_frame)
        controls_layout.setSpacing(30)
        controls_layout.setContentsMargins(40, 22, 40, 22)
        
        controls_layout.addStretch()

        self.btnUpload = AnimatedButton("Upload CSV File", "📤")
        self.btnUpload.clicked.connect(self.upload_csv)
        controls_layout.addWidget(self.btnUpload)

        self.btnHistory = AnimatedButton("View History", "📜")
        self.btnHistory.clicked.connect(self.open_history)
        controls_layout.addWidget(self.btnHistory)
        
        controls_layout.addStretch()

        main_layout.addWidget(self.controls_frame)

        # ============ INFO LABEL ============
        self.info = QLabel("👋 Welcome! Please login to continue")
        self.info.setFont(QFont("Segoe UI", 15))
        self.info.setMinimumHeight(65)
        self.info.setStyleSheet("""
            color: #4a5568;
            padding: 20px 30px;
            background-color: #edf2f7;
            border-radius: 15px;
            border-left: 6px solid #667eea;
        """)
        self.info.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.info.setWordWrap(True)
        main_layout.addWidget(self.info)

        # ============ CHART AREA (Hidden during login) ============
        self.chart_container = QWidget()
        self.chart_container.setVisible(False)
        
        chart_container_layout = QVBoxLayout(self.chart_container)
        chart_container_layout.setContentsMargins(0, 0, 0, 0)
        chart_container_layout.setSpacing(0)
        
        chart_frame = QFrame()
        chart_frame.setMinimumHeight(550)
        chart_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 25px;
                border: 2px solid #e2e8f0;
            }
        """)
        
        chart_layout = QVBoxLayout(chart_frame)
        chart_layout.setContentsMargins(35, 32, 35, 32)
        chart_layout.setSpacing(20)
        
        chart_title = QLabel("📊 Data Visualization")
        chart_title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        chart_title.setStyleSheet("color: #2d3748;")
        chart_layout.addWidget(chart_title)
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(14, 6), facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(450)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        chart_layout.addWidget(self.canvas)
        
        chart_container_layout.addWidget(chart_frame)
        
        main_layout.addWidget(self.chart_container)

        # Add bottom spacing
        main_layout.addSpacing(40)

        # Set the container as scroll widget
        scroll.setWidget(container)
        
        # Main window layout
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(scroll)

        # Initialize with empty chart
        self.draw_empty_state()

    # ================================================================
    # LOGIN LOGIC
    # ================================================================
    def login_user(self):
        username = self.user.text().strip()
        password = self.pwd.text().strip()

        if not username or not password:
            self.show_error("Please enter both username and password")
            return

        self.btnLogin.setEnabled(False)
        self.btnLogin.setText("🔄  Authenticating...")

        try:
            r = requests.get(f"{API_BASE}/auth-check/", auth=(username, password))
        except Exception as e:
            self.show_error("Server unreachable. Please check your connection.")
            self.btnLogin.setEnabled(True)
            self.btnLogin.setText("🔐  Sign In")
            return

        if r.status_code == 200:
            self.show_success_message("✅ Login successful! Welcome to the dashboard")
            self.animate_login_success()
        else:
            self.show_error("❌ Invalid credentials. Please try again.")
            self.btnLogin.setEnabled(True)
            self.btnLogin.setText("🔐  Sign In")

    def animate_login_success(self):
        """Hide login and show main dashboard with animation"""
        # First hide login container with fade
        self.fade_out_login()
        
        # After fade completes, show controls and chart
        QTimer.singleShot(350, self.show_dashboard)

    def fade_out_login(self):
        """Fade out the login container"""
        effect = QGraphicsOpacityEffect()
        self.login_container.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(300)
        anim.setStartValue(1)
        anim.setEndValue(0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.finished.connect(lambda: self.login_container.setVisible(False))
        anim.start()
        # Keep reference to prevent garbage collection
        self._login_fade_anim = anim

    def show_dashboard(self):
        """Show the main dashboard controls and chart"""
        # Make controls visible
        self.controls_frame.setVisible(True)
        self.chart_container.setVisible(True)
        
        # Animate them in
        self.fade_in(self.controls_frame)
        QTimer.singleShot(150, lambda: self.fade_in(self.chart_container))

    # ================================================================
    # UPLOAD CSV
    # ================================================================
    def upload_csv(self):
        path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select CSV File", 
            "", 
            "CSV Files (*.csv);;All Files (*)"
        )
        if not path:
            return

        self.info.setText("⏳ Uploading file, please wait...")
        self.info.setStyleSheet("""
            color: #3182ce;
            padding: 20px 30px;
            background-color: #ebf8ff;
            border-radius: 15px;
            border-left: 6px solid #3182ce;
        """)
        QApplication.processEvents()

        try:
            with open(path, "rb") as f:
                files = {"file": (path.split("/")[-1], f, "text/csv")}
                response = requests.post(
                    f"{API_BASE}/upload-csv/",
                    files=files,
                    auth=(self.user.text(), self.pwd.text())
                )
        except Exception as e:
            self.show_error(f"Upload failed: {str(e)}")
            return

        if response.status_code != 201:
            self.show_error(f"Upload failed: {response.text}")
            return

        data = response.json()
        summary = data["upload"]["summary_json"]
        filename = data["upload"]["original_filename"]

        self.show_success_message(f"✅ Successfully uploaded: {filename}")
        self.draw_summary(summary)

    # ================================================================
    # OPEN HISTORY POPUP
    # ================================================================
    def open_history(self):
        historyWindow = HistoryWindow(self, auth=(self.user.text(), self.pwd.text()))
        historyWindow.exec_()

    # ================================================================
    # DRAW CHARTS
    # ================================================================
    def draw_empty_state(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(
            0.5, 0.5, 
            '📊 No data to display\n\nUpload a CSV file to see beautiful visualizations',
            ha='center', va='center',
            fontsize=18, color='#a0aec0', fontweight='500',
            transform=ax.transAxes
        )
        ax.axis('off')
        self.figure.tight_layout(pad=2)
        self.canvas.draw()

    def draw_summary(self, summary):
        self.figure.clear()

        # Modern color palette
        colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b']

        # Create subplots with proper margins
        gs = self.figure.add_gridspec(1, 2, hspace=0.4, wspace=0.4, 
                                       left=0.08, right=0.96, top=0.88, bottom=0.15)
        
        # ---- BAR CHART: AVERAGES ----
        ax1 = self.figure.add_subplot(gs[0, 0])
        averages = summary.get("averages", {})
        keys = list(averages.keys())
        vals = [averages[k] or 0 for k in keys]

        if keys and vals:
            bars = ax1.bar(
                keys, vals, 
                color=colors[:len(keys)], 
                alpha=0.85, 
                edgecolor='white', 
                linewidth=3,
                width=0.65
            )
            
            # Add value labels
            for bar in bars:
                height = bar.get_height()
                ax1.text(
                    bar.get_x() + bar.get_width()/2., height * 1.03,
                    f'{height:.1f}',
                    ha='center', va='bottom',
                    fontsize=12, fontweight='bold',
                    color='#2d3748'
                )
            
            ax1.set_title(
                "Average Values by Type", 
                fontsize=17, 
                fontweight='bold', 
                color='#2d3748', 
                pad=20
            )
            ax1.set_ylabel("Value", fontsize=13, color='#4a5568', fontweight='600', labelpad=12)
            ax1.set_xlabel("Type", fontsize=13, color='#4a5568', fontweight='600', labelpad=12)
            ax1.set_xticklabels(keys, rotation=25, ha="right", fontsize=11)
            ax1.tick_params(axis='both', colors='#718096', labelsize=11)
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.spines['left'].set_color('#cbd5e0')
            ax1.spines['left'].set_linewidth(1.5)
            ax1.spines['bottom'].set_color('#cbd5e0')
            ax1.spines['bottom'].set_linewidth(1.5)
            ax1.grid(axis='y', alpha=0.25, linestyle='--', linewidth=1)
            ax1.set_facecolor('#fafafa')
            
            # Add padding
            y_max = max(vals) if vals else 1
            ax1.set_ylim(0, y_max * 1.25)
            
        else:
            ax1.text(
                0.5, 0.5, 'No average data available',
                ha='center', va='center',
                fontsize=14, color='#a0aec0', transform=ax1.transAxes
            )
            ax1.axis('off')

        # ---- PIE CHART: DISTRIBUTION ----
        ax2 = self.figure.add_subplot(gs[0, 1])
        dist = summary.get("type_distribution", {})
        labels = list(dist.keys())
        sizes = list(dist.values())

        if sizes:
            wedges, texts, autotexts = ax2.pie(
                sizes, 
                labels=labels, 
                autopct='%1.1f%%',
                colors=colors[:len(sizes)], 
                startangle=90,
                wedgeprops={
                    'edgecolor': 'white', 
                    'linewidth': 3.5,
                    'antialiased': True
                },
                textprops={'fontsize': 12, 'fontweight': '600'},
                pctdistance=0.85,
                labeldistance=1.15
            )
            
            for text in texts:
                text.set_fontsize(12)
                text.set_color('#2d3748')
                text.set_fontweight('bold')
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(12)
            
            ax2.set_title(
                "Equipment Type Distribution", 
                fontsize=17, 
                fontweight='bold', 
                color='#2d3748', 
                pad=20
            )
        else:
            ax2.text(
                0.5, 0.5, 
                'No distribution data available', 
                ha="center", 
                va="center",
                fontsize=14, 
                color='#a0aec0',
                transform=ax2.transAxes
            )
            ax2.axis('off')

        # Apply tight layout
        self.figure.tight_layout(pad=2.5)
        self.canvas.draw()

    # ================================================================
    # UI HELPERS
    # ================================================================
    def show_success_message(self, msg):
        self.info.setText(msg)
        self.info.setStyleSheet("""
            color: #2f855a;
            padding: 20px 30px;
            background-color: #f0fff4;
            border-radius: 15px;
            border-left: 6px solid #38a169;
        """)

    def show_error(self, msg):
        self.info.setText(f"❌ {msg}")
        self.info.setStyleSheet("""
            color: #c53030;
            padding: 20px 30px;
            background-color: #fff5f5;
            border-radius: 15px;
            border-left: 6px solid #e53e3e;
        """)

    def fade_out(self, widget):
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(300)
        anim.setStartValue(1)
        anim.setEndValue(0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.finished.connect(lambda: widget.setVisible(False))
        anim.start()
        # Keep reference to prevent garbage collection
        self._fade_out_anim = anim

    def fade_in(self, widget):
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(500)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.InCubic)
        anim.start()
        # Keep reference to prevent garbage collection
        if not hasattr(self, '_fade_in_anims'):
            self._fade_in_anims = []
        self._fade_in_anims.append(anim)


# ================================================================
# APP ENTRY POINT
# ================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    
    window = DesktopApp()
    window.show()
    sys.exit(app.exec_())
