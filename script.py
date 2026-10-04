import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys
import time
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Fonction pour lire le contenu d'un fichier avec encodage UTF-8
def lire_contenu_fichier(fichier):
    try:
        # Ajout de l'encodage utf-8
        with open(fichier, 'r', encoding='utf-8') as file:
            return file.read().strip()  
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {fichier}: {e}")
        return ""

def envoyer_email(smtp_server, smtp_port, login, password, subject, body, recipients):
    try:
        # Configuration de la connexion SMTP en dehors de la boucle
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(login, password)
    except Exception as e:
        print(f"Erreur impossible de se connecter au serveur SMTP : {e}")
        return

    # Création et envoi de l'email
    for index, recipient in enumerate(recipients, start=1):
        try:
            msg = MIMEMultipart()
            msg['From'] = login
            msg['To'] = recipient
            msg['Subject'] = subject

            # Ajouter le corps du message avec encodage utf-8
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # Envoi de l'email
            server.sendmail(login, recipient, msg.as_string())
            print(f"({index}/{len(recipients)}) Email envoyé avec succès à {recipient}")
            
            # Délai pour éviter le blocage anti-spam de Gmail
            time.sleep(2)

        except Exception as e:
            # Si un email échoue, on l'affiche mais on continue la boucle
            print(f"Une erreur est survenue pour l'adresse {recipient} : {e}")

    # Fermeture de la connexion après la boucle
    server.quit()

# Correction du nom du fichier pour correspondre à ta liste
emails = lire_contenu_fichier("communes.txt").splitlines()
body = lire_contenu_fichier("message.txt")

# Paramètres d'envoi
smtp_server = "smtp.gmail.com"
smtp_port = 587
login = "arthurlouette12@gmail.com"
password = os.getenv('SMTP_PASSWORD')

if len(sys.argv) < 2:
    print("Erreur : vous devez fournir l'objet du mail en paramètre.")
    print("Exemple : python3 script.py \"Recherche endroit de camp\"")
    sys.exit(1)
subject = sys.argv[1]

# Envoyer les emails
if emails and body:
    envoyer_email(smtp_server, smtp_port, login, password, subject, body, emails)
else:
    print("Erreur : Liste des emails ou contenu du message vide.")