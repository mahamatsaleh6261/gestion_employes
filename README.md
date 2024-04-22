# Cloner le dépôt
git clone <repository_url>
cd <repository_name>

# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
# Sur macOS et Linux :
source venv/bin/activate
# Sur Windows (Command Prompt) :
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Exécuter l'application Flask
flask run
