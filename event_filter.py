# event_filter.py


# Lista med händelsetyper
desired_event_types = [
    "Alla",
    "Alkohollagen",
    "Anträffad död",
    "Anträffat gods",
    "Arbetsplatsolycka",
    "Bedrägeri",
    "Bombhot",
    "Brand",
    "Brand automatlarm",
    "Bråk",
    "Detonation",
    "Djur skadat/omhändertaget",
    "Ekobrott",
    "Farligt föremål, misstänkt",
    "Fjällräddning",
    "Fylleri/LOB",
    "Förfalskningsbrott",
    "Försvunnen person",
    "Gränskontroll",
    "Häleri",
    "Inbrott",
    "Inbrott, försök",
    "Knivlagen",
    "Kontroll person/fordon",
    "Lagen om hundar och katter",
    "Larm inbrott",
    "Larm överfall",
    "Miljöbrott",
    "Missbruk av urkund",
    "Misshandel",
    "Misshandel, grov",
    "Mord/dråp",
    "Mord/dråp, försök",
    "Motorfordon, anträffat stulet",
    "Motorfordon, stöld",
    "Narkotikabrott",
    "Naturkatastrof",
    "Ofog barn/ungdom",
    "Ofredande/förargelse",
    "Olaga frihetsberövande",
    "Olaga hot",
    "Olaga intrång/hemfridsbrott",
    "Olovlig körning",
    "Ordningslagen",
    "Polisinsats/kommendering",
    "Rattfylleri",
    "Rån",
    "Rån väpnat",
    "Rån övrigt",
    "Rån, försök",
    "Räddningsinsats",
    "Sammanfattning dag",
    "Sammanfattning dygn",
    "Sammanfattning eftermiddag",
    "Sammanfattning förmiddag",
    "Sammanfattning helg",
    "Sammanfattning kväll",
    "Sammanfattning kväll och natt",
    "Sammanfattning natt",
    "Sammanfattning vecka",
    "Sedlighetsbrott",
    "Sjukdom/olycksfall",
    "Sjölagen",
    "Skadegörelse",
    "Skottlossning",
    "Skottlossning, misstänkt",
    "Spridning smittsamma kemikalier",
    "Stöld",
    "Stöld, försök",
    "Stöld, ringa",
    "Stöld/inbrott",
    "Tillfälligt obemannat",
    "Trafikbrott",
    "Trafikhinder",
    "Trafikkontroll",
    "Trafikolycka",
    "Trafikolycka, personskada",
    "Trafikolycka, singel",
    "Trafikolycka, smitning från",
    "Trafikolycka, vilt",
    "Uppdatering",
    "Utlänningslagen",
    "Vapenlagen",
    "Varningslarm/haveri",
    "Våld/hot mot tjänsteman",
    "Våldtäkt",
    "Våldtäkt, försök",
    "Vållande till kroppsskada",
]

def filterData(data, selected_parameter):
    if selected_parameter == "Alla":
        return data  # Visa alla händelser
    elif selected_parameter in desired_event_types:
        return [event for event in data if event.get('type', 'N/A') == selected_parameter]
    else:
        return []

def updateEventTypeComboBox(data, filterComboBox):
    # Skapa en tom lista för att lagra unika händelsetyper
    event_types = []

    # Loopa igenom JSON-data och extrahera händelsetyperna
    for event in data:
        event_type = event.get('type', 'N/A')
        if event_type not in event_types:
            event_types.append(event_type)

    # Sortera händelsetyperna i bokstavsordning
    event_types.sort()

    # Lägg till de önskade händelsetyperna i listan
    event_types.extend(desired_event_types)

    # Ta bort dubletter (om de finns)
    event_types = list(set(event_types))

    # Sortera listan igen
    event_types.sort()

    # Rensa ComboBox och lägg till händelsetyperna
    filterComboBox.clear()
    filterComboBox.addItems(event_types)  # Lägg till händelsetyperna
