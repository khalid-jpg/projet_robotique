import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class RobotController(Node):

    def __init__(self):
        super().__init__('robot_controller')

        # ==========================================
        # SUBSCRIBER : reçoit les commandes structurées
        # ==========================================
        self.subscription = self.create_subscription(
            String,
            '/parsed_command',
            self.command_callback,
            10
        )

        # ==========================================
        # PUBLISHER : publie l'état du robot
        # ==========================================
        self.state_publisher = self.create_publisher(
            String,
            '/robot_state',
            10
        )

        # ==========================================
        # ÉTAT INTERNE DU ROBOT
        # ==========================================
        self.position = "unknown"
        self.held_object = None
        self.status = "idle"

        self.get_logger().info(
            'Robot Controller prêt !'
        )

        self.get_logger().info(
            'État initial : position=unknown, '
            'objet=None, statut=idle'
        )

        # Publier l'état initial
        self.publish_state()

    # ==========================================
    # TRAITEMENT DES COMMANDES
    # ==========================================
    def command_callback(self, msg):

        try:
            command = json.loads(msg.data)

            intent = command.get('intent')

            self.get_logger().info(
                f'Commande reçue : {command}'
            )

            # ==================================
            # NAVIGATION
            # ==================================
            if intent == 'navigate':

                target = command.get('target')

                self.status = "moving"

                self.get_logger().info(
                    f'ROBOT -> Navigation vers {target}'
                )

                # Simulation de l'arrivée
                self.position = target
                self.status = "idle"

                self.get_logger().info(
                    f'ROBOT -> Arrivé à {self.position}'
                )

                self.publish_state()

            # ==================================
            # PICK
            # ==================================
            elif intent == 'pick':

                obj = command.get('object')

                self.held_object = obj
                self.status = "holding"

                self.get_logger().info(
                    f'ROBOT -> Prise de {obj}'
                )

                self.get_logger().info(
                    f'ROBOT -> Objet tenu : {self.held_object}'
                )

                self.publish_state()

            # ==================================
            # STOP
            # ==================================
            elif intent == 'stop':

                self.status = "stopped"

                self.get_logger().warn(
                    'ROBOT -> ARRÊT'
                )

                self.publish_state()

            # ==================================
            # REPORT
            # ==================================
            elif intent == 'report':

                self.print_robot_state()

            # ==================================
            # INTENT INCONNU
            # ==================================
            else:

                self.get_logger().error(
                    f'Intent inconnu : {intent}'
                )

        except json.JSONDecodeError:

            self.get_logger().error(
                f'JSON invalide : {msg.data}'
            )

    # ==========================================
    # PUBLICATION DE L'ÉTAT
    # ==========================================
    def publish_state(self):

        state = {
            "position": self.position,
            "held_object": self.held_object,
            "status": self.status
        }

        msg = String()

        msg.data = json.dumps(
            state,
            ensure_ascii=False
        )

        self.state_publisher.publish(msg)

        self.get_logger().info(
            f'ÉTAT publié sur /robot_state : {msg.data}'
        )

    # ==========================================
    # AFFICHAGE DE L'ÉTAT
    # ==========================================
    def print_robot_state(self):

        state = {
            "position": self.position,
            "held_object": self.held_object,
            "status": self.status
        }

        self.get_logger().info(
            '===== ÉTAT DU ROBOT ====='
        )

        self.get_logger().info(
            f'Position     : {self.position}'
        )

        self.get_logger().info(
            f'Objet tenu   : {self.held_object}'
        )

        self.get_logger().info(
            f'Statut       : {self.status}'
        )

        self.get_logger().info(
            f'JSON état    : {json.dumps(state, ensure_ascii=False)}'
        )

        self.get_logger().info(
            '========================='
        )


def main(args=None):

    rclpy.init(args=args)

    node = RobotController()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()