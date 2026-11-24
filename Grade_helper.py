import sys
import os

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices, QColor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QSpinBox, QLabel,
    QHeaderView, QAbstractItemView, QFileDialog, QLineEdit, QMessageBox,
)

from About import AboutWindow


class GradeHelperWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''

        self.about_window = None

        self.setWindowTitle("Grade Helper")
        self.resize(720, 760)

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        title = QLabel("Grade Helper")
        title.setObjectName("title")
        layout.addWidget(title)

        # --- בחירת קובץ ---
        file_row = QHBoxLayout()
        self.file_label = QLabel("No file selected")
        self.file_label.setObjectName("file_label")
        self.btn_open = QPushButton("Open File...")
        self.btn_open.setCursor(Qt.PointingHandCursor)
        self.btn_open.clicked.connect(self.load_file)
        file_row.addWidget(self.file_label, 1)
        file_row.addWidget(self.btn_open)
        layout.addLayout(file_row)

        # --- טבלה: 50 שורות, 3 עמודות ---
        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Original Grades", "Corrected Grades"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table, 1)

        #  בונוס (ENTER)
        bonus_row = QHBoxLayout()
        bonus_row.addWidget(QLabel("Bonus points (press ENTER):"))
        self.spin_bonus = QSpinBox()
        self.spin_bonus.setRange(0, 100)
        self.spin_bonus.lineEdit().returnPressed.connect(self.apply_bonus)
        bonus_row.addWidget(self.spin_bonus)
        bonus_row.addStretch()
        layout.addLayout(bonus_row)

        # BONUS: add points to a single student by ID
        id_row = QHBoxLayout()
        id_row.addWidget(QLabel("Student ID:"))
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Type an ID or click a row")
        self.id_input.returnPressed.connect(self.apply_bonus_by_id)
        id_row.addWidget(self.id_input, 1)
        id_row.addWidget(QLabel("Points:"))
        self.spin_id_bonus = QSpinBox()
        self.spin_id_bonus.setRange(0, 100)
        id_row.addWidget(self.spin_id_bonus)
        self.btn_id_bonus = QPushButton("Add to Student")
        self.btn_id_bonus.setCursor(Qt.PointingHandCursor)
        self.btn_id_bonus.clicked.connect(self.apply_bonus_by_id)
        id_row.addWidget(self.btn_id_bonus)
        layout.addLayout(id_row)
        self.table.cellClicked.connect(self.fill_id_from_row)

        #  כפתורים תחתונים 
        bottom_row = QHBoxLayout()
        self.btn_update = QPushButton("Update File")
        self.btn_update.setObjectName("btn_primary")
        self.btn_update.setCursor(Qt.PointingHandCursor)
        self.btn_update.clicked.connect(self.update_file)
        self.btn_about = QPushButton("About")
        self.btn_about.setCursor(Qt.PointingHandCursor)
        self.btn_about.clicked.connect(self.show_about)
        bottom_row.addWidget(self.btn_update, 1)
        bottom_row.addWidget(self.btn_about)
        layout.addLayout(bottom_row)

   
    def load_file(self):
        self.selected_file, _ = QFileDialog.getOpenFileName(
            self, "Select grades file", "", "CSV files (*.csv)")
        if not self.selected_file:
            return
        self.file_label.setText(self.selected_file)
        self.student_ids.clear()
        self.original_grades.clear()
        self.corrected_grades.clear()

        with open(self.selected_file, 'r') as f:
            self.header = f.readline()
            for line in f:
                student_id, grade = line.strip().split(',')
                self.student_ids.append(int(student_id))
                self.original_grades.append(int(grade))
                self.corrected_grades.append(int(grade))

        self.update_table()

    def update_table(self):
       
        self.table.clearContents()
        for row in range(len(self.student_ids)):
            self.table.setItem(row, 0, QTableWidgetItem(str(self.student_ids[row])))
            self.table.setItem(row, 1, QTableWidgetItem(str(self.original_grades[row])))
            self.table.setItem(row, 2, QTableWidgetItem(str(self.corrected_grades[row])))
            # BONUS: green background for grades that received a bonus
            if self.corrected_grades[row] != self.original_grades[row]:
                self.table.item(row, 2).setBackground(QColor("#bbf7d0"))

    def apply_bonus(self):
        Bonus = self.spin_bonus.value()
        for i in range(len(self.original_grades)):
            new_grade = self.original_grades[i] + Bonus
            self.corrected_grades[i] = min(new_grade, 100)
        self.update_table()

    def fill_id_from_row(self, row, col):
        # BONUS: clicking a row copies its ID into the ID box
        if row < len(self.student_ids):
            self.id_input.setText(str(self.student_ids[row]))

    def apply_bonus_by_id(self):
        # BONUS: add points to one student, on top of the current corrected grade
        text = self.id_input.text().strip()
        if not text.isdigit() or int(text) not in self.student_ids:
            QMessageBox.warning(self, "Student not found", f"No student with ID '{text}'")
            return
        i = self.student_ids.index(int(text))
        self.corrected_grades[i] = min(self.corrected_grades[i] + self.spin_id_bonus.value(), 100)
        self.update_table()
        self.table.selectRow(i)

    def update_file(self):
        if not self.selected_file:
            return
        with open(self.selected_file, 'w') as f:
            f.write(self.header)
            for i in range(len(self.student_ids)):
                f.write(f'{self.student_ids[i]},{self.corrected_grades[i]}\n')

        QDesktopServices.openUrl(QUrl.fromLocalFile(self.selected_file))                         

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
    window = GradeHelperWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()