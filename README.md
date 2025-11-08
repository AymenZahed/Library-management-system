
// exemple :
# Mini-Projet Agile – Gestion de bibliotheque

Ce projet a été réalisé dans le cadre du module **Méthodes de Management Agiles** (Université de Boumerdès). 
L’objectif est de développer une application web en appliquant la méthode **SCRUM** et les pratiques **DevOps**.

---

## Objectifs
- Appliquer la méthode agile **SCRUM** pour gérer le développement.
- Utiliser **GitHub** pour la gestion des versions et la collaboration.
- Mettre en place une **stratégie de branches** efficace.
- Intégrer **SonarQube** pour l’analyse de la qualité du code.
- Configurer des **tests unitaires** et mesurer la **couverture de code**.
- Créer un **pipeline CI/CD** automatisé avec GitHub Actions.

---

## Équipe de développement
| Nom        | Rôle                | 
|------------|---------------------|
| Abdelhafidh| Scrum Master        | 
| Ahmed      | Développeur Backend | 
| Houssem    | Développeur Frontend| 
| Aymen      | Testeur / DevOps    |
| Amine      | Product owner       | 

---

## Technologies utilisées
| Domaine         | Technologies |
|-----------------|--------------|
| Frontend        |  Vue         |
| Backend         | Django       |
| Base de données | MySQL        |
| Tests unitaires | PyTest       |
| Outils DevOps   | GitHub Actions, SonarQube, Jira |

---

## Installation rapide
1. **Cloner le projet**
   ```bash
   git clone https://github.com/Abdelhafidh-87/Library-management-system.git
   cd Library-management-system

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt

3. **Configurer la base de données**
   Créez la base décrite dans le fichier docs/INSTALL.md
   Renseignez vos identifiants dans .env

4. **Lancer le serveur**
   ```bash
   python manage.py runserver



#Arborescence Complète du Projet
Library-Management-System/
│
├── 📁 backend/                              # Tous les microservices backend
│   ├── 📁 api-gateway/                      # Point d’entrée des requêtes API
│   ├── 📁 user-service/                     # Microservice de gestion des utilisateurs
│   ├── 📁 books-service/                    # Microservice de gestion des livres
│   ├── 📁 loans-service/                    # Microservice de gestion des emprunts
│   ├── 📁 notifications-service/            # Microservice de notifications
│   └── 📁 shared/                           # Modules partagés (utils, configs, modèles communs)
│
├── 📁 frontend/                             # Application Vue.js (interface utilisateur)
│
├── 📁 tests/                                # Tests d’intégration et de bout en bout
│
├── 📁 docs/                                 # Documentation (guides, stratégies, rapports)
│
├── 📁 scripts/                              # Scripts utilitaires (déploiement, maintenance)
│
├── 📄 docker-compose.yml                    # Orchestration Docker des microservices
├── 📄 .gitignore                            # Liste des fichiers/dossiers à ignorer par Git
├── 📄 README.md                             # Présentation générale du projet
├── 📄 LICENSE                               # Informations de licence du projet
└── 📄 CONTRIBUTING.md                       # Guide de contribution et conventions d’équipe

#Stratégie de branches Git

Nous appliquons le modèle Git Flow, adapté au développement agile (SCRUM) :

Branche	Rôle
main	Branche principale et stable — contient uniquement le code validé et prêt pour la production.
develop	Branche d’intégration — regroupe toutes les nouvelles fonctionnalités avant livraison.
feature/*	Branche de développement d’une nouvelle fonctionnalité issue de develop.
➡️ Exemple : feature/add-auth-api.
fix/*	Branche pour corriger un bug mineur ou une anomalie non critique.
➡️ Exemple : fix/typo-in-dashboard.
hotfix/*	Branche de correctif d’urgence issue de main pour les bugs critiques en production.
➡️ Exemple : hotfix/fix-login-crash.

# Qualité du code et CI/CD

Chaque push ou pull request déclenche le pipeline GitHub Actions :

Initialisation : vérifie la configuration du projet

Tests unitaires : exécute les tests via le framework choisi

Analyse de qualité : envoie les résultats à SonarQube


# Gestion agile

Méthode : SCRUM

Outil : Jira Software

Backlog initial : 10+ user stories

Nombre de sprints : 4

Sprint 0 : configuration des environnements et outils DevOps


















