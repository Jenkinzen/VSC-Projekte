from dataclasses import dataclass
from typing import List, Optional
import textwrap


@dataclass
class Zutaten:
    name: str
    menge: Optional[str] = None
    einheit: Optional[str] = None

    def __str__(self):
        if self.menge is None:
            return self.name
        return f"{self.name} ({self.menge} {self.einheit})"


@dataclass
class Rezept:
    name: str
    zutaten: List[Zutaten]
    zubereitung: str
    gang: str
    notizen: str = ""

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