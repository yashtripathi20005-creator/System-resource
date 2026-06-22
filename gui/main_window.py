# ============================================
# File: gui/main_window.py
# ============================================
# Main window containing the resource monitor UI
# ============================================

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, 
                             QSystemTrayIcon, QMenu, QAction, QStyle)
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QIcon, QFont
from .resource_widget import ResourceWidget
from .system_tray import SystemTrayIcon
from core.resource_collector import ResourceCollector

class MainWindow(QMainWindow):
    """Main application window with system resource monitoring"""
    
    def __init__(self):
        super().__init__()
        self.collector = ResourceCollector()
        self.tray_icon = None
        self.init_ui()
        self.setup_tray()
        self.setup_timer()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("System Resource Monitor")
        self.setGeometry(100, 100, 400, 300)
        self.setMinimumSize(350, 250)
        
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("📊 System Resource Monitor")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Resource widgets
        self.cpu_widget = ResourceWidget("CPU Usage", "%", "#4CAF50")
        self.ram_widget = ResourceWidget("RAM Usage", "MB", "#2196F3")
        layout.addWidget(self.cpu_widget)
        layout.addWidget(self.ram_widget)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_stop_btn = QPushButton("⏸ Pause")
        self.start_stop_btn.clicked.connect(self.toggle_monitoring)
        button_layout.addWidget(self.start_stop_btn)
        
        refresh_btn = QPushButton("🔄 Refresh Now")
        refresh_btn.clicked.connect(self.update_data)
        button_layout.addWidget(refresh_btn)
        
        layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("Status: Monitoring...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #666; font-size: 10px;")
        layout.addWidget(self.status_label)
        
    def setup_tray(self):
        """Setup system tray icon"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = SystemTrayIcon(self)
            self.tray_icon.show()
            
    def setup_timer(self):
        """Setup timer for periodic updates"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Update every second
        self.is_monitoring = True
        
    def update_data(self):
        """Update resource data from collector"""
        try:
            cpu_data = self.collector.get_cpu_usage()
            ram_data = self.collector.get_ram_usage()
            
            self.cpu_widget.update_data(cpu_data)
            self.ram_widget.update_data(ram_data)
            
            # Update tray tooltip
            if self.tray_icon:
                self.tray_icon.update_tooltip(cpu_data, ram_data)
                
            self.status_label.setText(f"Status: Monitoring... (Updated: {cpu_data['timestamp']})")
            
        except Exception as e:
            self.status_label.setText(f"❌ Error: {str(e)}")
            
    def toggle_monitoring(self):
        """Toggle monitoring on/off"""
        if self.is_monitoring:
            self.timer.stop()
            self.start_stop_btn.setText("▶ Resume")
            self.status_label.setText("Status: ⏸ Paused")
            self.is_monitoring = False
        else:
            self.timer.start(1000)
            self.start_stop_btn.setText("⏸ Pause")
            self.status_label.setText("Status: Monitoring...")
            self.is_monitoring = True
            self.update_data()
            
    def closeEvent(self, event):
        """Handle window close event"""
        if self.tray_icon:
            self.tray_icon.hide()
        event.accept()
