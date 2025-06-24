# 🍽️ IETC-restaurant_manager

## Description du Projet

Ce projet a été réalisé dans le cadre du cours de Programmation Orientée Objet à l’IETC.
Il s'agit d'une application de gestion de restaurant permettant de :

- gérer les réservations par table

- enregistrer les commandes des clients

- suivre les tickets de caisse par service et par période (jour/mois)

- gérer l’accès aux données selon le rôle (admin, serveur, cuisinier, etc.).

L'application repose sur une architecture modulaire inspirée des principes de la programmation orientée objet ainsi que l'architecture MVC (modèle-vue-contrôleur) afin d’assurer une bonne séparation des différentes parties du code.

## Notre Groupe

- Anas : https://github.com/BrokeAnas
- Hussein : https://github.com/hsx1111
- Otman : https://github.com/otmanbal
- Mickbron : https://github.com/mickbron

## Les fonctionnalités
- Réservation par table : Possibilité de réserver une table en choisissant un créneau horaire (12-14h, 15-17h, 18-20h, 21-23h).

- Gestion des commandes : Sélection de plats à partir du menu et calcul automatique du total de la commande.

- Changement d’état des tables : Une fois la commande validée, la table devient rouge avec le total affiché dessus

- Rotation des services : À la fin du service, la table redevient disponible (verte) pour un nouveau client.

- Vue finance : Regroupement automatique des tickets par jour et par mois. Accessible uniquement pour "l'admin".
  
- Gestion du personnel : Seul l'admin a la possibilité d'ajouter, de supprimer et de modifier le rôle du personnel (CRUD).

- Accès administrateur : L’admin a accès à la vue "finances". Les autres utilisateurs n’ont pas cet accès.

## Technologies et bibliothèques utilisées

Python 3.12.2 : Langage principal utilisé.

PySide (interface graphique) : Pour l’interaction utilisateur.

JSON : Pour la persistance des données.

`collections.defaultdict` : Utilisé pour structurer dynamiquement les données (groupement des commandes, tickets par jour...).

`reportlab` : Utilisé pour générer les tickets de caisse au format PDF via `canvas` et le format `A4`.

## Structure du Projet

```bash
PROJET-POO/
│
├── controllers/          # Logique de contrôle (Finance, Tables)
│   ├── financeController.py
│   └── tableController.py
│
├── database/             # Données persistées en JSON
│   ├── employes.json
│   ├── menu.json
│   ├── orders.json
│   └── reservation.json
│
├── models/               # Classes métiers (FinanceManager, Menu, Reservations...)
│   ├── finance_manager.py
│   ├── menu.py
│   ├── persist.py
│   ├── reservationModel.py
│   └── pdfGenerator.py
│
├── views/                # Interfaces utilisateur
│   ├── adminView.py
│   ├── financeView.py
│   ├── loginView.py
│   ├── mainWindow.py
│   ├── menuView.py
│   ├── orderByDateView.py
│   ├── profileView.py
│   ├── tableDialog.py
│   └── tableView.py
│
├── main.py               # Point d’entrée de l’application
├── README.md             # Fichier de documentation (ce fichier)
├── requirements.txt        
└── .gitignore            # Fichiers/dossiers à ignorer (ex: .idea/)

```

## Installation et Lancement
### Prérequis:
Gestionnaire de paquet : pip
❗ **Important** : Ce projet n’est compatible qu'avec les versions comprises entre 3.13 et 3.9 de python.

### 0. Créer un dossier qui va contenir le projet et accéder à ce dossier dans un terminal de commande

### 1. Dans le terminal, cloner le projet
```bash
git clone https://github.com/otmanbal/IETC-restaurant_manager.git
```
### 2. Accéder au dossier contenant le projet
```bash
#Windows
cd .\IETC-restaurant_manager\

#macOS / Linux
cd IETC-restaurant_manager/
```
### 3. Créer un environnement virtuel
```bash
# Pour Windows, il faut d'abord autoriser les scripts powershell:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Ensuite, créer un environnement sur Windows:
python -m venv env

# macOS / Linux
python3 -m venv env
```
### 4. Activer l'environnement virtuel
```bash
# Windows (PowerShell)
.\env\Scripts\Activate.ps1

# Windows (CMD)
.\env\Scripts\activate.bat

# macOS / Linux
source env/bin/activate
```
### 5. Installer les dépendances
```bash
pip install -r requirements.txt
```
### 6. Lancer l’application
```bash
#Windows
python main.py

#macOS / Linux
python3 main.py
```
