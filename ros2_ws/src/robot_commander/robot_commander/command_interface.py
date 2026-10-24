import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class CommandInterface(Node):

    def __init__(self):
        super().__init__('command_interface')

        self.publisher = self.create_publisher(
            String,
            '/robot_command',
            10
        )

        # Permet de recevoir l'état du robot
        self.state_subscription = self.create_subscription(
            String,
            '/robot_state',
            self.state_callback,
            10
        )

        self.get_logger().info('========================================')
        self.get_logger().info('       ROBOT COMMANDER - INTERFACE')
        self.get_logger().info('========================================')
        self.get_logger().info('Tape une commande en français.')
        self.get_logger().info('Exemples :')
        self.get_logger().info('  Va dans la cuisine')
        self.get_logger().info('  Attrape le téléphone')
        self.get_logger().info('  Arrête-toi')
        self.get_logger().info('  Quel est ton état ?')
        self.get_logger().info('Tape "quit" pour quitter.')
        self.get_logger().info('========================================')

        self.last_state = None

    def state_callback(self, msg):
        self.last_state = msg.data

    def send_command(self, command):

        msg = String()
        msg.data = command

        self.publisher.publish(msg)

        self.get_logger().info(
            f'Commande envoyée : {command}'
        )

    def show_state(self):

        if self.last_state is not None:
            self.get_logger().info(
                f'🤖 État du robot > {self.last_state}'
            )
        else:
            self.get_logger().info(
                '🤖 État du robot > État indisponible'
            )


def main(args=None):

    rclpy.init(args=args)

    node = CommandInterface()

    try:

        while rclpy.ok():

            # Traiter les messages ROS avant de demander une commande
            rclpy.spin_once(node, timeout_sec=0.1)

            command = input("\n🤖 Commande > ").strip()

            if command.lower() == "quit":
                break

            if command == "":
                continue

            # Commande spéciale pour demander l'état
            if command.lower() in [
                "quel est ton état ?",
                "quel est ton état",
                "etat",
                "état"
            ]:
                node.show_state()
                continue

            # Envoyer la commande
            node.send_command(command)

            # IMPORTANT :
            # laisser ROS traiter immédiatement le publish
            for _ in range(5):
                rclpy.spin_once(node, timeout_sec=0.05)

    except KeyboardInterrupt:
        pass

    finally:

        node.get_logger().info(
            'Arrêt de l interface...'
        )

        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()