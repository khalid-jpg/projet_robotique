import csv
import json
import ollama


# ==============================
# CONFIGURATION
# ==============================

MODEL = "qwen2.5:3b"

# Nombre maximum de commandes à tester
# Mets 10 pour un test rapide
# Mets 80 pour tester tout le dataset
MAX_TESTS = 80


# ==============================
# PROMPT DU LLM
# ==============================

SYSTEM_PROMPT = """
Tu es le module NLP d'un robot mobile.

Ta tâche est de transformer une commande utilisateur en JSON.

Les seules intentions autorisées sont :

1. navigate
   Déplacer le robot vers une destination.
   Utilise le champ "target".

2. stop
   Arrêter immédiatement le robot.
   Aucun paramètre supplémentaire.

3. pick
   Prendre ou ramasser un objet.
   Utilise le champ "object".

4. report
   Donner l'état ou le statut du robot.
   Aucun paramètre supplémentaire.

==================================================
RÈGLES DE NORMALISATION OBLIGATOIRES
==================================================

Pour les destinations :

cuisine = kitchen
salon = living_room
chambre = bedroom
salle de bain = bathroom
bureau = office

IMPORTANT :
"bureau" signifie TOUJOURS "office".
Ne jamais interpréter "bureau" comme "bathroom".

Pour les objets :

téléphone = phone
telephone = phone
portable = phone

stylo = pen
stylo à bille = pen
crayon = pencil
bouteille = bottle

IMPORTANT :
"stylo" signifie TOUJOURS "pen".
Ne jamais utiliser "stenographer" pour "stylo".

==================================================
FORMAT DE SORTIE
==================================================

Réponds UNIQUEMENT avec un JSON valide.

Ne donne aucune explication.
Ne donne aucun texte avant ou après le JSON.
N'utilise pas Markdown.

==================================================
EXEMPLES
==================================================

Commande : Va dans la cuisine
Réponse :
{"intent":"navigate","target":"kitchen"}

Commande : Va dans le salon
Réponse :
{"intent":"navigate","target":"living_room"}

Commande : Va dans la chambre
Réponse :
{"intent":"navigate","target":"bedroom"}

Commande : Va dans la salle de bain
Réponse :
{"intent":"navigate","target":"bathroom"}

Commande : Va dans le bureau
Réponse :
{"intent":"navigate","target":"office"}

Commande : Positionne-toi dans le bureau
Réponse :
{"intent":"navigate","target":"office"}

Commande : Arrête le robot
Réponse :
{"intent":"stop"}

Commande : Stoppe le robot
Réponse :
{"intent":"stop"}

Commande : Prends le téléphone
Réponse :
{"intent":"pick","object":"phone"}

Commande : Attrape le téléphone
Réponse :
{"intent":"pick","object":"phone"}

Commande : Prends le stylo
Réponse :
{"intent":"pick","object":"pen"}

Commande : Ramasse le stylo
Réponse :
{"intent":"pick","object":"pen"}

Commande : Prends la bouteille
Réponse :
{"intent":"pick","object":"bottle"}

Commande : Quel est ton état ?
Réponse :
{"intent":"report"}

Commande : Donne-moi ton état
Réponse :
{"intent":"report"}
"""


# ==============================
# APPEL OLLAMA
# ==============================

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
        ],
        options={
            "temperature": 0,
            "num_predict": 64
        },
        keep_alive="10m"
    )

    content = response["message"]["content"].strip()

    try:
        return json.loads(content)

    except json.JSONDecodeError:

        # Tentative de récupération si le modèle
        # ajoute accidentellement du texte autour du JSON
        start = content.find("{")
        end = content.rfind("}")

        if start != -1 and end != -1:
            try:
                return json.loads(content[start:end + 1])
            except json.JSONDecodeError:
                pass

        return None


# ==============================
# VALIDATION
# ==============================

def check_result(result, expected_intent, expected_parameter):

    if result is None:
        return False

    # Vérification de l'intention
    if result.get("intent") != expected_intent:
        return False

    # STOP et REPORT
    if expected_intent in ["stop", "report"]:
        return True

    # NAVIGATE
    if expected_intent == "navigate":

        return result.get("target") == expected_parameter

    # PICK
    if expected_intent == "pick":

        return result.get("object") == expected_parameter

    return False


# ==============================
# TEST DU DATASET
# ==============================

def main():

    total = 0
    correct = 0
    errors = []

    print("\n======================================")
    print("   TEST DU DATASET - LLM COMMANDER")
    print("======================================")
    print(f"Modèle : {MODEL}")
    print(f"Nombre maximum de tests : {MAX_TESTS}")
    print("======================================\n")

    try:

        with open(
            "dataset/commands.csv",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for index, row in enumerate(reader):

                # Limite du nombre de tests
                if index >= MAX_TESTS:
                    break

                total += 1

                command = row["text"]
                expected_intent = row["intent"]
                expected_parameter = row["parameter"]

                print(
                    f"[{total}/{MAX_TESTS}] "
                    f"{command}"
                )

                result = parse_command(command)

                success = check_result(
                    result,
                    expected_intent,
                    expected_parameter
                )

                if success:

                    correct += 1

                    print("    ✅ Correct")

                else:

                    print("    ❌ Erreur")

                    errors.append({
                        "command": command,
                        "expected_intent": expected_intent,
                        "expected_parameter": expected_parameter,
                        "result": result
                    })

                print()

    except FileNotFoundError:

        print("❌ Erreur : dataset/commands.csv introuvable.")
        return

    except Exception as error:

        print("❌ Erreur pendant le test :")
        print(error)
        return

    # ==============================
    # RESULTATS
    # ==============================

    if total == 0:

        print("Aucune commande testée.")
        return

    accuracy = (correct / total) * 100

    print("\n======================================")
    print("              RÉSULTATS")
    print("======================================")

    print(f"Commandes testées  : {total}")
    print(f"Commandes correctes: {correct}")
    print(f"Erreurs            : {len(errors)}")
    print(f"Accuracy           : {accuracy:.2f}%")

    print("======================================")

    # ==============================
    # AFFICHAGE DES ERREURS
    # ==============================

    if errors:

        print("\n======================================")
        print("          ERREURS DÉTECTÉES")
        print("======================================")

        for i, error in enumerate(errors, 1):

            print(f"\nErreur {i}")
            print("--------------------------------------")

            print(
                f"Commande : "
                f"{error['command']}"
            )

            print(
                f"Attendu  : "
                f"intent={error['expected_intent']}, "
                f"parameter={error['expected_parameter']}"
            )

            print(
                f"Obtenu   : "
                f"{error['result']}"
            )

    else:

        print("\n🎉 Aucune erreur détectée !")


# ==============================
# PROGRAMME PRINCIPAL
# ==============================

if __name__ == "__main__":
    main()