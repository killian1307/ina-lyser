# ⚡⚽ Ina-Lyser ⚽⚡

[![Static Badge](https://img.shields.io/badge/lang-en-FF0000)](README.md) [![Static Badge](https://img.shields.io/badge/lang-fr-0000FF)](README.fr.md) [![Static Badge](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
![Artwork officiel d'Inazuma Eleven: Victory Road](assets/img/cover.jpg)

## 🌐 Accès en Ligne

**Vous pouvez accéder au scanner et l'utiliser directement dans votre navigateur sans installation :**

<h3 align="center">
🚀 Cliquez ici pour lancer : <a href="https://ina-lyser.streamlit.app" target="_blank">https://ina-lyser.streamlit.app</a>
</h3>

---

**Ina-Lyser** est un outil automatisé conçu pour les joueurs d'**Inazuma Eleven: Victory Road**. Il vous permet de télécharger des captures d'écran de vos formations d'équipe, détecte automatiquement les noms des joueurs, les statistiques et les configurations tactiques grâce à une IA locale (OCR), et exporte les données dans un format JSON propre. Mon objectif était principalement de construire cet outil dans le cadre d'un projet plus vaste de site web compétitif pour **Inazuma Eleven: Victory Road**, mais d'autres outils ou créateurs d'équipe pourraient également profiter de sa simplicité d'exécution et de son format épuré !

## Résumé

Le projet résout la tâche fastidieuse de la transcription manuelle des données d'équipe. En utilisant la **Vision par Ordinateur** et la **Correspondance de Chaînes Floues** (Fuzzy String Matching), Ina-Lyser peut lire du texte en basse résolution ou légèrement obstrué sur des captures d'écran de jeu, le comparer à une base de données de joueurs connus, et reconstruire votre formation d'équipe exacte dans un format propre.

## Fonctionnalités

* **Scan Local par IA :** Utilise `EasyOCR` et `OpenCV` pour lire le texte des images.
* **Correspondance Floue (Fuzzy Matching) :** Détection intelligente qui corrige les coquilles de l'OCR (ex: corriger "Yuya Kogurer" en "Yuya Kogure").
* **Détection de Formation :** Identifie automatiquement les formations comme 4-4-2 Diamond, 4-4-2 Box, 3-5-2 Freedom, etc.
* **Export JSON :** Génère un fichier `.json` structuré contenant toutes les données des joueurs, statistiques et positions.
* **Support Double Langue :** Capable de détecter les noms de joueurs aux formats Romanji et Localisé.

## Prérequis & Installation

> 📝
> Le projet est hébergé en ligne sur [https://ina-lyser.streamlit.app/](https://ina-lyser.streamlit.app/), donc aucune installation n'est requise pour une utilisation standard. Cependant, si vous souhaitez l'exécuter localement ou contribuer, suivez ces étapes.

### Étapes d'Installation

1.  **Cloner le Dépôt :**
    Téléchargez le code source depuis GitHub sur votre machine locale.

2.  **Installer Python :**
    Assurez-vous d'avoir **Python 3.9+** installé.

3.  **Installer les Dépendances :**
    Ouvrez votre terminal ou invite de commande dans le dossier du projet et exécutez :
    ```bash
    pip install -r requirements.txt
    ```

4.  **Lancer l'Application :**
    Démarrez le serveur local en utilisant Streamlit :
    ```bash
    streamlit run main.py
    ```
    *(Note : Remplacez `main.py` par le nom de votre fichier d'entrée s'il est différent, par ex. `app.py`)*

## Protocole d'Utilisation

1.  **Téléchargement :** Glissez-déposez une capture d'écran claire de votre menu d'équipe (JPG/PNG) dans la zone de téléchargement.
    * *Limite :* Max 5Mo par fichier.
2.  **Scan :** Cliquez sur le bouton **"Scan Team"**.
    * L'application traitera l'image en appliquant des filtres pour améliorer la lisibilité du texte.
    * Elle affichera un journal des joueurs détectés en temps réel.
3.  **Vérification & Téléchargement :**
    * Une fois terminé, les membres de l'équipe détectés et la formation seront affichés.
    * Cliquez sur **"Download JSON"** pour sauvegarder vos données d'équipe.

> 💡
> **Astuce :** Pour de meilleurs résultats, utilisez des captures d'écran standard en 1080p. Évitez de prendre des photos de votre écran avec un téléphone, car les reflets peuvent interférer avec la reconnaissance de texte.

## Aperçu de l'Architecture

La structure du projet est organisée comme suit :

* **`main.py`** : Le point d'entrée pour l'application web Streamlit.
* **`assets/`** :
    * **`package/detector.py`** : La logique centrale contenant la classe `ExactTeamScanner`, le moteur OCR et les algorithmes de correspondance floue.
    * **`package/website.py`** : Gère la mise en page de l'interface utilisateur et la gestion du téléchargement de fichiers.
    * **`models/`** : Contient les modèles EasyOCR hors ligne (pour assurer un déploiement cloud rapide).
    * **`players/db.csv`** : La base de données contenant les noms et statistiques valides des joueurs.
* **`requirements.txt`** : Liste des bibliothèques Python requises pour exécuter l'application.

## Dépendances

Ce projet repose sur les bibliothèques open-source suivantes :

* **Streamlit :** Pour l'interface web et l'hébergement cloud.
* **EasyOCR :** Pour la reconnaissance optique de caractères (lecture de texte).
* **OpenCV (headless) :** Pour le prétraitement d'image (niveaux de gris, contraste, redimensionnement).
* **Pandas :** Pour la gestion de la base de données des joueurs (CSV).
* **Difflib :** Pour la correspondance de chaînes floues et la correction des coquilles.

## Licences

**Image de couverture :** [https://x.com/InazumaSeries/status/1968873138210701555](https://x.com/InazumaSeries/status/1968873138210701555)

**Licence MIT**

Vous êtes libre d'utiliser, modifier, distribuer et vendre ce logiciel, à condition d'inclure l'avis de droit d'auteur original et la licence dans toute copie ou partie substantielle du logiciel.

Pour plus de détails, veuillez vous référer au fichier [LICENSE](LICENSE) dans ce dépôt.
