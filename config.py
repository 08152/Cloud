
"""
CLOUDE AI
Central Configuration
Version 0.1.0
"""

from pathlib import Path


# ==========================================
# APPLICATION
# ==========================================

APP_NAME = "Cloude AI"
APP_VERSION = "0.1.0"
APP_AUTHOR = "Cloude Development"


# ==========================================
# PROJECT ROOT
# ==========================================

ROOT_DIR = Path(__file__).resolve().parent

CORE_DIR = ROOT_DIR / "core"
LANGUAGE_DIR = ROOT_DIR / "language"
INTELLIGENCE_DIR = ROOT_DIR / "intelligence"
MEMORY_DIR = ROOT_DIR / "memory"
KNOWLEDGE_DIR = ROOT_DIR / "knowledge"
TRAINING_DIR = ROOT_DIR / "training"
STORAGE_DIR = ROOT_DIR / "storage"
TEST_DIR = ROOT_DIR / "tests"


# ==========================================
# LANGUAGE
# ==========================================

DEFAULT_LANGUAGE = "de"

SUPPORTED_LANGUAGES = [
    "de",
    "en"
]


# ==========================================
# RESPONSE GENERATION
# ==========================================

GENERATION = {
    "temperature": 0.85,
    "max_response_length": 1000,
    "repetition_penalty": 1.15,
    "response_variation": True,
    "creative_generation": True
}


# ==========================================
# MEMORY
# ==========================================

MEMORY = {
    "enabled": True,
    "short_term": True,
    "long_term": True,
    "max_history": 100,
    "save_conversations": True
}


# ==========================================
# LANGUAGE PROCESSING
# ==========================================

LANGUAGE_PROCESSING = {
    "tokenization": True,
    "syntax_analysis": True,
    "semantic_analysis": True,
    "grammar_analysis": True,
    "context_analysis": True
}


# ==========================================
# INTELLIGENCE
# ==========================================

INTELLIGENCE = {
    "reasoning": True,
    "planning": True,
    "inference": True,
    "problem_solving": True,
    "learning": False
}


# ==========================================
# SYSTEM
# ==========================================

SYSTEM = {
    "offline_mode": True,
    "external_apis": False,
    "external_models": False,
    "debug": True
}


# ==========================================
# DIRECTORY INITIALIZATION
# ==========================================

DIRECTORIES = [
    CORE_DIR,
    LANGUAGE_DIR,
    INTELLIGENCE_DIR,
    MEMORY_DIR,
    KNOWLEDGE_DIR,
    TRAINING_DIR,
    STORAGE_DIR,
    TEST_DIR
]


def initialize_directories():

    for directory in DIRECTORIES:
        directory.mkdir(
            parents=True,
            exist_ok=True
        )


# ==========================================
# CONFIGURATION VALIDATION
# ==========================================

def validate_configuration():

    assert APP_NAME
    assert APP_VERSION

    assert 0 <= GENERATION["temperature"] <= 2

    assert GENERATION["max_response_length"] > 0

    assert MEMORY["max_history"] > 0

    return True


def initialize():

    initialize_directories()
    validate_configuration()

    return True
