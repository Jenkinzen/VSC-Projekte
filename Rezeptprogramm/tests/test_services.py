import pytest 
import rezeptliste_storage as storage
import rezeptliste_services as services
import rezeptliste_model as model
"""Damit pytest Sachen findet , Ordner immer mit test_[irgendwas].py oder [irgendwas]_test.py betiteln
und auch test funktionen immer mit test_ beginnen damit pytest diese automatisch im ordner findet."""

# autouse = True > wird vor jedem test automatisch ausgeführt
@pytest.fixture(autouse=True)
def isolate_storage(monkeypatch):
    # vor jedem Test: leere Liste
    storage.Gerichte.clear()

    # verhindere Dateizugriff                       // lambda: None -> lambda = erstelle eine funktion  , : None -> die nichts tut (quasi der Platzhalter für die speichere_rezepte Funktion)
    monkeypatch.setattr(storage, "speichere_rezepte", lambda: None)

def test_rezept_nach_index_gueltig():
    r1 = model.Rezept("A", [], "z", "Hauptgericht", "")
    r2 = model.Rezept("B",[],"z","Dessert","")

    result = services.rezept_nach_index([r1,r2],1)

def test_rezept_finden_case_insensitive():
    storage.Gerichte.append(model.Rezept("Spaghetti", [], "z", "Hauptgericht", ""))

    result = services.rezept_finden(" spaghetti ")
    assert result is not None
    assert result.name == "Spaghetti"

    assert services.rezept_finden("Pizza") is None

def test_filter_rezepte_nach_gang():
    storage.Gerichte.append(model.Rezept("A", [], "z", "Dessert", ""))
    storage.Gerichte.append(model.Rezept("B", [], "z", "Hauptgericht", ""))

    result = services.filter_rezepte_nach_gang("dessert")
    assert [r.name for r in result] == ["A"]

def test_filter_rezepte_nach_zutaten_all_must_match():
    r1 = model.Rezept(
        "Pasta",
        [model.Zutaten("tomate", None, "stück"), model.Zutaten("salz", None, "prise")],
            "z"
        "Hauptgericht",
        ""
    )
    r2 = model.Rezept(
        "Brot",
        [model.Zutaten("mehl", "500", "g"), model.Zutaten("salz", None, "prise")],
        "z",
        "Hauptgericht",
        ""
    )
    storage.Gerichte.extend([r1, r2])

    result = services.filter_rezepte_nach_zutaten(["salz", "tomate"])
    assert [r.name for r in result] == ["Pasta"]
