import textwrap


class Zutaten:
    def __init__(self, name, menge=None, einheit=None):
        self.name = name
        self.menge = menge
        self.einheit = einheit

    def __str__(self):
        if self.menge is None:
            return self.name
        return f"{self.name} ({self.menge} {self.einheit})"


class Rezept:
    def __init__(self, name, zutaten, zubereitung, gang, notizen=""):
        self.name = name
        self.zutaten = zutaten          # Liste von Zutat-Objekten
        self.zubereitung = zubereitung
        self.gang = gang 
        self.notizen = notizen

    def _format_block(self, label, value, width=60):
        wrapper = textwrap.TextWrapper(
            width=width,
            subsequent_indent=" " * 13
        )

        lines = []

        if isinstance(value, list):
            first = True
            for item in value:
                wrapper.initial_indent = f"{label:<13}" if first else " " * 13
                first = False
                lines.extend(wrapper.wrap(str(item)))
        else:
            wrapper.initial_indent = f"{label:<13}"
            lines.extend(wrapper.wrap(str(value)))

        return lines

    def anzeigen(self):
        output = []
        output += self._format_block("Gericht:", self.name)
        output += self._format_block("Zutaten:", self.zutaten)
        output += self._format_block("Zubereitung:", self.zubereitung)
        output += self._format_block("Notizen:", self.notizen)
        return output