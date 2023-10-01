from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage  # Fixat
from PyQt5.QtWebChannel import QWebChannel  # Fixat
from PyQt5.QtCore import QUrl
import sys
import json
import os
import datetime
from logger import log_exception

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 WebEngine'
        self.data = []  # To hold loaded JSON data
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setLayout(self.createLayout())
        self.show()

    def createLayout(self):
        layout = QVBoxLayout()

        # Label to show number of loaded events
        self.label = QLabel("No events loaded yet")
        layout.addWidget(self.label)

        # Label to show file statistics
        self.fileInfoLabel = QLabel("No file loaded.")
        layout.addWidget(self.fileInfoLabel)

        # Button to load JSON file
        self.button = QPushButton('Load JSON File', self)
        self.button.clicked.connect(self.loadJSON)
        layout.addWidget(self.button)

        # WebEngineView to display map
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("file:///C:/Users/KL/PycharmProjects/event_scraper/map.html"))
        # Efter self.browser = QWebEngineView() i createLayout
        self.channel = QWebChannel()
        self.browser.page().setWebChannel(self.channel)
        layout.addWidget(self.browser)

        # Text Edit for event details
        self.eventTextEdit = QTextEdit()
        self.eventTextEdit.setReadOnly(True)
        layout.addWidget(self.eventTextEdit)

        return layout

    def loadJSON(self):
        try:
            options = QFileDialog.Options()
            filePath, _ = QFileDialog.getOpenFileName(self, "Load JSON file", "", "JSON Files (*.json)", options=options)
            if filePath:
                with open(filePath, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                    event_count = len(self.data)
                    self.label.setText(f"Loaded {event_count} events from the JSON file.")

                    # Update file info label
                    last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(filePath)).strftime(
                        '%Y-%m-%d %H:%M:%S')
                    self.fileInfoLabel.setText(f"File: {filePath}\nEvents: {event_count}\nLast Updated: {last_modified}")

                    # Display last 10 events in the QTextEdit
                    last_10_events = self.data[-10:]
                    event_text = ""
                    for event in last_10_events:
                        event_text += f"ID: {event.get('id', 'N/A')}, Type: {event.get('type', 'N/A')}, Location: {event.get('location', 'N/A')}\n"
                    self.eventTextEdit.setText(event_text)

                    # i slutet av loadJSON
                    self.sendLast10EventsToMap()

        except Exception as e:
            # Anropa log_exception för att logga undantaget
            log_exception(e)

    def sendLast10EventsToMap(self):
        last_10_events = self.data[-10:]
        self.browser.page().runJavaScript(f"updateMap({json.dumps(last_10_events)})")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
