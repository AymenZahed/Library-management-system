# 📚 Library Management System

Système de gestion de bibliothèque avec architecture microservices (Django + Vue.js)

## 🏗️ Architecture

- **Backend**: Django + Microservices
- **Frontend**: Vue.js 
- **Base de données**: MySQL
- **CI/CD**: GitHub Actions + SonarQube

## 📊 Qualité du Code

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

## 🚀 Installation

```bash
# Back - end 
cd backend
pip install -r requirements.txt

# Front - end 
cd frontend
npm install
```



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
| Domaine  | Technologies |
|----------|--------------|
| Frontend |  Vue         |
| Backend  | Django       |
| Base de données | MySQL |
| Tests unitaires | PyTest|
| Outils DevOps | GitHub Actions, SonarQube, Jira |

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

# Stratégie de branches
Nous suivons le modèle Git Flow :

main → code stable, prêt à être déployé.

develop → branche d’intégration (pré-release).

feature/* → une branche par nouvelle fonctionnalité.

📘 Détails complets dans docs/BRANCH_STRATEGY.md


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


















