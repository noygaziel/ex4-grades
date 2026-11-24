import sys
import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog,
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
import numpy as np

from About import AboutWindow


class IceCreamWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # שתי רשימות הנתונים
        self.temperature = []
        self.revenue = []
        self.selected_file = ''

        self.about_window = None

        self.setWindowTitle("Ice Cream Revenue")
        self.resize(900, 680)

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        title = QLabel("Ice Cream Revenue vs. Temperature")
        title.setObjectName("title")
        layout.addWidget(title)

        # --- בחירת קובץ ---
        file_row = QHBoxLayout()
        self.file_label = QLabel("No file selected")
        self.file_label.setObjectName("file_label")
        self.btn_open = QPushButton("Select File...")
        self.btn_open.setCursor(Qt.PointingHandCursor)
        self.btn_open.clicked.connect(self.load_file)
        file_row.addWidget(self.file_label, 1)
        file_row.addWidget(self.btn_open)
        layout.addLayout(file_row)

        # --- גרף matplotlib + סרגל כלים (זום, הזזה, שמירה כקובץ) ---
        self.figure = Figure(figsize=(8, 5))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas, 1)

        # --- כפתורים תחתונים ---
        bottom_row = QHBoxLayout()
        bottom_row.addStretch()
        self.btn_about = QPushButton("About")
        self.btn_about.setCursor(Qt.PointingHandCursor)
        self.btn_about.clicked.connect(self.show_about)
        bottom_row.addWidget(self.btn_about)
        layout.addLayout(bottom_row)

        self.plot_graph()

    # ---------------------------------------------------------------
    def load_file(self):
        print("load_file")                  # זמני – שלב 2

    def plot_graph(self):
        # זמני – גרף לדוגמה. בשלב 3 תחליף אותו בציור האמיתי
        self.ax.clear()
        self.ax.plot([0, 1, 2, 3], [0, 1, 4, 9])
        self.ax.set_title("Temporary graph")
        self.canvas.draw()

    def show_about(self):
        self.about_window = AboutWindow()
        self.about_window.show()


def load_stylesheet(app):
    qss_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())


def main():
    app = QApplication(sys.argv)
    load_stylesheet(app)
    window = IceCreamWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()