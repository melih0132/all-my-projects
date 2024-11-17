## **Gestion des Relevés de Comptages d’Oiseaux pour la Ligue de Protection des Oiseaux (LPO)**

### **Overview**  
Ce projet consiste à concevoir et implémenter une base de données permettant de gérer les relevés de comptages d’oiseaux pour la Ligue de Protection des Oiseaux (LPO). L’objectif est de faciliter la gestion des données, de réaliser des analyses statistiques pertinentes et de présenter les résultats de manière visuelle et interactive.  

### **Étapes du Projet**  
1. **Modélisation de la Base de Données**  
   - **MCD (Modèle Conceptuel des Données) :** Définition des entités, relations et contraintes pour représenter les relevés d’oiseaux, les observateurs, les espèces, les sites, etc.  
   - **MLD (Modèle Logique des Données) :** Traduction du MCD en tables relationnelles adaptées à PostgreSQL.  

2. **Mise en Place de la Base de Données (PostgreSQL)**  
   - Création des tables et définition des contraintes (clés primaires, étrangères, etc.).  
   - Insertion des données pour simuler les relevés réels.  
   - Développement de requêtes SQL pour interroger, analyser, et gérer les données.  

3. **Analyse Statistique (Excel)**  
   - Extraction des données pertinentes depuis PostgreSQL.  
   - Réalisation de statistiques descriptives : nombre d’individus par espèce, répartition géographique des observations, évolution des populations dans le temps, etc.  
   - Création de graphiques pour illustrer les résultats.  

4. **Rapport Interactif (Power BI)**  
   - Importation des données consolidées depuis PostgreSQL.  
   - Conception d’un tableau de bord interactif pour présenter :  
     - Les tendances des populations d’oiseaux.  
     - Les zones géographiques les plus riches en biodiversité.  
     - Les comparaisons annuelles ou saisonnières.  
   - Mise en avant d’indicateurs clés pour faciliter la prise de décision.  

### **Technologies Used**  
- **Base de Données :** PostgreSQL, pgAdmin4
- **Langage de Requêtes :** SQL  
- **Outils Statistiques :** Microsoft Excel  
- **Visualisation :** Power BI  

### **Installation et Exécution**  
1. **Configurer la base de données :**  
   - Installez PostgreSQL et exécutez les scripts SQL fournis pour créer et alimenter la base.  

2. **Exporter les données pour analyse :**  
   - Utilisez les requêtes SQL pour extraire les données nécessaires et les importer dans Excel pour l’analyse statistique.  

3. **Charger les données dans Power BI :**  
   - Connectez Power BI à PostgreSQL pour générer un tableau de bord interactif.  
