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

        # Lägg till en ComboBox för filtreringsparameter
        self.filterComboBox = QComboBox()
        self.filterComboBox.currentIndexChanged.connect(self.filterData)
        layout.addWidget(self.filterComboBox)

        self.setLayout(layout)
        self.show()

        # Uppdatera ComboBox med händelsetyper från JSON-filen
        updateEventTypeComboBox(self.data, self.filterComboBox)

    def createLayout(self):
        layout = QVBoxLayout()

        # Label för att visa antalet laddade händelser
        self.label = QLabel("No events loaded yet")
        layout.addWidget(self.label)

        # Label för att visa filstatistik
        self.fileInfoLabel = QLabel("No file loaded.")
        layout.addWidget(self.fileInfoLabel)

        # Knapp för att ladda JSON-fil
        self.button = QPushButton('Load JSON File', self)
        self.button.clicked.connect(self.loadJSON)
        layout.addWidget(self.button)

        # WebEngineView för att visa kartan
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("file:///C:/Users/KL/PycharmProjects/event_scraper/map.html"))
        self.channel = QWebChannel()
        self.browser.page().setWebChannel(self.channel)
        layout.addWidget(self.browser)

        # Textredigerare för händelsedetaljer
        self.eventTextEdit = QTextEdit()
        self.eventTextEdit.setReadOnly(True)
        layout.addWidget(self.eventTextEdit)

        return layout

    def filterData(self):
        try:
            last_10_events = self.data[-10:]
            selected_parameter = self.filterComboBox.currentText()
            self.filtered_data = filterData(last_10_events, selected_parameter)
            self.sendFilteredDataToMap()
            self.updateEventTextEdit()
            log_info(f"Data filtered by {selected_parameter}.")
        except Exception as e:
            log_exception(e)

    def updateEventTextEdit(self):
        event_text = ""
        for event in self.filtered_data:
            event_text += f"ID: {event.get('id', 'N/A')}, Type: {event.get('type', 'N/A')}, Location: {event.get('location', 'N/A')}\n"
        self.eventTextEdit.setText(event_text if event_text else "Ingen matchning.")

    def loadJSON(self):
        try:
            options = QFileDialog.Options()
            filePath, _ = QFileDialog.getOpenFileName(self, "Load JSON file", "", "JSON Files (*.json)", options=options)
            if filePath:
                with open(filePath, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                    event_count = len(self.data)
                    self.label.setText(f"Loaded {event_count} events from the JSON file.")
                    last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(filePath)).strftime('%Y-%m-%d %H:%M:%S')
                    self.fileInfoLabel.setText(f"File: {filePath}\nEvents: {event_count}\nLast Updated: {last_modified}")
                    last_10_events = self.data[-10:]
                    event_text = ""
                    for event in last_10_events:
                        event_text += f"ID: {event.get('id', 'N/A')}, Type: {event.get('type', 'N/A')}, Location: {event.get('location', 'N/A')}\n"
                    self.eventTextEdit.setText(event_text)
                    self.sendLast10EventsToMap()
                    log_info(f"{event_count} events loaded from {filePath}.")
        except Exception as e:
            log_exception(e)

    def sendLast10EventsToMap(self):
        try:
            last_10_events = self.data[-10:]
            self.browser.page().runJavaScript(f"updateMap({json.dumps(last_10_events)})")
            log_info("Sent last 10 events to the map.")
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

event_filter.py

