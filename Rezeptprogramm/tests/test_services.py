import pytest
import rezeptliste_services as service
import rezeptliste_model as model

from rezeptliste_repository import JsonRezeptRepository


"""Damit pytest Sachen findet , Ordner immer mit test_[irgendwas].py oder [irgendwas]_test.py betiteln
und auch test funktionen immer mit test_ beginnen damit pytest diese automatisch im ordner findet."""

"""Genereller Testaufbau:
    Arrange - Daten aufbauen (hier wird ja über den monkeypatch ne leere Liste aufgerufen, also muss man ein Rezept im Test einfügen um an diesem Rezept zu testen [zumindest mit monkeypatch])
    Act     - Funktion aufrufen(Die funktion die man halt testen möchte)
    Assert  - per assert funktion die Erwartungen überprüfen die man hat[ (assert service.gang_pruefen("Dessert") is True ) ] bspw.

    /to assert - behaupten | -> ich behaupte dies und das wird dabei raus kommen, stimmt das?
    """

@pytest.fixture
def repo(tmp_path):
    datei = tmp_path / "rezepte.json"
    r = JsonRezeptRepository(datei)
    r.load()  # startet leer, weil Datei noch nicht existiert
    return r
    


def test_rezept_nach_index_gueltig(repo):
    r1 = repo.add(model.Rezept("A", [], "z", "Hauptspeise", ""))
    r2 = repo.add(model.Rezept("B",[],"z","Dessert",""))

    result = service.rezept_nach_index([r1,r2],1)

    assert result is r1
    assert result is not None
    assert result.name == "A"

def test_rezept_finden_case_insensitive(repo):
    repo.add(model.Rezept("Spaghetti", [], "z", "Hauptspeise", ""))

    result = service.rezept_finden(repo," spaghetti ")
    assert result is not None
    assert result.name == "Spaghetti"

    assert service.rezept_finden(repo,"Pizza") is None

def test_filter_rezepte_nach_gang(repo):
    repo.add(model.Rezept("A", [], "z", "Dessert", ""))
    repo.add(model.Rezept("B", [], "z", "Hauptspeise", ""))

    result = service.filter_rezepte_nach_gang(repo,"dessert")
    assert [r.name for r in result] == ["A"]

def test_filter_rezepte_nach_zutaten_all_must_match(repo):
    r1 = repo.add(model.Rezept(
        "Pasta",
        [model.Zutaten("tomate", None, "stück"), model.Zutaten("salz", None, "prise")],
            "z",
            "Hauptspeise",
        ""
    ))
    r2 = repo.add(model.Rezept(
        "Brot",
        [model.Zutaten("mehl", "500", "g"), model.Zutaten("salz", None, "prise")],
        "z",
        "Hauptspeise",
        ""
    ))
    result = service.filter_rezepte_nach_zutaten(repo,["salz", "tomate"])
    assert [r.name for r in result] == ["Pasta"]

def test_repo_roundtrip(tmp_path):
    datei = tmp_path / "rezepte.json"
    repo1 = JsonRezeptRepository(datei)

    repo1.add(model.Rezept(
        "Toast",
        [model.Zutaten("brot", "2", "scheiben")],
        "toasten",
        "Hauptspeise",
        ""
    ))
    repo1.save()

    repo2 = JsonRezeptRepository(datei)
    repo2.load()

    toast = repo2.find_by_name("Toast")

    assert toast is not None
    assert toast.zutaten[0].name == "brot"

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

    """optimiert + parametrize funktion von pytest"""

# "text, expected" gibt quasi die beiden parameter vor die danach im Tupel kommen ( also text ="Dessert", expected = True) 
# warum auch immer man das hier als String anlegt  
@pytest.mark.parametrize(["text", "expected"], [
("Dessert", True),
(" dessert ", True),
("dessssert", False),
])
def test_gang_pruefen_parametrize(text, expected):
    assert service.gang_pruefen(text) is expected

"""xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"""

def test_filter_rezepte_nach_gericht(repo):

    repo.add(model.Rezept("Kokoscurry-Sushibowl-Schokomousse",[],"x","x","x"))
    repo.add(model.Rezept("Misosuppe",[],"x","x","x"))

    #wahr

    result1 = service.filter_rezepte_nach_gericht(repo,"Curr") 
    result2 = service.filter_rezepte_nach_gericht(repo,"sUsH ") 
    result3 = service.filter_rezepte_nach_gericht(repo," schok") 
    result4 = service.filter_rezepte_nach_gericht(repo,"Miso")
    result5 = service.filter_rezepte_nach_gericht(repo,"su")

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
    

    assert any(r.name for r in service.filter_rezepte_nach_gericht(repo,"Curr"))

    #falsch

    result4 = service.filter_rezepte_nach_gericht(repo,"myv2")  
    result5 = service.filter_rezepte_nach_gericht(repo,"ölgi")   
    result6 = service.filter_rezepte_nach_gericht(repo,"3425") 

    assert not any(r.name for r in result5) 
    assert not any(r.name for r in result6)
    assert not any(r.name for r in result4) 
    assert not [r.name  for r in result5] == ["Misosuppe","Kokoscurry-Sushibowl-Schokomousse"]

    """Selbst optimierte Version nach rumprobieren"""

