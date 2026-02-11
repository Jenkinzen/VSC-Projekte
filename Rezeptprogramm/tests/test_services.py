import pytest 
import rezeptliste_storage as storage
import rezeptliste_services as service
import rezeptliste_model as model
"""Damit pytest Sachen findet , Ordner immer mit test_[irgendwas].py oder [irgendwas]_test.py betiteln
und auch test funktionen immer mit test_ beginnen damit pytest diese automatisch im ordner findet."""

"""Genereller Testaufbau:
    Arrange - Daten aufbauen (hier wird ja über den monkeypatch ne leere Liste aufgerufen, also muss man ein Rezept im Test einfügen um an diesem Rezept zu testen [zumindest mit monkeypatch])
    Act     - Funktion aufrufen(Die funktion die man halt testen möchte)
    Assert  - per assert funktion die Erwartungen überprüfen die man hat[ (assert service.gang_pruefen("Dessert") is True ) ] bspw.

    /to assert - behaupten | -> ich behaupte dies und das wird dabei raus kommen, stimmt das?
    """

# autouse = True > wird vor jedem test automatisch ausgeführt
@pytest.fixture(autouse=True)
def isolate_storage(monkeypatch):
    # vor jedem Test: leere Liste
    storage.Gerichte.clear()

    # verhindere Dateizugriff                       // lambda: None -> lambda = erstelle eine funktion  , : None -> die nichts tut (quasi der Platzhalter für die speichere_rezepte Funktion)
    monkeypatch.setattr(storage, "speichere_rezepte", lambda: None)
    monkeypatch.setattr(storage, "lade_rezepte", lambda: None)
    
def test_rezept_nach_index_gueltig():
    r1 = model.Rezept("A", [], "z", "Hauptspeise", "")
    r2 = model.Rezept("B",[],"z","Dessert","")

    result = service.rezept_nach_index([r1,r2],1)

    assert result is r1
    assert result is not None
    assert result.name == "A"

    

def test_rezept_finden_case_insensitive():
    storage.Gerichte.append(model.Rezept("Spaghetti", [], "z", "Hauptspeise", ""))

    result = service.rezept_finden(" spaghetti ")
    assert result is not None
    assert result.name == "Spaghetti"

    assert service.rezept_finden("Pizza") is None

def test_filter_rezepte_nach_gang():
    storage.Gerichte.append(model.Rezept("A", [], "z", "Dessert", ""))
    storage.Gerichte.append(model.Rezept("B", [], "z", "Hauptspeise", ""))

    result = service.filter_rezepte_nach_gang("dessert")
    assert [r.name for r in result] == ["A"]

def test_filter_rezepte_nach_zutaten_all_must_match():
    r1 = model.Rezept(
        "Pasta",
        [model.Zutaten("tomate", None, "stück"), model.Zutaten("salz", None, "prise")],
            "z",
            "Hauptspeise",
        ""
    )
    r2 = model.Rezept(
        "Brot",
        [model.Zutaten("mehl", "500", "g"), model.Zutaten("salz", None, "prise")],
        "z",
        "Hauptspeise",
        ""
    )
    storage.Gerichte.extend([r1, r2])

    result = service.filter_rezepte_nach_zutaten(["salz", "tomate"])
    assert [r.name for r in result] == ["Pasta"]


########################### EIGENE TESTS #############################################################################################################################

def test_gang_pruefen():
     
    test1 = service.gang_pruefen("Dessert")
    test2 = service.gang_pruefen("dessert")
    test3 = service.gang_pruefen(" dessert ")
    test4 = service.gang_pruefen("dessssert")
    test5 = service.gang_pruefen("d e s s e r t ")
    test6 = service.gang_pruefen("Eima swei halbe hahn bidde")

    assert test1 is True
    assert test2 is True
    assert test3 is True
    assert test4 is False   #zu viele 's'
    assert test5 is False   #Falsch weil .strip() nur die leerzeichen vor dem ersten und nach dem letzten Buchstaben weg macht. also is dann quasi immernoch "d e s s e r t"
    assert test6 is False   #merkste selber,wa?

    """optimiert Version von GPT"""

