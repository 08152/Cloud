
"""
Cloude AI – Semantik-Modul
Analysiert Bedeutungen, Begriffe, Verneinungen und Beziehungen.

Verwendet ausschließlich die Python-Standardbibliothek.
Alle Wissensdaten liegen im Ordner DATA.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class SemanticsEngine:
    NEGATIONS = {
        "nicht", "kein", "keine", "keinen", "keinem",
        "keiner", "niemals", "nie", "nichts", "ohne"
    }

    QUESTION_WORDS = {
        "wer", "was", "wann", "wo", "warum",
        "weshalb", "wieso", "wie", "welche", "welcher"
    }

    def __init__(
        self,
        meanings_file: str | Path,
        relationships_file: str | Path
    ) -> None:
        self.meanings_file = Path(meanings_file)
        self.relationships_file = Path(relationships_file)

        self.meanings: dict[str, Any] = {}
        self.relationships: list[dict[str, Any]] = []

        self.load_data()

    @staticmethod
    def normalize(text: str) -> str:
        """Vereinheitlicht Text für Vergleiche."""
        return re.sub(r"\s+", " ", text.lower()).strip()

    def _read_json(self, path: Path, default: Any) -> Any:
        """Liest eine JSON-Datei sicher ein."""
        if not path.exists():
            return default

        try:
            with path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except (OSError, json.JSONDecodeError):
            return default

    def load_data(self) -> None:
        """Lädt Bedeutungen und Beziehungen aus DATA."""
        meanings = self._read_json(self.meanings_file, {})
        relationships = self._read_json(self.relationships_file, [])

        self.meanings = meanings if isinstance(meanings, dict) else {}
        self.relationships = (
            relationships if isinstance(relationships, list) else []
        )

    def save_meanings(self) -> None:
        """Speichert Bedeutungen in DATA."""
        self.meanings_file.parent.mkdir(parents=True, exist_ok=True)

        with self.meanings_file.open("w", encoding="utf-8") as file:
            json.dump(
                self.meanings,
                file,
                ensure_ascii=False,
                indent=4
            )

    def save_relationships(self) -> None:
        """Speichert Beziehungen in DATA."""
        self.relationships_file.parent.mkdir(parents=True, exist_ok=True)

        with self.relationships_file.open("w", encoding="utf-8") as file:
            json.dump(
                self.relationships,
                file,
                ensure_ascii=False,
                indent=4
            )

    def add_meaning(
        self,
        word: str,
        meaning: str,
        category: str = "unknown",
        examples: list[str] | None = None
    ) -> None:
        """Fügt einem Begriff eine Bedeutung hinzu."""
        key = self.normalize(word)

        if not key or not meaning.strip():
            raise ValueError("Wort und Bedeutung dürfen nicht leer sein.")

        self.meanings[key] = {
            "meaning": meaning.strip(),
            "category": category.strip(),
            "examples": examples or []
        }

        self.save_meanings()

    def add_relationship(
        self,
        source: str,
        relation: str,
        target: str
    ) -> None:
        """Speichert eine Beziehung zwischen zwei Begriffen."""
        item = {
            "source": self.normalize(source),
            "relation": self.normalize(relation),
            "target": self.normalize(target)
        }

        if not all(item.values()):
            raise ValueError("Alle Beziehungsfelder müssen ausgefüllt sein.")

        if item not in self.relationships:
            self.relationships.append(item)
            self.save_relationships()

    def find_meaning(self, word: str) -> dict[str, Any] | None:
        """Sucht die gespeicherte Bedeutung eines Wortes."""
        return self.meanings.get(self.normalize(word))

    def find_relationships(self, word: str) -> list[dict[str, Any]]:
        """Findet alle Beziehungen zu einem Begriff."""
        key = self.normalize(word)

        return [
            relation
            for relation in self.relationships
            if isinstance(relation, dict)
            and (
                self.normalize(str(relation.get("source", ""))) == key
                or self.normalize(str(relation.get("target", ""))) == key
            )
        ]

    def analyze_negation(self, words: list[str]) -> bool:
        """Prüft, ob eine Verneinung vorkommt."""
        return any(
            self.normalize(word) in self.NEGATIONS
            for word in words
        )

    def detect_question(self, text: str) -> bool:
        """Erkennt einfache Frageformen."""
        normalized = self.normalize(text)

        if "?" in text:
            return True

        words = normalized.split()
        return bool(words and words[0] in self.QUESTION_WORDS)

    def extract_known_concepts(self, text: str) -> list[dict[str, Any]]:
        """Findet bekannte Begriffe im Text."""
        normalized = self.normalize(text)
        found = []

        for word, information in self.meanings.items():
            if not isinstance(word, str) or not word:
                continue

            pattern = rf"(?<!\w){re.escape(word)}(?!\w)"

            if re.search(pattern, normalized):
                found.append({
                    "word": word,
                    "information": information
                })

        return found

    def analyze(self, text: str) -> dict[str, Any]:
        """
        Erstellt eine strukturierte Bedeutungsanalyse.

        Das Ergebnis ist eine regelbasierte Einschätzung,
        kein vollständiges Sprachverständnis.
        """
        if not isinstance(text, str):
            raise TypeError("Der Text muss eine Zeichenkette sein.")

        normalized = self.normalize(text)
        words = re.findall(r"\b[\wäöüß]+\b", normalized)

        concepts = self.extract_known_concepts(normalized)

        relations = []
        for concept in concepts:
            relations.extend(
                self.find_relationships(concept["word"])
            )

        return {
            "original_text": text,
            "normalized_text": normalized,
            "words": words,
            "is_question": self.detect_question(text),
            "contains_negation": self.analyze_negation(words),
            "known_concepts": concepts,
            "relationships": relations,
            "unknown_words": [
                word for word in words
                if word not in self.meanings
            ]
        }
