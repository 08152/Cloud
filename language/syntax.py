
"""
====================================================
CLOUDE AI - SYNTAX ENGINE
Version: 0.1.0
====================================================

Eigener Syntax-Parser.

Funktionen:
- Satzstrukturen aufbauen
- Satzglieder erkennen
- Wortabhängigkeiten speichern
- Satzbäume erzeugen
- Haupt- und Nebensätze vorbereiten
- Wortpositionen analysieren
- Satzstrukturen exportieren

Nur Python-Standardbibliothek.
"""

import re

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


# ==================================================
# 1. NODE TYPES
# ==================================================

NODE_ROOT = "ROOT"
NODE_SENTENCE = "SENTENCE"
NODE_SUBJECT = "SUBJECT"
NODE_PREDICATE = "PREDICATE"
NODE_OBJECT = "OBJECT"
NODE_ATTRIBUTE = "ATTRIBUTE"
NODE_ADVERBIAL = "ADVERBIAL"
NODE_NEGATION = "NEGATION"
NODE_CONNECTOR = "CONNECTOR"
NODE_WORD = "WORD"
NODE_UNKNOWN = "UNKNOWN"


# ==================================================
# 2. SYNTAX NODE
# ==================================================

@dataclass
class SyntaxNode:

    value: str

    node_type: str

    position: int = -1

    parent: Optional["SyntaxNode"] = None

    children: List["SyntaxNode"] = field(
        default_factory=list
    )

    attributes: Dict[str, Any] = field(
        default_factory=dict
    )

    def add_child(self, child):

        child.parent = self

        self.children.append(child)

    def get_children(self, node_type=None):

        if node_type is None:
            return self.children

        return [
            child
            for child in self.children
            if child.node_type == node_type
        ]

    def to_dict(self):

        return {

            "value": self.value,

            "type": self.node_type,

            "position": self.position,

            "attributes": self.attributes,

            "children": [

                child.to_dict()

                for child in self.children

            ]

        }


# ==================================================
# 3. SYNTAX PARSER
# ==================================================

