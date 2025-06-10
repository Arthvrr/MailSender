import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Fonction pour lire le contenu d'un fichier
def lire_contenu_fichier(fichier):
    try:
        with open(fichier, 'r') as file:
            return file.read().strip()  # Retourne le contenu sans espaces superflus
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {fichier}: {e}")
        return ""

# Fonction pour envoyer un email
def envoyer_email(smtp_server, smtp_port, login, password, subject, body, recipients):
    try:
        # Configuration du serveur SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Sécurise la connexion
        server.login(login, password)

        # Création de l'email
        for index, recipient in enumerate(recipients, start=1):
            msg = MIMEMultipart()
            msg['From'] = login
            msg['To'] = recipient
            msg['Subject'] = subject

            # Ajouter le corps du message
            msg.attach(MIMEText(body, 'plain'))

            # Envoi de l'email
            server.sendmail(login, recipient, msg.as_string())
            print(f"({index}/{len(recipients)}) Email envoyé avec succès à {recipient}")

        # Fermeture de la connexion
        server.quit()
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

# Charger les emails et le message
emails = lire_contenu_fichier("emails.txt").splitlines()
body = lire_contenu_fichier("message.txt")

# Paramètres d'envoi
smtp_server = "smtp.gmail.com"  #Serveur SMTP de Gmail
smtp_port = 587  #Port SMTP
login = "arthurlouette12@gmail.com"
password = os.getenv('SMTP_PASSWORD')
subject = "Recherche d'endroit pour un camp baladin juillet 2026" #Objet de l'email

# Envoyer les emails
if emails and body:
    envoyer_email(smtp_server, smtp_port, login, password, subject, body, emails)
else:
    print("Erreur : Liste des emails ou contenu du message vide.")