import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
from datetime import datetime
import pandas as pd
import numpy as np
import statsmodels.api as sm
import time
import os

# Funktion för att konvertera datetime till sträng i ISO 8601-format
def datetime_to_str(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

# Funktion för att plotta tidsserien och initiala estimeringar
def plot_time_series(ax, time_in_seconds, events, predicted_events, initial_estimations):
    ax.plot(time_in_seconds, events, label='Tidsserie')
    ax.plot(time_in_seconds, predicted_events, label='Linjär Regression')

    ax.set_xlabel('Tid (sekunder sedan start)')
    ax.set_ylabel('Händelser')
    ax.set_title(f'Tidsserie och Linjär Regression för {event_type}')
    ax.legend()

# Funktion för att skapa initiala estimeringar för händelsetypen
def create_initial_estimations(data):
    estimations = {}
    # Filtrera data för den specifika händelsetypen
    filtered_data = [event for event in data if event['type'] == event_type]

    # Lägg till utskrifter för felsökning
    print(f'Antal händelser av typ {event_type}: {len(filtered_data)}')

    # Skapa tidsserier för händelsetypen
    time_series = [datetime.strptime(event['datetime'], '%Y-%m-%d %H:%M:%S %z') for event in filtered_data]
    # Konvertera tidsserier till strängar i ISO 8601-format
    time_series_str = [datetime_to_str(ts) for ts in time_series]
    # Skapa en array med tidpunkter som integer i sekunder sedan epoken (epoch)
    time_in_seconds = [(ts - time_series[0]).total_seconds() for ts in time_series]
    # Skapa en array för händelserna med y-axeln börjande från noll
    events = np.arange(len(time_series))
    # Skapa en linjär regressionsmodell
    model = sm.OLS(events, sm.add_constant(time_in_seconds))
    # Anpassa modellen till tidsserien
    results = model.fit()
    # Prediktioner från modellen för framtida händelser
    predicted_events = results.predict(sm.add_constant(time_in_seconds))
    # Lagra initiala estimeringar för händelsetypen
    estimations[event_type] = {
        'Initial_Time_Series': time_series_str,
        'Initial_Predicted_Events': predicted_events.tolist()
    }
    return estimations

# Funktion för att spara en beräkning eller estimering i loggfilen
def save_to_log(data, filename):
    try:
        if not os.path.exists(filename):
            print(f'Fil {filename} existerar inte. Skapar filen...')
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump([data], f, default=datetime_to_str, ensure_ascii=False, indent=4)
            print(f'Fil {filename} skapad.')
        else:
            with open(filename, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
            log_data.append(data)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, default=datetime_to_str, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Fel vid sparande till loggfil: {str(e)}")

# Här börjar uppdateringskoden med timesleep
def update_and_estimate_periodically(interval_minutes):
    log_filename = 'estimations_log.json'  # Ange filnamnet för loggfilen
    while True:
        # Uppdatera JSON-filen med ny data
        update_json_file()  # Implementera din kod för uppdatering

        # Läs in data från JSON-filen
        with open('C:\\Users\\KL\\PycharmProjects\\periodic_api_scrape\\all_police_events.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Skapa initiala estimeringar för händelsetypen
        initial_estimations = create_initial_estimations(data)

        # Läs in tidigare estimeringar från loggfilen om den finns
        previous_estimations = load_from_log(log_filename)

        # Kombinera de initiala estimeringarna med tidigare estimeringar om de finns
        if previous_estimations is not None:
            combined_estimations = {event_type: {**initial_estimations[event_type], **previous_estimations[event_type]}}
        else:
            combined_estimations = initial_estimations

        # Skapa ett Tkinter-fönster
        root = tk.Tk()
        root.title(f'Tidsserie och Linjär Regression för {event_type}')

        # Skapa en Matplotlib-figur
        fig = Figure(figsize=(12, 6))
        ax = fig.add_subplot(111)

        # Hämta tidsseriedata
        time_series = initial_estimations[event_type]['Initial_Time_Series']
        predicted_events = initial_estimations[event_type]['Initial_Predicted_Events']
        time_in_seconds = [(ts - time_series[0]).total_seconds() for ts in time_series]
        events = np.arange(len(time_series))

        # Plotta tidsserien med den hämtade datan och inkludera initial_estimations
        plot_time_series(ax, time_in_seconds, events, predicted_events, initial_estimations)

        # Skapa en Matplotlib Canvas för att bädda in figuren i Tkinter-fönstret
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().pack()

        # Starta Tkinter-loopen
        root.mainloop()

        # Spara de kombinerade estimeringarna i loggfilen
        save_to_log(combined_estimations, log_filename)

        # Sov i intervallet innan nästa uppdatering
        time.sleep(interval_minutes * 60)

# Funktion för att uppdatera JSON-filen med ny data
def update_json_file():
    # Implementera din kod för att hämta och uppdatera JSON-filen här
    # Exempel: Läs in data från en annan källa och spara den i JSON-filen
    new_data = fetch_data_from_source()  # Implementera din funktion för att hämta data
    with open('C:\\Users\\KL\\PycharmProjects\\periodic_api_scrape\\all_police_events.json', 'w', encoding='utf-8') as f:
        json.dump(new_data, f, default=datetime_to_str, ensure_ascii=False, indent=4)
    return new_data


root = tk.Tk()
root.mainloop()