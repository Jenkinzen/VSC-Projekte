import json
from pathlib import Path
from typing import List
import rezeptliste_model as model

DATEI = Path(__file__).resolve().parent / "rezepte.json"
# __file__ sagt : der Dateipfad von dieser Datei, also Ordner:C:// ........ Rezeptprogramm| 
# .resolve() macht einen absoluten Pfad
# .parent ist der Ordner in dem diese Datei liegt
# "rezepte.json" hängt den Dateinamen an den Pfad des Ordners
# alles zusammen -> egal von wo, wenn auf die "rezepte.json" Datei zugegriffen wird ist es IMMER(resolve) die json Datei die im Ordner 
# liegt in der auch diese Datei ist. 
Gerichte: List[model.Rezept] = []



GUELTIGE_GAENGE = ["vorspeise", "hauptspeise", "dessert"]

def lade_rezepte():
    """global Gerichte ist der Verweis auf die zentrale leere Liste  (Gerichte: List[Rezept] = [])
       in DIESEM Modul (rezeptliste_storage) in die beim öffnen des Programmes die Daten in der JSON Datei reingeladen werden.
        """
    global Gerichte
    if not DATEI.exists():
        Gerichte = []
        return

    with open(DATEI, "r", encoding="utf-8") as f:
        daten = json.load(f)

    Gerichte = []

    for r in daten:
        zutaten = [
            model.Zutaten(
                z["name"],
                z.get("menge"),
                z.get("einheit")
            )
            for z in r.get("zutaten", [])
        ]

        rezept = model.Rezept(
            name=r["name"],
            zutaten=zutaten,
            zubereitung=r["zubereitung"],
            gang=r["gang"],
            notizen=r.get("notizen", "")
        )

        Gerichte.append(rezept)

def speichere_rezepte():
    daten = []

    for r in Gerichte:
        daten.append({
            "name": r.name,
            "gang": r.gang,
            "zubereitung": r.zubereitung,
            "notizen": r.notizen,
            "zutaten": [
                {
                    "name": z.name,
                    "menge": z.menge,
                    "einheit": z.einheit
                }
                for z in r.zutaten
            ]
        })

    with open(DATEI, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=2, ensure_ascii=False)


def rezept_hinzufuegen(rezept: model.Rezept):
    global Gerichte
    Gerichte.append(rezept)
    speichere_rezepte()

def rezept_loeschen(rezept: model.Rezept):
    global Gerichte
    Gerichte.remove(rezept)
    speichere_rezepte()

