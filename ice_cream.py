import sys
import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QLineEdit,
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
        self.slope = None
        self.intercept = None
        self.predicted_point = None

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

        
        file_row = QHBoxLayout()
        self.file_label = QLabel("No file selected")
        self.file_label.setObjectName("file_label")
        self.btn_open = QPushButton("Select File...")
        self.btn_open.setCursor(Qt.PointingHandCursor)
        self.btn_open.clicked.connect(self.load_file)
        file_row.addWidget(self.file_label, 1)
        file_row.addWidget(self.btn_open)
        layout.addLayout(file_row)

        #סרגל הכלים
        self.figure = Figure(figsize=(8, 5))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas, 1)

        # BONUS: zoom with the mouse wheel, double-click to reset the view
        self.canvas.mpl_connect("scroll_event", self.on_scroll_zoom)
        self.canvas.mpl_connect("button_press_event", self.on_double_click)

        # BONUS: predict revenue for a given temperature using the trend line
        predict_row = QHBoxLayout()
        predict_row.addWidget(QLabel("Predict revenue for temperature (°C):"))
        self.temp_input = QLineEdit()
        self.temp_input.setPlaceholderText("e.g. 30")
        self.temp_input.setFixedWidth(90)
        self.temp_input.returnPressed.connect(self.predict_revenue)
        predict_row.addWidget(self.temp_input)
        self.btn_predict = QPushButton("Predict")
        self.btn_predict.setCursor(Qt.PointingHandCursor)
        self.btn_predict.clicked.connect(self.predict_revenue)
        predict_row.addWidget(self.btn_predict)
        self.predict_label = QLabel("")
        self.predict_label.setObjectName("stats_label")
        predict_row.addWidget(self.predict_label, 1)
        layout.addLayout(predict_row)

        #  כפתורים תחתונים 
        bottom_row = QHBoxLayout()
        bottom_row.addStretch()
        self.btn_about = QPushButton("About")
        self.btn_about.setCursor(Qt.PointingHandCursor)
        self.btn_about.clicked.connect(self.show_about)
        bottom_row.addWidget(self.btn_about)
        layout.addLayout(bottom_row)

        self.plot_graph()



    def load_file(self):
        self.selected_file, _ = QFileDialog.getOpenFileName(
            self, "Select data file", "", "CSV files (*.csv)")
        if not self.selected_file:
            return
        self.file_label.setText(self.selected_file)
        self.temperature.clear()
        self.revenue.clear()
        self.predicted_point = None

        with open(self.selected_file, 'r') as f:
            f.readline()
            for line in f:
                temp, rev = line.strip().split(',')
                self.temperature.append(float(temp))
                self.revenue.append(float(rev))

        self.plot_graph()

    def plot_graph(self):
        self.ax.clear()
        self.ax.scatter(self.temperature, self.revenue, s=1)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set_title("Ice Cream Revenue vs. Temperature")
        self.ax.set_xlabel("Temperature (°C)")
        self.ax.set_ylabel("Revenue ($)")

        # קו מגמה ליניארי (np.polyfit)
        if len(self.temperature) >= 2:
            slope, intercept = np.polyfit(self.temperature, self.revenue, 1)
            self.slope, self.intercept = slope, intercept
            # BONUS: R² – how well the line fits the data (1 = perfect)
            predicted = slope * np.array(self.temperature) + intercept
            residual = np.sum((np.array(self.revenue) - predicted) ** 2)
            total = np.sum((np.array(self.revenue) - np.mean(self.revenue)) ** 2)
            r2 = 1 - residual / total
            x_line = np.linspace(min(self.temperature), max(self.temperature), 100)
            y_line = slope * x_line + intercept
            self.ax.plot(x_line, y_line, color='red', linewidth=1.5,
                         label=f"y = {slope:.2f}x + {intercept:.2f}   (R² = {r2:.3f})")
            self.ax.legend()
        if self.predicted_point is not None:
            px, py = self.predicted_point
            self.ax.scatter([px], [py], color='green', s=80, marker='*', zorder=5)
        self.figure.tight_layout()
        self.canvas.draw()
        self.initial_xlim = self.ax.get_xlim()
        self.initial_ylim = self.ax.get_ylim()

    def predict_revenue(self):
        # BONUS: uses the trend line y = slope*x + intercept
        if self.slope is None:
            self.predict_label.setText("Load a data file first")
            return
        try:
            temp = float(self.temp_input.text())
        except ValueError:
            self.predict_label.setText("Please enter a number")
            return
        revenue = self.slope * temp + self.intercept
        self.predict_label.setText(f"Expected revenue: ${revenue:.2f}")
        self.predicted_point = (temp, revenue)
        self.plot_graph()

    def on_scroll_zoom(self, event):
        # BONUS: zoom in/out around the mouse position
        if event.inaxes != self.ax:
            return
        factor = 0.8 if event.button == 'up' else 1.25
        x0, x1 = self.ax.get_xlim()
        y0, y1 = self.ax.get_ylim()
        x, y = event.xdata, event.ydata
        self.ax.set_xlim(x - (x - x0) * factor, x + (x1 - x) * factor)
        self.ax.set_ylim(y - (y - y0) * factor, y + (y1 - y) * factor)
        self.canvas.draw_idle()

    def on_double_click(self, event):
        # BONUS: double-click resets the zoom
        if event.dblclick and event.inaxes == self.ax:
            self.ax.set_xlim(self.initial_xlim)
            self.ax.set_ylim(self.initial_ylim)
            self.canvas.draw_idle()

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