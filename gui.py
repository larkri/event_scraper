# gui.py

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit, QComboBox
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl
import sys
import json
import os
import datetime
from event_filter import updateEventTypeComboBox
from logger import log_exception

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
        # Hämta den valda parametern från ComboBox
        selected_parameter = self.filterComboBox.currentText()

        # Använd filtreringsfunktionen från filter.py för att filtrera datan
        self.filtered_data = filterData(self.data, selected_parameter)

        # Uppdatera kartan med de filtrerade händelserna
        self.sendFilteredDataToMap()

    def loadJSON(self):
        try:
            options = QFileDialog.Options()
            filePath, _ = QFileDialog.getOpenFileName(self, "Load JSON file", "", "JSON Files (*.json)", options=options)
            if filePath:
                with open(filePath, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                    event_count = len(self.data)
                    self.label.setText(f"Loaded {event_count} events from the JSON file.")

                    # Uppdatera informationsetiketten om filen
                    last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(filePath)).strftime(
                        '%Y-%m-%d %H:%M:%S')
                    self.fileInfoLabel.setText(f"File: {filePath}\nEvents: {event_count}\nLast Updated: {last_modified}")

                    # Visa de senaste 10 händelserna i QTextEdit
                    last_10_events = self.data[-10:]
                    event_text = ""
                    for event in last_10_events:
                        event_text += f"ID: {event.get('id', 'N/A')}, Type: {event.get('type', 'N/A')}, Location: {event.get('location', 'N/A')}\n"
                    self.eventTextEdit.setText(event_text)

                    # I slutet av loadJSON
                    self.sendLast10EventsToMap()

        except Exception as e:
            # Anropa log_exception för att logga undantaget
            log_exception(e)

    def sendLast10EventsToMap(self):
        last_10_events = self.data[-10:]
        self.browser.page().runJavaScript(f"updateMap({json.dumps(last_10_events)})")

    def sendFilteredDataToMap(self):
        # Kontrollera om det finns någon filtrerad data
        if self.filtered_data:
            # Skapa en JavaScript-kod för att skicka den filtrerade datan till kartan
            js_code = f"updateMap({json.dumps(self.filtered_data)})"
            # Använd runJavaScript-metoden för att köra JavaScript-koden på webbsidan
            self.browser.page().runJavaScript(js_code)
        else:
            # Om det inte finns någon filtrerad data, rensa kartan genom att skicka en tom lista
            js_code = "clearMap()"
            self.browser.page().runJavaScript(js_code)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())