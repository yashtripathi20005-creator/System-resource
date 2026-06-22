# ============================================
# File: resource_monitor.py
# ============================================
# Main application file - run this to start the monitor
# ============================================

import sys
import os
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    app.setApplicationName("System Resource Monitor")
    app.setOrganizationName("ResourceMonitor")
    
    # Set application icon (optional - you can add an icon file)
    # app.setWindowIcon(QIcon('icon.png'))
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
