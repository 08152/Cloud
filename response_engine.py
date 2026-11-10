
import random
import re


class ResponseEngine:

    def __init__(self):
        self.history = []

        self.greetings = [
            "Hallo! Was beschäftigt dich?",
            "Hey! Wie kann ich dir helfen?",
            "Hallo! Worüber möchtest du sprechen?",
            "Schön, dass du da bist. Was gibt es?"
        ]

        self.unknown_answers = [
            "Das ist interessant. Kannst du mir mehr darüber erzählen?",
            "Ich möchte das genauer verstehen. Was meinst du damit?",
            "Darüber würde ich gerne mehr erfahren.",
            "Kannst du deine Frage etwas genauer formulieren?"
        ]

    def generate(self, message):

        message = message.strip()
        lower = message.lower()

        if not message:
            return "Du hast noch keine Nachricht eingegeben."

        self.history.append({
            "user": message
        })

        if re.search(r"\b(hallo|hi|hey|guten tag)\b", lower):
            answer = random.choice(self.greetings)

        elif "wie heißt du" in lower:
            answer = "Ich bin Cloude AI."

        elif "wie geht es dir" in lower:
            answer = "Danke der Nachfrage! Ich bin bereit, dir zu helfen."

        elif "was kannst du" in lower:
            answer = (
                "Ich bin Cloude AI. "
                "Ich kann mit dir kommunizieren und "
                "lerne gerade, immer vielseitiger zu antworten."
            )

        elif "danke" in lower:
            answer = random.choice([
                "Sehr gerne!",
                "Kein Problem!",
                "Gerne! Was möchtest du noch wissen?",
                "Immer gerne!"
            ])

        else:
            answer = random.choice(self.unknown_answers)

        self.history.append({
            "assistant": answer
        })

        return answer
