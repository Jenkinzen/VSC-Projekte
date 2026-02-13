from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

import rezeptliste_model as model


class JsonRezeptRepository:
    def __init__(self, datei: Path):
        self._datei = datei
        self._gerichte: List[model.Rezept] = []

    # ---- Zugriff ----
    def alle(self) -> List[model.Rezept]:
        # Optional: return list(self._gerichte) um Kopie zu geben
        return self._gerichte

    def add(self, rezept: model.Rezept) -> model.Rezept:
        self._gerichte.append(rezept)
        return rezept

    def remove(self, rezept: model.Rezept) -> None:
        self._gerichte.remove(rezept)

    def find_by_name(self, rezeptname: str) -> Optional[model.Rezept]:
        needle = rezeptname.strip().lower()
        for rezept in self._gerichte:
            if rezept.name.strip().lower() == needle:
                return rezept
        return None

    # ---- Persistenz ----
    def load(self) -> None:
        if not self._datei.exists():
            self._gerichte = []
            return

        with open(self._datei, "r", encoding="utf-8") as f:
            daten = json.load(f)

        gerichte: List[model.Rezept] = []
        for r in daten:
            zutaten = [
                model.Zutaten(
                    z["name"],
                    z.get("menge"),
                    z.get("einheit"),
                )
                for z in r.get("zutaten", [])
            ]

            gerichte.append(
                model.Rezept(
                    name=r["name"],
                    zutaten=zutaten,
                    zubereitung=r["zubereitung"],
                    gang=r["gang"],
                    notizen=r.get("notizen", ""),
                )
            )

        self._gerichte = gerichte

    def save(self) -> None:
        daten = []
        for r in self._gerichte:
            daten.append(
                {
                    "name": r.name,
                    "gang": r.gang,
                    "zubereitung": r.zubereitung,
                    "notizen": r.notizen,
                    "zutaten": [
                        {"name": z.name, "menge": z.menge, "einheit": z.einheit}
                        for z in r.zutaten
                    ],
                }
            )

        with open(self._datei, "w", encoding="utf-8") as f:
            json.dump(daten, f, indent=2, ensure_ascii=False)

    # ---- Komfortzugriff ----
    def __getitem__(self, index: int) -> model.Rezept:
        return self._gerichte[index]

    def __len__(self) -> int:
        return len(self._gerichte)
