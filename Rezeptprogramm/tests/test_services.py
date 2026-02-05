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

    # verhindere Dateizugriff
    monkeypatch.setattr(storage, "speichere_rezepte", lambda: None)


def test_rezept_nach_index_gueltig():
    r1 = model.Rezept("A", [], "z", "Hauptgericht", "")
    r2 = model.Rezept("B",[],"z","Dessert","")

    result = services.rezept_nach_index([r1,r2],1)
