# ============================================
# File: gui/system_tray.py
# ============================================
# System tray icon with menu
# ============================================

from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class SystemTrayIcon(QSystemTrayIcon):
    """System tray icon for the application"""
    
    def __init__(self, parent=None):
        # Create a simple icon (you can replace with actual icon file)
        icon = QIcon.fromTheme("system-monitor")
        if icon.isNull():
            # Fallback - create a simple colored icon programmatically
            from PyQt5.QtGui import QPixmap, QPainter, QColor
            pixmap = QPixmap(64, 64)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            painter.setBrush(QColor(33, 150, 243))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(8, 8, 48, 48)
            painter.setBrush(QColor(255, 255, 255))
            painter.drawEllipse(24, 24, 16, 16)
            painter.end()
            icon = QIcon(pixmap)
            
        super().__init__(icon, parent)
        self.parent = parent
        self.setToolTip("System Resource Monitor")
        
        # Create context menu
        self.menu = QMenu()
        
        show_action = QAction("Show Window", self)
        show_action.triggered.connect(self.show_window)
        self.menu.addAction(show_action)
        
        self.menu.addSeparator()
        
        pause_action = QAction("Pause/Resume", self)
        pause_action.triggered.connect(self.toggle_monitoring)
        self.menu.addAction(pause_action)
        
        self.menu.addSeparator()
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_application)
        self.menu.addAction(quit_action)
        
        self.setContextMenu(self.menu)
        
        # Connect activation signal
        self.activated.connect(self.on_activated)
        
    def show_window(self):
        """Show the main window"""
        if self.parent:
            self.parent.show()
            self.parent.raise_()
            self.parent.activateWindow()
            
    def toggle_monitoring(self):
        """Toggle monitoring state"""
        if self.parent:
            self.parent.toggle_monitoring()
            
    def quit_application(self):
        """Quit the application"""
        if self.parent:
            self.parent.close()
        from PyQt5.QtWidgets import QApplication
        QApplication.quit()
        
    def on_activated(self, reason):
        """Handle tray icon activation (click)"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window()
            
    def update_tooltip(self, cpu_data, ram_data):
        """Update the tooltip with current resource usage"""
        cpu_percent = cpu_data.get('percent', 0)
        ram_percent = (ram_data.get('used', 0) / max(ram_data.get('total', 1), 1)) * 100
        
        tooltip = f"System Resources\n"
        tooltip += f"CPU: {cpu_percent:.1f}%\n"
        tooltip += f"RAM: {ram_percent:.1f}%"
        self.setToolTip(tooltip)