class SyntaxParser:

    def __init__(self):

        self.articles = {

            "der", "die", "das",
            "ein", "eine", "einen",
            "einem", "einer",
            "den", "dem", "des"

        }

        self.pronouns = {

            "ich", "du", "er", "sie",
            "es", "wir", "ihr",
            "mich", "dich", "ihn",
            "uns", "euch", "mir",
            "dir", "ihm", "ihnen"

        }

        self.negations = {

            "nicht", "kein", "keine",
            "keinen", "nie", "niemals"

        }

        self.connectors = {

            "und", "oder", "aber",
            "weil", "dass", "wenn",
            "obwohl", "denn", "sondern"

        }

        self.subject_markers = self.pronouns

        self.verb_dictionary = {

            "bin", "bist", "ist",
            "sind", "seid",
            "habe", "hast", "hat",
            "haben", "habt",
            "war", "waren",
            "wird", "werden",
            "wurde", "wurden",
            "gehe", "geht", "gehen",
            "komme", "kommt", "kommen",
            "mache", "macht", "machen",
            "lerne", "lernt", "lernen",
            "denke", "denkt", "denken",
            "schreibe", "schreibt",
            "schreiben", "lese", "liest",
            "lesen", "sehe", "sieht",
            "sehen", "spreche", "spricht",
            "sprechen", "kann", "können",
            "muss", "müssen", "will", "wollen"

        }

        self.subordinate_markers = {

            "weil", "dass", "wenn",
            "obwohl", "damit", "bevor",
            "nachdem", "während", "falls"

        }

    # ==============================================
    # 4. TOKENIZATION
    # ==============================================

    def tokenize(self, text):

        return re.findall(

            r"[A-Za-zÄÖÜäöüß]+"
            r"|[0-9]+"
            r"|[^\w\s]",

            text,

            re.UNICODE

        )

    # ==============================================
    # 5. WORD CLASSIFICATION
    # ==============================================

    def classify(self, word):

        normalized = word.lower()

        if normalized in self.articles:
            return "ARTICLE"

        if normalized in self.pronouns:
            return "PRONOUN"

        if normalized in self.negations:
            return "NEGATION"

        if normalized in self.connectors:
            return "CONNECTOR"

        if normalized in self.verb_dictionary:
            return "VERB"

        if normalized.isdigit():
            return "NUMBER"

        if re.fullmatch(r"[^\w\s]", word):
            return "PUNCTUATION"

        return "WORD"

    # ==============================================
    # 6. FIND VERBS
    # ==============================================

    def find_verbs(self, tokens):

        results = []

        for index, token in enumerate(tokens):

            if self.classify(token) == "VERB":

                results.append(index)

        return results

    # ==============================================
    # 7. FIND SUBJECT
    # ==============================================

    def find_subject(self, tokens, verbs):

        if not verbs:
            return None

        verb_position = verbs[0]

        candidates = tokens[:verb_position]

        for index in range(
            len(candidates) - 1,
            -1,
            -1
        ):

            token = candidates[index]

            if self.classify(token) == "PRONOUN":

                return index

        for index in range(
            len(candidates) - 1,
            -1,
            -1
        ):

            if self.classify(
                candidates[index]
            ) in {"WORD", "ARTICLE"}:

                return index

        return None

    # ==============================================
    # 8. FIND OBJECT
    # ==============================================

    def find_object(self, tokens, verbs):

        if not verbs:
            return None

        verb_position = verbs[0]

        for index in range(
            verb_position + 1,
            len(tokens)
        ):

            token_type = self.classify(
                tokens[index]
            )

            if token_type in {
                "WORD",
                "PRONOUN"
            }:

                return index

        return None

    # ==============================================
    # 9. FIND NEGATIONS
    # ==============================================

    def find_negations(self, tokens):

        return [

            index

            for index, token in enumerate(tokens)

            if self.classify(token) == "NEGATION"

        ]

    # ==============================================
    # 10. FIND CONNECTORS
    # ==============================================

    def find_connectors(self, tokens):

        return [

            index

            for index, token in enumerate(tokens)

            if self.classify(token) == "CONNECTOR"

        ]

    # ==============================================
    # 11. CREATE WORD NODE
    # ==============================================

    def create_word_node(
        self,
        token,
        position
    ):

        return SyntaxNode(

            value=token,

            node_type=NODE_WORD,

            position=position,

            attributes={

                "word_class": self.classify(token),

                "normalized": token.lower()

            }

        )

    # ==============================================
    # 12. BUILD SENTENCE TREE
    # ==============================================

    def build_tree(self, text):

        tokens = self.tokenize(text)

        root = SyntaxNode(

            value="ROOT",

            node_type=NODE_ROOT

        )

        sentence = SyntaxNode(

            value=text,

            node_type=NODE_SENTENCE

        )

        root.add_child(sentence)

        if not tokens:
            return root

        verbs = self.find_verbs(tokens)

        subject_position = self.find_subject(
            tokens,
            verbs
        )

        object_position = self.find_object(
            tokens,
            verbs
        )

        negations = self.find_negations(tokens)

        connectors = self.find_connectors(tokens)

        for index, token in enumerate(tokens):

            word_node = self.create_word_node(
                token,
                index
            )

            if index == subject_position:

                subject = SyntaxNode(
                    value=token,
                    node_type=NODE_SUBJECT,
                    position=index
                )

                subject.add_child(word_node)

                sentence.add_child(subject)

            elif index in verbs:

                predicate = SyntaxNode(
                    value=token,
                    node_type=NODE_PREDICATE,
                    position=index
                )

                predicate.add_child(word_node)

                sentence.add_child(predicate)

            elif index == object_position:

                object_node = SyntaxNode(
                    value=token,
                    node_type=NODE_OBJECT,
                    position=index
                )

                object_node.add_child(word_node)

                sentence.add_child(object_node)

            elif index in negations:

                negation = SyntaxNode(
                    value=token,
                    node_type=NODE_NEGATION,
                    position=index
                )

                negation.add_child(word_node)

                sentence.add_child(negation)

            elif index in connectors:

                connector = SyntaxNode(
                    value=token,
                    node_type=NODE_CONNECTOR,
                    position=index
                )

                connector.add_child(word_node)

                sentence.add_child(connector)

            else:

                sentence.add_child(word_node)

        sentence.attributes.update({

            "token_count": len(tokens),

            "verb_count": len(verbs),

            "has_subject": subject_position is not None,

            "has_predicate": bool(verbs),

            "has_object": object_position is not None,

            "has_negation": bool(negations),

            "has_connector": bool(connectors)

        })

        return root

    # ==============================================
    # 13. ANALYZE SENTENCE STRUCTURE
    # ==============================================

    def analyze_structure(self, text):

        tree = self.build_tree(text)

        sentence = tree.children[0]

        structure = {

            "text": text,

            "token_count": sentence.attributes.get(
                "token_count", 0
            ),

            "subject": [],

            "predicates": [],

            "objects": [],

            "negations": [],

            "connectors": [],

            "unknown_words": []

        }

        for node in sentence.children:

            if node.node_type == NODE_SUBJECT:
                structure["subject"].append(node.value)

            elif node.node_type == NODE_PREDICATE:
                structure["predicates"].append(node.value)

            elif node.node_type == NODE_OBJECT:
                structure["objects"].append(node.value)

            elif node.node_type == NODE_NEGATION:
                structure["negations"].append(node.value)

            elif node.node_type == NODE_CONNECTOR:
                structure["connectors"].append(node.value)

            elif node.node_type == NODE_WORD:

                structure["unknown_words"].append(
                    node.value
                )

        return structure

    # ==============================================
    # 14. DETECT SUBORDINATE CLAUSES
    # ==============================================

    def detect_subordinate_clauses(self, text):

        tokens = self.tokenize(text)

        clauses = []

        for index, token in enumerate(tokens):

            if token.lower() in self.subordinate_markers:

                clauses.append({

                    "connector": token,

                    "position": index,

                    "type": "subordinate_clause",

                    "remaining_tokens": tokens[index + 1:]

                })

        return clauses

    # ==============================================
    # 15. DEPENDENCY RELATIONSHIPS
    # ==============================================

    def get_dependencies(self, text):

        tokens = self.tokenize(text)

        verbs = self.find_verbs(tokens)

        subject = self.find_subject(tokens, verbs)

        object_position = self.find_object(tokens, verbs)

        dependencies = []

        if verbs and subject is not None:

            dependencies.append({

                "source": tokens[verbs[0]],

                "target": tokens[subject],

                "relation": "subject"

            })

        if verbs and object_position is not None:

            dependencies.append({

                "source": tokens[verbs[0]],

                "target": tokens[object_position],

                "relation": "object"

            })

        return dependencies

    # ==============================================
    # 16. COMPLETE ANALYSIS
    # ==============================================

    def analyze(self, text):

        return {

            "syntax_tree": self.build_tree(
                text
            ).to_dict(),

            "structure": self.analyze_structure(
                text
            ),

            "subordinate_clauses": (
                self.detect_subordinate_clauses(text)
            ),

            "dependencies": self.get_dependencies(
                text
            )

        }
