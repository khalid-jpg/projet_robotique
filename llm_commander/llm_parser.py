import json
import ollama


MODEL = "qwen2.5:3b"


SYSTEM_PROMPT = """
Tu es le module NLP d'un robot mobile.

Ta tâche est de transformer une commande utilisateur en JSON.

Les seules intentions autorisées sont :

- navigate : déplacer le robot vers une destination
- stop : arrêter le robot
- pick : prendre un objet
- report : donner l'état du robot

Pour navigate, utilise le champ "target".
Pour pick, utilise le champ "object".
Pour stop et report, aucun paramètre supplémentaire n'est nécessaire.

Tu dois répondre UNIQUEMENT avec un JSON valide.
Tu ne dois donner aucune explication.

Exemples :

Commande : Va dans la cuisine
Réponse :
{"intent":"navigate","target":"kitchen"}

Commande : Arrête le robot
Réponse :
{"intent":"stop"}

Commande : Prends la bouteille
Réponse :
{"intent":"pick","object":"bottle"}

Commande : Quel est ton état ?
Réponse :
{"intent":"report"}
"""


def parse_command(command):
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": command
            }
        ]
    )

    content = response["message"]["content"]

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "error": "LLM did not return valid JSON",
            "raw_response": content
        }


if __name__ == "__main__":
    command = input("Commande du robot : ")

    result = parse_command(command)

    print("\nRésultat :")
    print(json.dumps(result, indent=2, ensure_ascii=False))
