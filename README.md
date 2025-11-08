
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
│   ├── 📁 api-gateway/                      # API Gateway
│   ├── 📁 user-service/                     # Microservice Users
│   ├── 📁 books-service/                    # Microservice Books
│   ├── 📁 loans-service/                    # Microservice Loans
│   ├── 📁 notifications-service/            # Microservice Notifications
│   └── 📁 shared/                           # Code partagé (utils, configs)
├── 📁 frontend/                             # Application Vue.js
├── 📁 tests/                                # Tests d'intégration globaux
├── 📁 docs/                                 # Documentation du projet
├── 📁 scripts/                              # Scripts utilitaires
├── 📄 docker-compose.yml                    # Configuration Docker Compose
├── 📄 .gitignore                            # Fichiers à ignorer par Git
├── 📄 README.md                             # Documentation principale
├── 📄 LICENSE                               # Licence du projet
└── 📄 CONTRIBUTING.md                       # Guide de contribution


# Stratégie de branches
Nous suivons le modèle Git Flow :

main             ← toujours stable (prête pour la production)
│
├── develop      ← branche d’intégration de toutes les nouvelles fonctionnalités
│
├── feature/...  ← chaque nouvelle fonctionnalité (créée par les développeurs)
│
├── fix/...      ← corrections de bogues
│
└── hotfix/...   ← correctifs urgents en production


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


















