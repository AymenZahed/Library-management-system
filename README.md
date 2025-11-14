#Library Management System

Système de gestion de bibliothèque avec architecture microservices (Django + Vue.js)

##Objectifs

Ce projet a été réalisé dans le cadre du module **Méthodes de Management Agiles** (Université de Boumerdès). 
L'objectif est de développer une application web en appliquant la méthode **SCRUM** et les pratiques **DevOps** :

- Appliquer la méthode agile **SCRUM** pour gérer le développement
- Utiliser **GitHub** pour la gestion des versions et la collaboration
- Mettre en place une **stratégie de branches** efficace
- Intégrer **SonarQube** pour l'analyse de la qualité du code
- Configurer des **tests unitaires** et mesurer la **couverture de code**
- Créer un **pipeline CI/CD** automatisé avec GitHub Actions

##Équipe de développement

| Nom | Rôle |
|-----|------|
| Abdelhafidh | Scrum Master |
| Ahmed | Développeur Backend |
| Houssem | Développeur Frontend |
| Aymen | Testeur / DevOps |
| Amine | Product Owner |

##Architecture

- **Backend**: Django + Microservices
- **Frontend**: Vue.js 
- **Base de données**: MySQL
- **CI/CD**: GitHub Actions + SonarQube
- **Gestion de projet**: Jira Software

###Arborescence du Projet

```
Library-Management-System/
│
├── 📁 backend/                              # Tous les microservices backend
│   ├── 📁 api-gateway/                      # Point d'entrée des requêtes API
│   ├── 📁 user-service/                     # Microservice de gestion des utilisateurs
│   ├── 📁 books-service/                    # Microservice de gestion des livres
│   ├── 📁 loans-service/                    # Microservice de gestion des emprunts
│   ├── 📁 notifications-service/            # Microservice de notifications
│   └── 📁 shared/                           # Modules partagés (utils, configs, modèles communs)
│
├── 📁 frontend/                             # Application Vue.js (interface utilisateur)
│
├── 📁 tests/                                # Tests d'intégration et de bout en bout
│
├── 📁 docs/                                 # Documentation (guides, stratégies, rapports)
│
├── 📁 scripts/                              # Scripts utilitaires (déploiement, maintenance)
│
├── 📄 docker-compose.yml                    # Orchestration Docker des microservices
├── 📄 .gitignore                            # Liste des fichiers/dossiers à ignorer par Git
├── 📄 README.md                             # Présentation générale du projet
├── 📄 LICENSE                               # Informations de licence du projet
└── 📄 CONTRIBUTING.md                       # Guide de contribution et conventions d'équipe
```

##Technologies utilisées

| Domaine | Technologies |
|---------|--------------|
| Frontend | Vue.js |
| Backend | Django |
| Base de données | MySQL |
| Tests unitaires | PyTest |
| Outils DevOps | GitHub Actions, SonarQube, Jira |

##Qualité du Code

[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-white.svg)](https://sonarcloud.io/summary/new_code?id=AymenZahed_Library-management-system)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=AymenZahed_Library-management-system&metric=coverage)](https://sonarcloud.io/summary/new_code?id=AymenZahed_Library-management-system)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=AymenZahed_Library-management-system&metric=bugs)](https://sonarcloud.io/summary/new_code?id=AymenZahed_Library-management-system)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=AymenZahed_Library-management-system&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=AymenZahed_Library-management-system)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=AymenZahed_Library-management-system&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=AymenZahed_Library-management-system)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=AymenZahed_Library-management-system&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=AymenZahed_Library-management-system)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=AymenZahed_Library-management-system&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=AymenZahed_Library-management-system)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=AymenZahed_Library-management-system&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=AymenZahed_Library-management-system)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=AymenZahed_Library-management-system&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=AymenZahed_Library-management-system)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=AymenZahed_Library-management-system&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=AymenZahed_Library-management-system)

##Stratégie de branches Git

Nous appliquons le modèle Git Flow, adapté au développement agile (SCRUM) :

| Branche | Rôle |
|---------|------|
| `main` | Branche principale et stable — contient uniquement le code validé et prêt pour la production |
| `develop` | Branche d'intégration — regroupe toutes les nouvelles fonctionnalités avant livraison |
| `feature/*` | Branche de développement d'une nouvelle fonctionnalité issue de `develop`<br>➡️ Exemple : `feature/add-auth-api` |
| `fix/*` | Branche pour corriger un bug mineur ou une anomalie non critique<br>➡️ Exemple : `fix/typo-in-dashboard` |
| `hotfix/*` | Branche de correctif d'urgence issue de `main` pour les bugs critiques en production<br>➡️ Exemple : `hotfix/fix-login-crash` |

##CI/CD Pipeline

Chaque push ou pull request déclenche le pipeline GitHub Actions :

1. **Initialisation** : vérifie la configuration du projet
2. **Tests unitaires** : exécute les tests via le framework choisi  
3. **Analyse de qualité** : envoie les résultats à SonarQube

##Gestion Agile

- **Méthode** : SCRUM
- **Outil** : Jira Software
- **Backlog initial** : 10+ user stories
- **Nombre de sprints** : 4
- **Sprint 0** : configuration des environnements et outils DevOps

##Installation

### Prérequis
- Python 3.8+
- Node.js 14+
- MySQL 5.7+

##Installation rapide

1. **Cloner le projet**
   ```bash
   git clone https://github.com/Abdelhafidh-87/Library-management-system.git
   cd Library-management-system
   ```

2. **Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Configurer la base de données**
   - Créez la base décrite dans le fichier `docs/INSTALL.md`
   - Renseignez vos identifiants dans `.env`

5. **Lancer le serveur**
   ```bash
   python manage.py runserver
   ```

##Documentation

Pour plus de détails sur l'installation, la configuration et l'utilisation, consultez le dossier `docs/`.

##Contribution

Veuillez lire [CONTRIBUTING.md](CONTRIBUTING.md) pour les détails sur notre code de conduite et le processus de soumission des pull requests.

##Licence

Ce projet est sous licence - voir le fichier [LICENSE](LICENSE) pour plus de détails.
