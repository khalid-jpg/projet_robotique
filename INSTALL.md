# Guide d'installation — NLP Robot Commander

Ce fichier explique comment installer et lancer le projet `nlp_robot_commander` sur un nouveau PC.

## 1. Prérequis

Le projet utilise :

- Ubuntu 24.04 LTS
- Python 3
- Git
- ROS 2 Jazzy
- Ollama
- Qwen 2.5 3B
- Python package `ollama`
- `pytest`

> Si le PC utilise Windows, le plus simple est d'utiliser Ubuntu 24.04 avec WSL2.

---

## 2. Installer Git et Python

Dans Ubuntu :

```bash
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv
```

Vérifier :

```bash
git --version
python3 --version
```

---

## 3. Installer ROS 2 Jazzy

Installer ROS 2 Jazzy en suivant la documentation officielle :

https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html

Après l'installation :

```bash
source /opt/ros/jazzy/setup.bash
```

Pour charger ROS 2 automatiquement à chaque ouverture du terminal :

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

Vérifier :

```bash
ros2 --version
```

---

## 4. Installer Ollama

Installer Ollama :

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Vérifier :

```bash
ollama --version
```

Puis télécharger le modèle utilisé par le projet :

```bash
ollama pull qwen2.5:3b
```

Tester :

```bash
ollama run qwen2.5:3b
```

Pour quitter le modèle :

```text
/bye
```

---

## 5. Télécharger le projet GitHub

Cloner le projet :

```bash
git clone https://github.com/khalid-jpg/projet_robotique.git
```

Entrer dans le projet :

```bash
cd projet_robotique
```

---

## 6. Créer l'environnement Python

Créer l'environnement virtuel :

```bash
python3 -m venv .venv
```

Activer l'environnement :

```bash
source .venv/bin/activate
```

Installer les dépendances :

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 7. Compiler le workspace ROS 2

Entrer dans le workspace :

```bash
cd ros2_ws
```

Compiler :

```bash
colcon build --packages-select robot_commander
```

Charger le workspace :

```bash
source install/setup.bash
```

Pour charger automatiquement le workspace :

```bash
echo "source ~/projet_robotique/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

## 8. Tester le projet

Ouvrir trois terminaux Ubuntu.

### Terminal 1 — LLM Listener

```bash
cd ~/projet_robotique
source .venv/bin/activate
source /opt/ros/jazzy/setup.bash
source ros2_ws/install/setup.bash
ros2 run robot_commander command_listener
```

Le terminal doit afficher quelque chose comme :

```text
LLM Command Listener prêt !
```

### Terminal 2 — Robot Controller

```bash
cd ~/projet_robotique
source /opt/ros/jazzy/setup.bash
source ros2_ws/install/setup.bash
ros2 run robot_commander robot_controller
```

### Terminal 3 — Interface utilisateur

```bash
cd ~/projet_robotique
source /opt/ros/jazzy/setup.bash
source ros2_ws/install/setup.bash
ros2 run robot_commander command_interface
```

---

## 9. Tester une commande

Dans le terminal de l'interface :

```text
Va dans la cuisine
```

Puis :

```text
Attrape le téléphone
```

Puis :

```text
Quel est ton état ?
```

Autres exemples :

```text
Va dans le bureau
```

```text
Arrête-toi
```

Pour quitter :

```text
quit
```

---

## 10. Lancer les tests Python

Depuis la racine du projet :

```bash
cd ~/projet_robotique
source .venv/bin/activate
pytest
```

---

## 11. Après avoir récupéré une nouvelle version du projet

Si un membre du groupe a ajouté du code :

```bash
cd ~/projet_robotique
git pull
```

Si de nouvelles dépendances Python ont été ajoutées :

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Si le code ROS 2 a changé :

```bash
cd ros2_ws
colcon build --packages-select robot_commander
source install/setup.bash
```

---

## 12. Pour travailler sur le projet

Avant de commencer :

```bash
cd ~/projet_robotique
git pull
```

Créer une branche personnelle :

```bash
git checkout -b feature/ma-partie
```

Après les modifications :

```bash
git add .
git commit -m "Description de la modification"
git push -u origin feature/ma-partie
```

Ensuite, créer une Pull Request sur GitHub vers `main`.

---

## Architecture du projet

```text
projet_robotique/
│
├── dataset/
│   └── commands.csv
│
├── llm_commander/
│   ├── config.py
│   ├── llm_parser.py
│   └── prompt.py
│
├── ros2_ws/
│   └── src/
│       └── robot_commander/
│           ├── launch/
│           ├── robot_commander/
│           │   ├── command_interface.py
│           │   ├── command_listener.py
│           │   └── robot_controller.py
│           ├── package.xml
│           ├── setup.py
│           └── setup.cfg
│
├── tests/
│   └── test_dataset.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Technologies utilisées

- Python
- Ollama
- Qwen 2.5 3B
- ROS 2 Jazzy
- ROS 2 topics
- Git / GitHub
- pytest

## Dépannage rapide

### `ros2: command not found`

```bash
source /opt/ros/jazzy/setup.bash
```

### `ros2 run robot_commander ...` ne trouve pas le package

```bash
cd ~/projet_robotique/ros2_ws
colcon build --packages-select robot_commander
source install/setup.bash
```

### Ollama ne trouve pas le modèle

```bash
ollama pull qwen2.5:3b
```

### Python ne trouve pas `ollama`

```bash
cd ~/projet_robotique
source .venv/bin/activate
pip install -r requirements.txt
```

### Après un `git pull`, le projet ne fonctionne plus

Recompiler ROS 2 :

```bash
cd ~/projet_robotique/ros2_ws
colcon build --packages-select robot_commander
source install/setup.bash
```

Puis réinstaller les dépendances :

```bash
cd ~/projet_robotique
source .venv/bin/activate
pip install -r requirements.txt
```
