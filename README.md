# Projet 10 Développeur d'application Python OC SoftDesk API

***Livrable du Projet 10 du parcours Développeur-d'Application Python d'OpenClassrooms***

API-SoftDesk est une API RESTful permettant de remonter et suivre des problèmes
techniques pour les trois plateformes (site web, applications Android et iOS).

L'application permet aux utilisateurs de créer divers projets,
d'ajouter des utilisateurs (contributeurs) à des projets spécifiques,
de créer des problèmes au sein des projets et d'attribuer des libellés
à ces problèmes en fonction de leurs priorités, de balises, etc.

![logo](assets/logo.png)

## Fonctionnalités

L'application permet de :

* -> creer diverses projets
* -> d'ajouter des utilisateurs à des projets spécifiques
* -> de creer des problèmes au sein des projets
* -> d'ajouter des commentaires aux problèmes identifiés
* -> seuls les auteurs des projets, problèmes, commentaires peuvent les modifier ou les supprimer

## Technologie utilisée

* Le projet est développé avec le framework REST Django, il s'agit d'une API REST.
* Les données sont sauvegardées dans une base de données sqlite3.
* Un swagger a été utilisé pour tester les points de terminaison de l'API et la documenter

## Installation

* Téléchargez et dézippez le repository github

* Creer l'environnement virtuel (exemple avec pipenv)

``` bash
pipenv install b
pipenv shell
```

## Utilisation

* Lancer le serveur : `python manage.py runserver`
* Depuis votre navigateur habituel, l'accès à l'api se fait via l'url : `http:/127.0.0.1:8000`
* Pour creer un compte administrateur, utilisez la commande : `python manage.py createsuperuser`
* Pour accéder à l'administration : `http://127.0.0.1:8000/admin`
* Les endpoints peuvent êtres testés ici : `http://127.0.0.1:8000/schema`

## Documentation

* Vous pouvez accéder à la documentation de l'API ici : `http://127.0.0.1:8000/docs`
