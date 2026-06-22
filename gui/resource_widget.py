# ============================================
# File: gui/resource_widget.py
# ============================================
# Widget to display a single resource (CPU/RAM)
# ============================================

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ResourceWidget(QWidget):
    """Widget that displays a single resource with progress bar and details"""
    
    def __init__(self, name, unit, color):
        super().__init__()
        self.name = name
        self.unit = unit
        self.color = color
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI elements"""
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        # Header with name and value
        header_layout = QHBoxLayout()
        self.name_label = QLabel(self.name)
        self.name_label.setFont(QFont("Arial", 10, QFont.Bold))
        header_layout.addWidget(self.name_label)
        
        self.value_label = QLabel("0%")
        self.value_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.value_label.setAlignment(Qt.AlignRight)
        header_layout.addWidget(self.value_label)
        layout.addLayout(header_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #ccc;
                border-radius: 5px;
                text-align: center;
                height: 20px;
            }}
            QProgressBar::chunk {{
                background-color: {self.color};
                border-radius: 5px;
            }}
        """)
        layout.addWidget(self.progress_bar)
        
        # Details label
        self.details_label = QLabel("Total: 0 MB | Used: 0 MB")
        self.details_label.setStyleSheet("color: #555; font-size: 9px;")
        self.details_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.details_label)
        
        self.setLayout(layout)
        
    def update_data(self, data):
        """Update the widget with new data"""
        if self.name == "CPU Usage":
            # For CPU
            percentage = data.get('percent', 0)
            self.value_label.setText(f"{percentage:.1f}%")
            self.progress_bar.setValue(int(percentage))
            self.details_label.setText(f"Cores: {data.get('cores', 1)} | Load: {data.get('load_avg', 'N/A')}")
        else:
            # For RAM
            used = data.get('used', 0)
            total = data.get('total', 1)
            percentage = (used / total * 100) if total > 0 else 0
            
            self.value_label.setText(f"{percentage:.1f}%")
            self.progress_bar.setValue(int(percentage))
            
            # Format sizes for readability
            used_gb = used / 1024
            total_gb = total / 1024
            if used_gb > 1024:
                self.details_label.setText(f"Total: {total_gb/1024:.2f} GB | Used: {used_gb/1024:.2f} GB")
            else:
                self.details_label.setText(f"Total: {total_gb:.1f} GB | Used: {used_gb:.1f} GB")
