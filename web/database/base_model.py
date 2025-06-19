##
# @file base_model.py
# @brief Définit les modèles de données utilisés par l’API avec Pydantic.
#
# Ces classes structurent les échanges entre client et serveur :
# - Initialisation : configuration initiale d’un robot
# - REF : modèle représentant un robot
# - Telemetry : données envoyées par le robot en temps réel
# - Summary : fin de mission
# - Instruction : mission à réaliser
# - Message : utilisé uniquement pour les tests

from pydantic import BaseModel

##
# @class Initialisation
# @brief Modèle pour les données d'initialisation d'un robot.
class Initialisation(BaseModel):
    ref_id: str              ## Identifiant du robot
    position: int            ## Position initiale du robot
    has_box: bool            ## Présence d’une boîte au démarrage

##
# @class REF
# @brief Modèle représentant un robot dans la base.
class REF(BaseModel):
    name: str                ## Nom du robot
    id: str                  ## Identifiant unique du robot

##
# @class Telemetry
# @brief Données de télémétrie transmises par le robot.
class Telemetry(BaseModel):
    robot_id: str = None             ## Identifiant du robot
    vitesse_instant: float = None    ## Vitesse mesurée
    ds_ultrasons: float = None       ## Distance mesurée par ultrason
    statut_deplacement: str = None   ## État actuel du déplacement
    ligne: int = None                ## Ligne détectée (si applicable)
    statut_pince: bool = None        ## État de la pince (ouverte/fermée)

##
# @class Summary
# @brief Résumé envoyé à la fin d'une mission.
class Summary(BaseModel):
    robot_id: str = None             ## Identifiant du robot ayant terminé une mission

##
# @class Instruction
# @brief Mission assignée à un robot (liste de blocs à collecter).
class Instruction(BaseModel):
    robot_id: str            ## Identifiant du robot
    blocks: list[int]        ## Blocs à récupérer
    status: str              ## Statut de la mission

##
# @class Message
# @brief Modèle de message utilisé uniquement pour les tests.
#
# Ce modèle est utilisé pour simuler ou vérifier le bon fonctionnement des échanges.
class Message(BaseModel):
    ref_id: str              ## Identifiant du robot concerné
    contenu: str             ## Message de test
