import pandas as pd
import matplotlib.pyplot as plt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
    QFileDialog, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox,
    QColorDialog, QFontDialog, QHeaderView
)
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt


class FullscreenDataAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fullscreen Data Analysis Tool")
        self.setGeometry(100, 100, 1400, 900)

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Top Buttons for Menu Actions
        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        self.load_button = QPushButton("Load")
        self.load_button.clicked.connect(self.load_file)
        self.button_layout.addWidget(self.load_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_file)
        self.button_layout.addWidget(self.save_button)

        self.format_button = QPushButton("Format Cells")
        self.format_button.clicked.connect(self.format_cells)
        self.button_layout.addWidget(self.format_button)

        self.theme_button = QPushButton("Toggle Theme")
        self.theme_button.clicked.connect(self.toggle_theme)
        self.button_layout.addWidget(self.theme_button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.exit_button)

        # Label
        self.label = QLabel("Load a file to start", self)
        self.layout.addWidget(self.label)

        # Table Widget
        self.table_widget = QTableWidget()
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table_widget)

        # Visualization Controls
        self.visualization_layout = QHBoxLayout()
        self.layout.addLayout(self.visualization_layout)

        self.chart_type = QComboBox()
        self.chart_type.addItems(["Scatter Plot", "Bar Chart", "Pie Chart", "Histogram", "Line Chart"])
        self.visualization_layout.addWidget(self.chart_type)

        self.visualize_button = QPushButton("Visualize Data")
        self.visualize_button.clicked.connect(self.visualize_data)
        self.visualization_layout.addWidget(self.visualize_button)

        self.data = None
        self.is_dark_theme = False

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "All Files (*.xlsx *.csv *.txt);;Excel Files (*.xlsx);;CSV Files (*.csv);;Text Files (*.txt)"
        )
        if file_path:
            try:
                if file_path.endswith('.xlsx'):
                    self.data = pd.read_excel(file_path)
                elif file_path.endswith('.csv'):
                    self.data = pd.read_csv(file_path)
                elif file_path.endswith('.txt'):
                    self.data = pd.read_csv(file_path, delimiter='	')
                else:
                    raise ValueError("Unsupported file format")
                self.display_data()
                self.label.setText(f"File loaded successfully: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file: {e}")

    def save_file(self):
        if self.data is not None:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save File",
                "",
                "Excel Files (*.xlsx);;CSV Files (*.csv);;Text Files (*.txt)"
            )
            if file_path:
                try:
                    if file_path.endswith('.xlsx'):
                        self.data.to_excel(file_path, index=False)
                    elif file_path.endswith('.csv'):
                        self.data.to_csv(file_path, index=False)
                    elif file_path.endswith('.txt'):
                        self.data.to_csv(file_path, index=False, sep='	')
                    else:
                        raise ValueError("Unsupported file format")
                    QMessageBox.information(self, "Success", f"File saved successfully: {file_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save file: {e}")
        else:
            QMessageBox.warning(self, "Warning", "No data to save.")

    def display_data(self):
        if self.data is not None:
            self.table_widget.setRowCount(self.data.shape[0])
            self.table_widget.setColumnCount(self.data.shape[1])
            self.table_widget.setHorizontalHeaderLabels(self.data.columns)

            for i in range(self.data.shape[0]):
                for j in range(self.data.shape[1]):
                    self.table_widget.setItem(i, j, QTableWidgetItem(str(self.data.iat[i, j])))

    def visualize_data(self):
        if self.data is not None:
            numeric_columns = self.data.select_dtypes(include='number').columns
            if len(numeric_columns) >= 2:
                chart_type = self.chart_type.currentText()
                try:
                    if chart_type == "Scatter Plot":
                        plt.scatter(self.data[numeric_columns[0]], self.data[numeric_columns[1]])
                        plt.xlabel(numeric_columns[0])
                        plt.ylabel(numeric_columns[1])
                        plt.title("Scatter Plot")
                    elif chart_type == "Bar Chart":
                        self.data[numeric_columns[0]].value_counts().plot(kind="bar")
                        plt.title("Bar Chart")
                    elif chart_type == "Pie Chart":
                        self.data[numeric_columns[0]].value_counts().plot(kind="pie", autopct='%1.1f%%')
                        plt.title("Pie Chart")
                    elif chart_type == "Histogram":
                        self.data[numeric_columns[0]].plot(kind="hist", bins=10)
                        plt.title("Histogram")
                    elif chart_type == "Line Chart":
                        self.data[numeric_columns[0]].plot(kind="line")
                        plt.title("Line Chart")
                    plt.show()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to generate chart: {e}")
            else:
                QMessageBox.warning(self, "Warning", "Not enough numeric columns to plot.")
        else:
            QMessageBox.warning(self, "Warning", "No data loaded.")

    def format_cells(self):
        font, ok = QFontDialog.getFont(self)
        if ok:
            self.table_widget.setFont(font)
        color = QColorDialog.getColor()
        if color.isValid():
            self.table_widget.setStyleSheet(f"color: {color.name()};")

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        if self.is_dark_theme:
            self.setStyleSheet("background-color: #2e2e2e; color: white;")
        else:
            self.setStyleSheet("")


if __name__ == "__main__":
    app = QApplication([])
    window = FullscreenDataAnalysisApp()
    window.show()
    app.exec()
