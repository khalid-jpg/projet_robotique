import json
import urllib.request

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"


SYSTEM_PROMPT = """
Tu es un parseur de commandes pour un robot.

Transforme chaque commande française en JSON STRICT.

Les intents possibles sont uniquement :

1. navigate
{"intent": "navigate", "target": "..."}

2. pick
{"intent": "pick", "object": "..."}

3. stop
{"intent": "stop"}

4. report
{"intent": "report"}

Normalisation des destinations :
- cuisine -> kitchen
- salon -> living_room
- chambre -> bedroom
- salle de bain -> bathroom
- bureau -> office

Normalisation des objets :
- téléphone -> phone
- telephone -> phone
- portable -> phone
- stylo -> pen
- stylo à bille -> pen
- crayon -> pencil
- bouteille -> bottle

IMPORTANT :
- bureau = office
- stylo = pen

Exemples :

"Va dans la cuisine"
{"intent":"navigate","target":"kitchen"}

"Positionne-toi dans le bureau"
{"intent":"navigate","target":"office"}

"Attrape le téléphone"
{"intent":"pick","object":"phone"}

"Prends le stylo"
{"intent":"pick","object":"pen"}

"Arrête-toi"
{"intent":"stop"}

"Quel est ton état ?"
{"intent":"report"}

Réponds UNIQUEMENT avec le JSON.
"""


class CommandListener(Node):

    def __init__(self):
        super().__init__('command_listener')

        self.subscription = self.create_subscription(
            String,
            '/robot_command',
            self.command_callback,
            10
        )

        self.publisher = self.create_publisher(
            String,
            '/parsed_command',
            10
        )

        self.get_logger().info(
            'LLM Command Listener prêt !'
        )

    def command_callback(self, msg):

        command = msg.data

        self.get_logger().info(
            f'Commande reçue : {command}'
        )

        try:

            result = self.ask_ollama(command)

            json_command = json.dumps(
                result,
                ensure_ascii=False
            )

            self.get_logger().info(
                f'Commande structurée : {json_command}'
            )

            output = String()
            output.data = json_command

            self.publisher.publish(output)

            self.get_logger().info(
                'Commande publiée sur /parsed_command'
            )

        except Exception as e:

            self.get_logger().error(
                f'Erreur LLM : {e}'
            )

    def ask_ollama(self, command):

        prompt = (
            SYSTEM_PROMPT
            + "\nCommande utilisateur : "
            + command
        )

        data = {
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0,
                "num_predict": 64
            },
            "keep_alive": "10m"
        }

        request = urllib.request.Request(
            OLLAMA_URL,
            data=json.dumps(data).encode("utf-8"),
            headers={
                "Content-Type": "application/json"
            },
            method="POST"
        )

        with urllib.request.urlopen(
            request,
            timeout=120
        ) as response:

            response_data = json.loads(
                response.read().decode("utf-8")
            )

        llm_response = response_data["response"]

        return json.loads(llm_response)


def main(args=None):

    rclpy.init(args=args)

    node = CommandListener()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()