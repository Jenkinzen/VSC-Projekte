import rezeptliste_services as service
neustart = True

def eingabezahl_pruefen(prompt,min_value=None,max_value=None):
    while True:
        raw = input(prompt)
        try:
            value = int(raw)

        except ValueError:
            print("Bitte eine Zahl eingeben.")
            continue

        if min_value is not None and value < min_value:
            print("Die Nummer ist zu klein.")
            continue

        if max_value is not None and value > max_value:
            print("Die Nummer ist zu groß.")
            continue

        return value



def filter_auswaehlen():
    return eingabezahl_pruefen("Nach welchen Kriterien soll die\n"
                "Rezeptauswahl gefiltert werden?\n\n"
                 "1-[Gerichte]\n"
                 "2-[Zutaten]\n"
                 "3-[Gang]\n\n"
                 "0-[Zurück]:\n\n"
                 "Auswahl:", 
                 min_value=0,
                 max_value=3)


def rezepte_ansehen_nach_gang():
    while True:
        gang_map = {1: "vorspeise",2: "hauptspeise",3:"dessert"}
        gangeingabe = eingabezahl_pruefen("Welchen Gang möchten Sie wählen?\n\n"
        "1-[Vorspeise],\n"
        "2-[Hauptspeise]\n"
        "3-[Dessert]\n\n" 
        "0-[Zurück]:\n\n"
        "Auswahl:",
        min_value=0, 
        max_value=3)
        
        if gangeingabe == 0:
            return

        gangeingabe = gang_map[gangeingabe]

        
        

        rezepte = service.filter_rezepte_nach_gang(gangeingabe)
        print()
        for i, rezept in enumerate(rezepte, start=1):
            print(f"{i}. {rezept.name}")

        print()
        print("0-[Zurück]\n")
        while True:
            try:
                nummer = eingabezahl_pruefen("Nummer wählen:\n" 
                ,min_value=0,max_value=len(rezepte))

                if nummer == 0:
                    break

                rezept = service.rezept_nach_index(rezepte, nummer)

                if rezept is None:
                    print("Ungültige Nummer.")
                    continue

                for zeile in rezept.anzeigen():
                    print(zeile)

                break

            except ValueError:
                print("Bitte eine Zahl eingeben.")

def rezepte_ansehen_nach_zutaten():
    while True:
        zutat = [z.strip() for z in input("Welche Zutat(en) möchten Sie wählen?\nBitte Zutaten mit  \",\"  trennen.\n\n" 
        "0-[Zurück]\n").strip().lower().split(",")]

        if zutat == ["0"]:
            return
        
        rezepte = service.filter_rezepte_nach_zutaten(zutat)

        

        if not rezepte :
            print("Keine Rezepte gefunden.")
            continue    

        for i, rezept in enumerate(rezepte, start=1):
            print(f"{i}. {rezept.name}")

        while True:

            try:
                nummer = eingabezahl_pruefen("Nummer wählen:\n",min_value=0,max_value=len(rezepte))
                rezept = service.rezept_nach_index(rezepte, nummer)

                if rezept is None:
                    print("Ungültige Nummer.")
                    continue

                for zeile in rezept.anzeigen():
                    print(zeile)
                    #wenn hier break stehen würde bricht er print(zeile) 
                    #nach der ersten zeile ab ( also printet nur namen aber nicht zutaten,zubereitung etc.)
                break    

            except ValueError:
                print("Bitte eine Zahl eingeben.")  
                #hier brauch man kein continue weil die Schleife hier eh endet und dann wieder anfängt
            
