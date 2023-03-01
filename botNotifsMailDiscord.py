# Importer les librairies
import discord
from discord.ext import commands
import sqlalchemy
import smtplib

# Créer une instance de la classe Bot
bot = commands.Bot(command_prefix="!")

# Créer une connexion avec la base de données PostgreSQL
engine = sqlalchemy.create_engine("postgresql://user:password@host/database")
metadata = sqlalchemy.MetaData()
# Créer une table pour stocker les adresses mail des utilisateurs
mail_table = sqlalchemy.Table("mail", metadata,
    sqlalchemy.Column("user_id", sqlalchemy.BigInteger, primary_key=True),
    sqlalchemy.Column("mail_address", sqlalchemy.String)
)
metadata.create_all(engine)

# Définir les paramètres du serveur SMTP
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "votre_email@gmail.com"
sender_password = "votre_mot_de_passe"

# Définir une commande pour envoyer un mail à une adresse spécifiée
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

# Définir une commande pour que les utilisateurs puissent entrer leur adresse mail et la lier à leur identifiant discord 
@bot.command()
async def setmail(ctx, mail_address):
    # Vérifier si l'adresse mail est valide 
    if "@" in mail_address:
        # Récupérer l'identifiant de l'utilisateur 
        user_id = ctx.author.id 
        # Insérer ou mettre à jour l'adresse mail dans la table 
        with engine.connect() as conn:
            stmt = mail_table.insert().values(user_id=user_id, mail_address=mail_address) 
            conn.execute(stmt) 
        # Envoyer un message de confirmation dans le chat discord 
        await ctx.send(f"Votre adresse mail a été enregistrée.") 
    else: 
        # Envoyer un message d'erreur dans le chat discord 
        await ctx.send(f"Votre adresse mail n'est pas valide.")

# Définir une commande pour que les utilisateurs puissent récupérer l'adresse mail d'un autre utilisateur 
@bot.command() 
async def getmail(ctx, user_id): 
     # Vérifier si l'identifiant est valide  
     if user_id.isdigit():  
         # Convertir l'identifiant en entier  
         user_id = int(user_id)  
         # Interroger la base de données pour trouver l'adresse mail correspondante  
         with engine.connect() as conn:  
             stmt = mail_table.select().where(mail_table.c.user_id == user_id)  
             result = conn.execute(stmt).fetchone()  
         # Vérifier si le résultat existe  
         if result:  
             # Récupérer l'adresse mail  
             mail_address = result["mail_address"]  
             # Envoyer un message avec l'adresse mail dans le chat discord  
             await ctx.send(f"L'adresse mail de l'utilisateur {user_id} est {mail_address}.")  
         else:  
             # Envoyer un message d'erreur dans le chat discord  
             await ctx.send(f"L'utilisateur {user_id} n'a pas enregistré son adresse mail.")   
     else:   
         # Envoyer un message d'erreur dans le chat discord   
         await ctx.send(f"L'identifiant n'est pas valide.")

# Récupérer le token du bot sur le portail développeur discord et le passer à la méthode run 
bot.run("votre_token")