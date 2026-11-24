import webbrowser

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout

GITHUB_URL = "https://github.com/noygaziel/ex4-grades"   


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setFixedSize(360, 260)
        self.setStyleSheet("""
            QWidget { background-color: #0f172a; color: #e2e8f0; font-family: "Segoe UI"; }
            QLabel#name { font-size: 22px; font-weight: 700; color: #ffffff; }
            QPushButton { background-color: #2563eb; border: none; border-radius: 6px;
                          padding: 8px; color: white; font-weight: 600; }
            QPushButton:hover { background-color: #1d4ed8; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        name = QLabel("Noy Gaziel")                                       
        name.setObjectName("name")
        layout.addWidget(name)
        layout.addWidget(QLabel("Mechanical Engineering student, Afeka"))   
        layout.addWidget(QLabel("Grade Helper – Exercise 4"))

        link = QLabel(f'<a href="{GITHUB_URL}" style="color:#67e8f9;">GitHub repository</a>')
        link.setOpenExternalLinks(True)
        layout.addWidget(link)
        layout.addStretch()

        btn_github = QPushButton("Open GitHub")
        btn_github.setCursor(Qt.PointingHandCursor)
        btn_github.clicked.connect(self.open_github)
        layout.addWidget(btn_github)

    def open_github(self):
        webbrowser.open(GITHUB_URL)