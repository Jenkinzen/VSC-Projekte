import rezeptliste_model as model
import rezeptliste_storage as storage
from typing import List, Optional
from rezeptliste_repository import JsonRezeptRepository




######## BASISZUGRIFF - LESEN #################################################################################################################################

 
def alle_rezepte(repo: JsonRezeptRepository) -> List[model.Rezept]:
    return repo.alle()

def rezept_nach_index(rezepte: List[model.Rezept], index: int) -> Optional[model.Rezept]:
    """index = auswahl der Gerichtnummer im UI.
    wenn die auswahl größer gleich 1 ist und kleiner als die
    gesamtanzahl an rezepten (len(rezepte) nummeriert die einzelnen Objekte in der Liste durch
    ,hier halt die Rezepte in der Liste Gerichte)"""
    if 1 <= index <= len(rezepte):
        return rezepte[index - 1]
    return None

def rezept_finden(repo: JsonRezeptRepository, rezeptname: str) -> Optional[model.Rezept]:

    return repo.find_by_name(rezeptname)


######## VALIDIERUNG ##############################################################################################################################################

def gang_pruefen(gangeingabe):
    return gangeingabe.lower().strip() in storage.GUELTIGE_GAENGE

def gang_validieren(gerichte, gangeingabe):
    """wenn irgendwas (any) in rezept.Gang das beinhaltet was der input war dann gibs raus
   any ----> auch wenn man "des" eingibt zeigt er dessert an weil des dadrin steckt.
   ohne any würde er dann nichts raus geben."""
    gang = gangeingabe.strip().lower()
    return any(
        rezept.gang.strip().lower() == gang
        for rezept in gerichte
    )

######## FILTER ####################################################################################################################################################

def filter_rezepte_nach_gericht(repo: JsonRezeptRepository, gericht: str) -> List[model.Rezept]:
    """wollte eigentlich mit "any" arbeiten, aber teiltreffer ("Bro" eingabe zeigt "Brokkoli" an)
    werden auch durch "in" ermöglicht. any macht kein sinn weil gerichte.Name keine Liste
     sondern ein String ist, bei Zutaten machte es Sinn weil Zutaten eine Liste ist.(any = irgendeins aus (der liste)/ in = irgendetwas in (string))
     """
    gericht = gericht.strip().lower()
    return [r for r in repo.alle() if gericht in r.name.strip().lower()]

def filter_rezepte_nach_gang(repo: JsonRezeptRepository, gangeingabe: str) -> List[model.Rezept]:
    """Siehe filter_rezepte_nach_zutaten, selbe sache nur ohne aus einer liste(gerichte)
   eine weitere liste(wie unten die zutatenliste) aufrufen zu müssen."""
    gang = gangeingabe.strip().lower()
    return [r for r in repo.alle() if r.gang.strip().lower() == gang]

def filter_rezepte_nach_zutaten(repo: JsonRezeptRepository, zutateneingabe: List[str]) -> List[model.Rezept]:
    """ rezept for rezept in storage.Gerichte > geh jedes rezept durch was gespeichert wurde.(s.Gerichte = rezeptsammlung / rezept for rezept = jedes Rezept einzeln durchgehen)
    any(zutat in einzelne_zutat = gibt es die gesuchten Zutaten im Rezept? ///// for einzelne_zutat in rezept.Zutaten) = guck jede Zutat des Rezepts an.
    all(any(bla)for zutat in zutaten) =  sind ALLE gesuchten Zutaten in diesem Rezept?""" 
    zutatenwahl = [z.strip().lower() for z in zutateneingabe if z.strip()]
    return [
        rezept
        for rezept in repo.alle()
        if all(
            any(zutat in einzelne_zutat.name.strip().lower() for einzelne_zutat in rezept.zutaten)
            for zutat in zutatenwahl
        )
    ]

######## ÄNDERUNGEN ################################################################################################################################################


    """In die Leere Zutatenliste kommen nachher die Objekte aus der Funktion.
        zs variable für Zutat als Text ( wie das 1. x in x for x in Gerichte )
        teile = zs.split() -> die Sachen werden durch leerzeichen gesplittet(also Name,menge,einheit)
        if not teile -> überspringen von allem was sonst zum error führen würde, bzw durch so einen Input
        wird man per continue dann wieder an den Schleifenanfang gebracht für erneuten input.

        zutatenname Zeile -> teile (also die Teile der Zutat: Name, menge, einheit)
          [:-2] heißt NICHT geteilt durch -2 sondern : sagt alles und -2 bis auf die letzten beiden! 
          damit wird jeder Input bis auf die letzten beiden zum "teil" Name hinzugefügt.
          wenns bspw [:-1] wär dann würde die Menge noch mit beim Namen stehen.
          und durch .join davor wird die liste von wörtern zu einem String mit Leerzeichen.
        if len(teile) > 2 -> also mach .join(teile[:-2]) insofern mehr als 2 wörter eingegeben werde.
        else teile[0] -> wenn weniger als 2 wörter eingegeben werden, nimm halt das 1 Wort oder die Leerstelle.
        
        menge -> teile[-2] if len(teile) > 1  --> also vorletztes Teil
            wenn es mehr als 1 teil gibt
            else None -> sonst gibts halt keine Menge. 
            (Unfassbar smart, weil es "Salz , Prise" gibt also angaben ohne Menge,
            aber es gibt keine Angaben ohne Einheit aber mit Menge, weil was will jemand mit
            der aussage " du brauchst 150 Salz")
            
        einheit -> teile[-1] also ist das letzte teil
                if len(teile) >= 2 -> insofern es genau oder mehr als 2 teile gibt.
    """
    
def rezepterstellung(
    repo: JsonRezeptRepository,
    rezeptname: str,
    zutaten_strings: List[str],
    zubereitung: str,
    gang: str,
    notizen: str,
) -> model.Rezept:
    zutatenliste: List[model.Zutaten] = []
    for zs in zutaten_strings:
        teile = zs.split()
        if not teile:
            continue
        zutatenname = " ".join(teile[:-2]) if len(teile) > 2 else teile[0]
        menge = teile[-2] if len(teile) > 2 else None
        einheit = teile[-1] if len(teile) >= 2 else None
        zutatenliste.append(model.Zutaten(name=zutatenname, menge=menge, einheit=einheit))

    neues_rezept = model.Rezept(
        name=rezeptname,
        zutaten=zutatenliste,
        zubereitung=zubereitung,
        notizen=notizen,
        gang=gang.title(),
    )

    repo.add(neues_rezept)
    repo.save()
    return neues_rezept

"""def rezept_laden():
    storage.lade_rezepte()
    
    Ist jetzt hinfällig da diese Funktion von repo übernommen wird."""

def rezept_loeschen(repo: JsonRezeptRepository, rezept: model.Rezept) -> None:
    repo.remove(rezept)
    repo.save()