def test_gang_pruefen_optimiert():

    #wahr
    assert service.gang_pruefen("Dessert") is True
    assert service.gang_pruefen("dessert") is True
    assert service.gang_pruefen(" dessert ") is True

    #falsch
    assert service.gang_pruefen("dessssert") is False
    assert service.gang_pruefen("d e s s e r t ") is False
    assert service.gang_pruefen("Eima swei halbe hahn") is False

"""xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"""

def test_filter_rezepte_nach_gericht():

    storage.Gerichte.append(model.Rezept("Kokoscurry-Sushibowl-Schokomousse",[],"x","x","x"))
    storage.Gerichte.append(model.Rezept("Misosuppe",[],"x","x","x"))

    #wahr

    result1 = service.filter_rezepte_nach_gericht("Curr") 
    result2 = service.filter_rezepte_nach_gericht("sUsH ") 
    result3 = service.filter_rezepte_nach_gericht(" schok") 
    result4 = service.filter_rezepte_nach_gericht("Miso")
    result5 = service.filter_rezepte_nach_gericht("su")

    assert any(r.name for r in result1) 
    assert (r.name == "Kokoscurry-Sushibowl-Schokomousse" for r in result2) 
    assert any(r.name for r in result3)
    assert (r.name == "Misosuppe" for r in result4)
    assert {r.name  for r in result5} == {"Kokoscurry-Sushibowl-Schokomousse","Misosuppe"}

    """Testet durch {} generell ob die beiden Namen, und NUR die beiden Namen im Set(so heißt das wenn man
    ne Liste mit {} einklammert) sind. Die Reihenfolge ist egal.
     Wenn diese beiden im Set enthalten sind, aber noch irgendetwas anderes dadrin wäre der test falsch."""
    
    assert [r.name  for r in result5] == ["Kokoscurry-Sushibowl-Schokomousse","Misosuppe"]

    """Testet durch [] als Liste, der unterschied ist, hier muss die Reihenfolge stimmen( by default ist
    die Reihenfolge > was als erstes eingefügt wurde kommt zuerst dran[also hier erst kokosbla dann Misosuppe])
    deshalb """


    """WICHTIG!!!! WENN MAN EIN SET {} TESTET MUSS AUCH DIE LC EIN SET{} SEIN.
                   WENN MAN EINE LIST [] TESTET MUSS AUCH DIE LC EINE LIST [] SEIN. """
    
    """ ALTERNATIV KANN MAN EINE LISTE WIE UNTEN IN DER OPTIMIERTEN VERSION ZUM SET 
                    UMWANDELN:
                    assert set(names("e")) == {"Kokoscurry-Sushibowl-Schokomousse","Ekelpampe"}"""
    

    assert any(r.name for r in service.filter_rezepte_nach_gericht("Curr"))

    #falsch

    result4 = service.filter_rezepte_nach_gericht("myv2")  
    result5 = service.filter_rezepte_nach_gericht("ölgi")   
    result6 = service.filter_rezepte_nach_gericht("3425") 

    assert not any(r.name for r in result5) 
    assert not any(r.name for r in result6)
    assert not any(r.name for r in result4) 
    assert not [r.name  for r in result5] == ["Misosuppe","Kokoscurry-Sushibowl-Schokomousse"]

    """Selbst optimierte Version nach rumprobieren"""

def test_filter_rezepte_nach_gericht_optimal():

    storage.Gerichte.append(model.Rezept("Kokoscurry-Sushibowl-Schokomousse",[],"x","x","x"))

    #wahr

    assert any(r.name for r in service.filter_rezepte_nach_gericht("Curr"))
    assert any(r.name for r in service.filter_rezepte_nach_gericht("sUsH"))
    assert any(r.name for r in service.filter_rezepte_nach_gericht(" schok"))

    #falsch

    assert not any(r.name for r in service.filter_rezepte_nach_gericht("g932d"))
    assert not any(r.name for r in service.filter_rezepte_nach_gericht("schnokomabe"))
    assert not any(r.name for r in service.filter_rezepte_nach_gericht("miep-2xx.r9"))

    

