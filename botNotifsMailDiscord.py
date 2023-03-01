# Importer les librairies
import discord
from discord.ext import commands
import smtplib

# Créer une instance de la classe Bot
bot = commands.Bot(command_prefix="!")

# Définir les paramètres du serveur SMTP
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "votre_email@gmail.com"
sender_password = "votre_mot_de_passe"

# Définir une commande pour envoyer un mail
@bot.command()
async def mail(ctx, recipient_email, subject, message):
    # Créer une connexion sécurisée avec le serveur SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    # Se connecter au compte email de l'expéditeur
    server.login(sender_email, sender_password)
    # Créer le contenu du mail
    mail_content = f"Subject: {subject}\n\n{message}"
    # Envoyer le mail au destinataire
    server.sendmail(sender_email, recipient_email, mail_content)
    # Fermer la connexion avec le serveur SMTP
    server.quit()
    # Envoyer un message de confirmation dans le chat discord
    await ctx.send(f"Mail envoyé à {recipient_email}.")

# Récupérer le token du bot sur le portail développeur discord et le passer à la méthode run 
bot.run("votre_token")