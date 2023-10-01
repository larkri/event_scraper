from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit, QComboBox
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl
import sys
import json
import os
import datetime
from event_filter import updateEventTypeComboBox, filterData
from logger import log_info, log_exception
from collections import Counter

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 WebEngine'
        self.data = []  # För att hålla JSON-data
        self.filtered_data = []  # För att hålla filtrerad data
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        layout = self.createLayout()
        self.filterComboBox = QComboBox()
        self.filterComboBox.addItem("Alla")
        self.filterComboBox.currentIndexChanged.connect(self.filterData)
        layout.addWidget(self.filterComboBox)
        self.setLayout(layout)
        self.show()
        updateEventTypeComboBox(self.data, self.filterComboBox)

    def createLayout(self):
        layout = QVBoxLayout()
        self.label = QLabel("No events loaded yet")
        layout.addWidget(self.label)
        self.fileInfoLabel = QLabel("No file loaded.")
        layout.addWidget(self.fileInfoLabel)
        self.button = QPushButton('Load JSON File', self)
        self.button.clicked.connect(self.loadJSON)
        layout.addWidget(self.button)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("file:///C:/Users/KL/PycharmProjects/event_scraper/map.html"))
        self.channel = QWebChannel()
        self.browser.page().setWebChannel(self.channel)
        layout.addWidget(self.browser)
        self.eventTextEdit = QTextEdit()
        self.eventTextEdit.setReadOnly(True)
        layout.addWidget(self.eventTextEdit)
        return layout

    def generate_event_summary(self, events):
        event_types = [event.get('type', 'N/A') for event in events]
        event_count = Counter(event_types)
        summary = "Sammanfattning av händelser:\n"
        for event_type, count in event_count.items():
            summary += f"{event_type}: {count}\n"
        return summary

    def filterData(self):
        try:
            selected_parameter = self.filterComboBox.currentText()
            self.filtered_data = filterData(self.data, selected_parameter)
            if not self.filtered_data:
                self.eventTextEdit.setText(f"Inga matchningar för händelsetypen '{selected_parameter}'.")
                js_code = "clearMap()"
                self.browser.page().runJavaScript(js_code)
                log_info("Cleared the map.")
            else:
                self.sendFilteredDataToMap()
                self.updateEventTextEdit(selected_parameter)
                log_info(f"Data filtered by {selected_parameter}.")
        except Exception as e:
            log_exception(e)

    def updateEventTextEdit(self, selected_parameter):
        if selected_parameter == "Alla":
            summary = self.generate_event_summary(self.data)
            self.eventTextEdit.setText(summary)
        else:
            event_text = ""
            for event in self.filtered_data:
                event_text += f"ID: {event.get('id', 'N/A')}, Type: {event.get('type', 'N/A')}, Location: {event.get('location', 'N/A')}\n"
            self.eventTextEdit.setText(
                event_text if event_text else f"Inga matchningar för händelsetypen '{selected_parameter}'.")

    def loadJSON(self):
        try:
            options = QFileDialog.Options()
            filePath, _ = QFileDialog.getOpenFileName(self, "Load JSON file", "", "JSON Files (*.json)",
                                                      options=options)
            if filePath:
                with open(filePath, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                    event_count = len(self.data)
                    self.label.setText(f"Loaded {event_count} events from the JSON file.")
                    last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(filePath)).strftime(
                        '%Y-%m-%d %H:%M:%S')
                    self.fileInfoLabel.setText(
                        f"File: {filePath}\nEvents: {event_count}\nLast Updated: {last_modified}")
                    self.eventTextEdit.setText(self.generate_event_summary(self.data))
                    self.sendFilteredDataToMap()
                    log_info(f"{event_count} events loaded from {filePath}.")
        except Exception as e:
            log_exception(e)

    def sendFilteredDataToMap(self):
        try:
            if self.filtered_data:
                js_code = f"updateMap({json.dumps(self.filtered_data)})"
                self.browser.page().runJavaScript(js_code)
                log_info("Sent filtered data to the map.")
            else:
                js_code = "clearMap()"
                self.browser.page().runJavaScript(js_code)
                log_info("Cleared the map.")
        except Exception as e:
            log_exception(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())