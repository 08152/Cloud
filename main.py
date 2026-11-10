
from pathlib import Path
from llama_cpp import Llama

# =====================================
# CLOUDE AI - Hauptprogramm
# =====================================

APP_NAME = "Cloude AI"
MODEL_PATH = Path("models/model.gguf")

# KI-Einstellungen
MAX_TOKENS = 512
CONTEXT_SIZE = 4096

# Gesprächsverlauf
conversation_history = []


def load_model():
    """Lädt das lokale KI-Modell."""

    if not MODEL_PATH.exists():
        print(f"Modell nicht gefunden: {MODEL_PATH}")
        print("Bitte lege dein GGUF-Modell im Ordner models ab.")
        return None

    print(f"{APP_NAME} wird gestartet...")

    try:
        model = Llama(
            model_path=str(MODEL_PATH),
            n_ctx=CONTEXT_SIZE,
            verbose=False
        )

        print(f"{APP_NAME} ist bereit!")
        return model

    except Exception as error:
        print(f"Fehler beim Laden: {error}")
        return None


def generate_answer(model, user_message):
    """Generiert eine neue Antwort."""

    conversation_history.append(
        f"Benutzer: {user_message}"
    )

    prompt = (
        "Du bist Cloude AI, ein hilfreicher, "
        "kreativer und selbstständig formulierender "
        "KI-Assistent. Antworte auf Deutsch, "
        "natürlich und abwechslungsreich.\n\n"
        + "\n".join(conversation_history[-10:])
        + "\nCloude AI:"
    )

    response = model(
        prompt,
        max_tokens=MAX_TOKENS,
        temperature=0.8,
        repeat_penalty=1.15,
        stop=["Benutzer:", "\n\nBenutzer:"]
    )

    answer = response["choices"][0]["text"].strip()

    conversation_history.append(
        f"Cloude AI: {answer}"
    )

    return answer


def main():
    print("============================")
    print("       CLOUDE AI")
    print("============================")

    model = load_model()

    if model is None:
        return

    while True:
        user_input = input("\nDu: ").strip()

        if user_input.lower() in ["exit", "quit", "stop"]:
            print("Cloude AI wird beendet.")
            break

        if not user_input:
            continue

        try:
            answer = generate_answer(model, user_input)
            print(f"\nCloude AI: {answer}")

        except Exception as error:
            print(f"Fehler: {error}")


if __name__ == "__main__":
    main()
