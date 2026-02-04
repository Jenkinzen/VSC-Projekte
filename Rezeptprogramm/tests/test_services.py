import pytest 
from Rezeptprogramm import rezeptliste_services as services
from Rezeptprogramm import rezeptliste_model as model
"""Damit pytest Sachen findet , Ordner immer mit test_[irgendwas].py oder [irgendwas]_test.py betiteln
und auch test funktionen immer mit test_ beginnen damit pytest diese automatisch im ordner findet."""

def test_rezept_nach_index_gueltig():
    r1 = model.Rezept("A", [], "z", "Hauptgericht", "")
    r2 = model.Rezept("B",[],"z","Dessert","")

    result = services.rezept_nach_index([r1,r2],1)