def rezepte_ansehen_nach_Gericht():
    while True:
        print()
        for i, rezept in enumerate(service.alle_rezepte(), start=1):
            print(f"{i}. {rezept.name}")
        gerichte = service.filter_rezepte_nach_gericht("")
        nummer = eingabezahl_pruefen("\nWählen sie bitte die Nummer des Gerichtes,\n"
        "geben sie 0 ein um zurück zur Kriterienauswahl zu gelangen:\n",min_value=0,max_value=len(gerichte))

        if nummer == 0:
            return

        if nummer > len(gerichte):
            print("Falsche Zahl eingegeben!")
            continue
        rezepte = service.rezept_nach_index(gerichte,nummer)

        if not rezepte or 0:
            print("Kein Rezept passt zu diesen Angaben.")
            continue

        
        for zeile in rezepte.anzeigen():
            print(zeile)


def rezepte_ansehen():
    while True:
        filterwahl = filter_auswaehlen()

        if filterwahl == 0:
            return
        
        elif filterwahl == 1:
            rezepte_ansehen_nach_Gericht()
            continue

        elif filterwahl == 2:
            rezepte_ansehen_nach_zutaten()
            continue
        
        elif filterwahl == 3:
            rezepte_ansehen_nach_gang()
            continue
        
        
        else:
            print("Ungültige Auswahl.")

def rezept_einfuegen():
    rezeptname = input("Wie heißt das Rezept?" \
    "0-[Zurück]:\n").strip()

    if rezeptname == "0":
        return

    zutaten_input = input("Welche Zutaten in welcher Menge brauch es?( Zutaten bitte mit , trennen[z.B. Enokis 200 g, Salz 2 Prise])")
    zutaten_strings = [z.strip() for z in zutaten_input.split(",")if z.strip()]
    zubereitung = input("Wie wird es zubereitet?") 
    notizen = input("Notizen oder Tipps")
    gangeingabe = None
    while gangeingabe is None:
        eingabe = input("Ist es Vorspeise, Hauptspeise oder Dessert? ").strip().lower()
        if service.gang_pruefen(eingabe):
                gangeingabe = eingabe
        else:
            print("Ungültige Auswahl! Bitte erneut eingeben.") 

    rezept = service.rezepterstellung(rezeptname, zutaten_strings, zubereitung,gangeingabe,notizen)
    print(f"{rezept.name} wurde eingefügt!")
    return

def rezept_loeschen():
        for i, rezept in enumerate(service.alle_rezepte(), start=1):
            print(f"{i}. {rezept.name}")
        
        while True:
            
            gerichte = service.alle_rezepte()
            nummer = eingabezahl_pruefen("Welche Nummer soll gelöscht werden?\n"
            "0-[Zurück]:\n",min_value=0,max_value=len(gerichte))                # len(alle_rezepte())würde auch gehen aber so ist es effizienter und logischer wenn
                                                                                # schon durch gerichte einmal die funktion aufgerufen wurde.
            if nummer == 0:
                break
            
            rezept_zum_loeschen = service.rezept_nach_index(gerichte,nummer)

            if rezept_zum_loeschen is None:
                print("Rezept nicht gefunden.")
                return

            for zeile in rezept_zum_loeschen.anzeigen():
                print(zeile)
                
            rueckversichern = input(f"Sind sie sicher, dass {rezept_zum_loeschen.name} gelöscht werden soll? Ja/Nein").strip().lower()

            if rueckversichern.strip().lower() == "ja":
                    service.rezept_loeschen(rezept_zum_loeschen)
                    print(f"{rezept_zum_loeschen} wurde gelöscht!")
                    return
            
            else:
                print(f"{rezept_zum_loeschen} wird nicht gelöscht.")
                break




service.rezept_laden()
# Vor dem Programm ausführen um die aktuellste Rezeptliste aus JSON geladen zu haben.



while neustart:

    Menueauswahl = input("""Möchten sie ein Rezept \n
1-[ansehen]
2-[einfügen]
3-[löschen]\n
Eingabe:""")



    if Menueauswahl == "1":

        rezepte_ansehen()



    elif Menueauswahl == "2":

        rezept_einfuegen()



    elif Menueauswahl == "3":
        
        rezept_loeschen()
        


    else:
        print("Ungültige Auswahl!")
        continue
        