def test_filter_rezepte_nach_gericht_optimal(repo):

    repo.add(model.Rezept("Kokoscurry-Sushibowl-Schokomousse",[],"x","x","x"))

    #wahr

    assert any(r.name for r in service.filter_rezepte_nach_gericht(repo,"Curr"))
    assert any(r.name for r in service.filter_rezepte_nach_gericht(repo,"sUsH"))
    assert any(r.name for r in service.filter_rezepte_nach_gericht(repo," schok"))

    #falsch

    assert not any(r.name for r in service.filter_rezepte_nach_gericht(repo,"g932d"))
    assert not any(r.name for r in service.filter_rezepte_nach_gericht(repo,"schnokomabe"))
    assert not any(r.name for r in service.filter_rezepte_nach_gericht(repo,"miep-2xx.r9"))   
"""Optimierung von GPT"""
def test_filter_rezepte_nach_gericht_noch_krasser_optimiert(repo):


    repo.add(model.Rezept("Kokoscurry-Sushibowl-Schokomousse", [], "x", "x", "x"))
    repo.add(model.Rezept("Ekelpampe",[],"x","x","x"))
                            
    def names(repo,q):
        return [r.name for r in service.filter_rezepte_nach_gericht(repo,q)]

    # wahr (Teilstrings + case + whitespace)
    assert "Kokoscurry-Sushibowl-Schokomousse" in names(repo,"Curr")
    assert "Kokoscurry-Sushibowl-Schokomousse" in names(repo,"sUsH ")
    assert "Kokoscurry-Sushibowl-Schokomousse" in names(repo," schok")

    assert set(names(repo,"e")) == {"Kokoscurry-Sushibowl-Schokomousse","Ekelpampe"}

    # falsch
    assert names(repo,"g932d") == []
    assert names(repo,"schnokomabe") == []
    assert names(repo,"miep-2xx.r9") == []
"""xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"""
def test_alle_rezepte(repo):

    repo.add(model.Rezept("1",[],"x","x","x"))
    repo.add(model.Rezept("2",[],"x","x","x"))
    repo.add(model.Rezept("3",[],"x","x","x"))
    repo.add(model.Rezept("4",[],"x","x","x"))
    repo.add(model.Rezept("5",[],"x","x","x"))
    repo.add(model.Rezept("6",[],"x","x","x"))

    def names():
        return len([r.name for r in repo.alle()])
    
    assert names() == 6
# wichtig!! nur mit names klappt es nicht, die () is wichtig und heißt "führe diese funktion jetzt aus"
"""Optimale Form von Chat GPT """
def test_alle_rezepte_optimal(repo):

    repo.add(model.Rezept("1",[],"x","x","x"))
    repo.add(model.Rezept("2",[],"x","x","x"))
    repo.add(model.Rezept("3",[],"x","x","x"))
    repo.add(model.Rezept("4",[],"x","x","x"))
    repo.add(model.Rezept("5",[],"x","x","x"))
    repo.add(model.Rezept("6",[],"x","x","x"))

    assert len(repo.alle()) == 6
"""xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"""
def test_rezept_loeschen(repo):
    repo.add(model.Rezept("Handfeuerwaffeln",[],"x","x","x"))

    rezept = service.rezept_finden(repo,"Handfeuerwaffeln")
    assert rezept is not None
    service.rezept_loeschen(repo,rezept) 
    assert len(repo.alle()) == 0  
"""xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"""
def test_rezept_einfuegen(repo):

    service.rezepterstellung(repo,"Handfeuerwaffeln",["Waffeln 4 Stück","Schießpulver 200 g","Schnittlauch Bündel"],"x","x","x")
    assert len(repo.alle()) == 1

    rezept = repo.alle()[0]

    schnittlauch = next(z for z in rezept.zutaten if z.name == "Schnittlauch")
    schießpulver = next(z for z in rezept.zutaten if z.name == "Schießpulver")
    waffeln = next(z for z in rezept.zutaten if z.name == "Waffeln")

    assert schnittlauch.menge is None
    assert schnittlauch.einheit == "Bündel"
    assert waffeln.einheit == "Stück"
    assert schießpulver.menge == "200"

    assert waffeln.menge != "5"
    assert schießpulver.name != "piesschulver"
    assert schnittlauch.menge != "12" 
"""xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"""

