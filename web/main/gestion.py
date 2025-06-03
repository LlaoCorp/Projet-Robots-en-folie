from database.init_db import ajouter_message, recuperer_messages

def enregistrer_message(msg):
    ajouter_message(msg.ref_id, msg.contenu)

def lire_messages():
    return recuperer_messages()
