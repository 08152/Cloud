
from pathlib import Path

# ==========================================
# CLOUDE AI CONFIGURATION
# ==========================================

APP_NAME = "Cloude AI"
APP_VERSION = "0.2.0"

ROOT_DIR = Path(__file__).resolve().parent

# ==========================================
# CENTRAL DATA DIRECTORY
# ==========================================

DATA_DIR = ROOT_DIR / "DATA"

LANGUAGE_DATA_DIR = DATA_DIR / "language"
KNOWLEDGE_DATA_DIR = DATA_DIR / "knowledge"
TRAINING_DATA_DIR = DATA_DIR / "training"
MEMORY_DATA_DIR = DATA_DIR / "memory"

# ==========================================
# LANGUAGE FILES
# ==========================================

VOCABULARY_FILE = LANGUAGE_DATA_DIR / "vocabulary.json"
GRAMMAR_FILE = LANGUAGE_DATA_DIR / "grammar.json"
SYNONYMS_FILE = LANGUAGE_DATA_DIR / "synonyms.json"
MEANINGS_FILE = LANGUAGE_DATA_DIR / "meanings.json"

# ==========================================
# KNOWLEDGE FILES
# ==========================================

FACTS_FILE = KNOWLEDGE_DATA_DIR / "facts.json"
CONCEPTS_FILE = KNOWLEDGE_DATA_DIR / "concepts.json"
RELATIONSHIPS_FILE = KNOWLEDGE_DATA_DIR / "relationships.json"

# ==========================================
# TRAINING FILES
# ==========================================

SENTENCES_FILE = TRAINING_DATA_DIR / "sentences.json"
EXAMPLES_FILE = TRAINING_DATA_DIR / "examples.json"

# ==========================================
# MEMORY FILES
# ==========================================

CONVERSATIONS_FILE = MEMORY_DATA_DIR / "conversations.json"

# ==========================================
# SYSTEM SETTINGS
# ==========================================

SYSTEM = {
    "offline_mode": True,
    "external_apis": False,
    "external_models": False,
    "debug": True
}

GENERATION = {
    "temperature": 0.85,
    "max_response_length": 1000,
    "repetition_penalty": 1.15
}


# ==========================================
# DIRECTORY INITIALIZATION
# ==========================================

DIRECTORIES = [
    DATA_DIR,
    LANGUAGE_DATA_DIR,
    KNOWLEDGE_DATA_DIR,
    TRAINING_DATA_DIR,
    MEMORY_DATA_DIR
]


def initialize_directories():

    for directory in DIRECTORIES:
        directory.mkdir(
            parents=True,
            exist_ok=True
        )


def validate_configuration():

    assert APP_NAME
    assert APP_VERSION

    assert GENERATION["max_response_length"] > 0

    return True


def initialize():

    initialize_directories()

    validate_configuration()

    return True