"""Optimierung von GPT"""

def test_filter_rezepte_nach_gericht_noch_krasser_optimiert():

    
    storage.Gerichte.append(model.Rezept("Kokoscurry-Sushibowl-Schokomousse", [], "x", "x", "x"))
    storage.Gerichte.append(model.Rezept("Ekelpampe",[],"x","x","x"))
                            
    def names(q):
        return [r.name for r in service.filter_rezepte_nach_gericht(q)]

    # wahr (Teilstrings + case + whitespace)
    assert "Kokoscurry-Sushibowl-Schokomousse" in names("Curr")
    assert "Kokoscurry-Sushibowl-Schokomousse" in names("sUsH ")
    assert "Kokoscurry-Sushibowl-Schokomousse" in names(" schok")

    assert set(names("e")) == {"Kokoscurry-Sushibowl-Schokomousse","Ekelpampe"}

    # falsch
    assert names("g932d") == []
    assert names("schnokomabe") == []
    assert names("miep-2xx.r9") == []
"""xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"""

def test_alle_rezepte():

    storage.Gerichte.append(model.Rezept("1",[],"x","x","x"))
    storage.Gerichte.append(model.Rezept("2",[],"x","x","x"))
    storage.Gerichte.append(model.Rezept("3",[],"x","x","x"))
    storage.Gerichte.append(model.Rezept("4",[],"x","x","x"))
    storage.Gerichte.append(model.Rezept("5",[],"x","x","x"))
    storage.Gerichte.append(model.Rezept("6",[],"x","x","x"))

    def names():
        return len([r.name for r in storage.Gerichte])
    
    assert names() == 6

# wichtig!! nur mit names klappt es nicht, die () is wichtig und heißt "führe diese funktion jetzt aus"

"""Optimale Form von Chat GPT """

def test_alle_rezepte_optimal():

    storage.Gerichte.append(model.Rezept("1",[],"x","x","x"))
    storage.Gerichte.append(model.Rezept("2",[],"x","x","x"))
    storage.Gerichte.append(model.Rezept("3",[],"x","x","x"))
    storage.Gerichte.append(model.Rezept("4",[],"x","x","x"))
    storage.Gerichte.append(model.Rezept("5",[],"x","x","x"))
    storage.Gerichte.append(model.Rezept("6",[],"x","x","x"))

    assert len(storage.Gerichte) == 6

    

"""xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"""

def test_rezept_loeschen():
    storage.Gerichte.append(model.Rezept("Handfeuerwaffeln",[],"x","x","x"))

    rezept = service.rezept_finden("Handfeuerwaffeln")
    service.rezept_loeschen(rezept) 
    assert len(storage.Gerichte) == 0

    
"""xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"""

def test_rezept_einfuegen():

    service.rezepterstellung("Handfeuerwaffeln",["Waffeln 4 Stück","Schießpulver 200 g","Schnittlauch Bündel"],"x","x","x")
    assert len(storage.Gerichte) == 1

    rezept = storage.Gerichte[0]

    schnittlauch = next(z for z in rezept.zutaten if z.name == "Schnittlauch")
    schießpulver = next(z for z in rezept.zutaten if z.name == "Schießpulver")
    waffeln = next(z for z in rezept.zutaten if z.name == "Waffeln")

    assert schnittlauch.menge is None
    assert waffeln.einheit == "Stück"
    assert schießpulver.menge == "200"

    assert waffeln.menge != "5"
    assert schießpulver.name != "piesschulver"
    assert schnittlauch.menge != "Dingens"

    

"""xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"""

