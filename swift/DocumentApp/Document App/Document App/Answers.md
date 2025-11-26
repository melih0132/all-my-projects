# Introduction à iOS avec UIKit

## Environnement de développement

### Exercice 1

**Ouvrir le storyboard : qu’est-ce que le storyboard ?**  
Le storyboard est un fichier visuel dans Xcode qui permet de concevoir l’interface utilisateur de l’application en plaçant des éléments graphiques (boutons, labels, vues, etc.) et en définissant les transitions entre les différents écrans. C’est un outil qui facilite la création d’interfaces sans avoir à écrire beaucoup de code.

**Ouvrir un simulateur : qu’est-ce que le simulateur ?**  
Le simulateur est un outil intégré à Xcode qui permet d’exécuter et tester l’application iOS directement sur l’ordinateur, sans avoir besoin d’un appareil physique. Il simule le fonctionnement d’un iPhone ou d’un iPad, permettant de vérifier le comportement de l’application dans différents environnements.

### Exercice 2

**À quoi sert le raccourci Cmd + R ?**  
Le raccourci Cmd + R permet de lancer l’exécution de l’application sur le simulateur ou sur un appareil connecté.

**À quoi sert le raccourci Cmd + Shift + O ?**  
Le raccourci Cmd + Shift + O ouvre une fenêtre de recherche rapide qui permet de trouver n’importe quel fichier, classe, fonction ou symbole dans le projet.

**Raccourci pour indenter le code automatiquement :**  
Le raccourci pour indenter automatiquement le code est Ctrl + I.

**Raccourci pour commenter la sélection :**  
Le raccourci pour commenter ou décommenter une sélection de code est Cmd + /.

### Exercice 3

**Lancer l’application sur un simulateur :**  
Pour lancer l’application, il faut d’abord choisir un simulateur dans la barre en haut de Xcode (par exemple un iPhone 14), puis appuyer sur Cmd + R ou cliquer sur le bouton « Run ». L’application se compile puis se lance dans le simulateur choisi.

**Changer d’appareil simulé :**  
Pour changer d’appareil simulé, il faut cliquer sur le menu déroulant en haut à gauche de Xcode où est indiqué le modèle de simulateur (par exemple iPhone 14). On peut alors sélectionner un autre modèle d’iPhone ou d’iPad. Ensuite, il suffit de relancer l’application pour voir comment elle fonctionne sur ce nouvel appareil.

## Délégation

### Exercice 1

**Pourquoi une propriété statique ?**  
Une propriété statique appartient à la structure elle-même et non à une instance particulière. Cela permet d’accéder à `DocumentFile.testData` directement sans avoir besoin de créer un objet `DocumentFile`. Ici, on stocke les données de test globalement pour pouvoir les réutiliser facilement.

### Exercice 2

**Pourquoi utiliser `dequeueReusableCell` ?**  
`dequeueReusableCell` permet de réutiliser les cellules déjà créées au lieu d’en créer une nouvelle pour chaque ligne. Cela optimise la mémoire et les performances, surtout quand la liste est longue, car on ne crée qu’un nombre limité de cellules visibles à un moment donné.

## Ajout de la navigation

**Que venons-nous de faire ?**  
En faisant `Editor > Embed In > Navigation Controller`, on a inséré un `UINavigationController` au-dessus de ton `DocumentTableViewController`. Le `UINavigationController` est un container view controller ; c’est un contrôleur spécial qui ne présente pas directement une vue, mais qui gère une pile de vues (stack). Ton `DocumentTableViewController` est maintenant le root view controller de cette pile.

**En pratique :**  
Le `UINavigationController` fournit la barre de navigation en haut (Navigation Bar). Chaque fois que tu veux aller vers une nouvelle page, tu fais un push d’un autre `UIViewController` sur cette pile. Quand tu reviens en arrière, c’est un pop automatique qui retire le contrôleur courant de la pile.

**Quel est le rôle du NavigationController ?**  
Il orchestre la navigation hiérarchique dans l’application. Il gère la pile d’écrans (stack) et fournit les outils intégrés : bouton Back automatique, titre de la page (défini par la propriété `navigationItem.title` du contrôleur courant), barres d’outils et boutons configurés par chaque contrôleur (`navigationItem.leftBarButtonItem`, `rightBarButtonItem`, etc.).

**Est-ce que la NavigationBar est la même chose que le NavigationController ?**  
Non. La Navigation Bar (la barre en haut avec le titre et les boutons) n’est qu’un élément d’interface graphique. Le Navigation Controller est le contrôleur qui gère la pile d’écrans et qui affiche automatiquement une Navigation Bar correspondant à la vue en cours.  
Ainsi, le NavigationController représente la logique de navigation, tandis que la NavigationBar est ce que l’utilisateur voit en haut.

## Créer l’écran de détail

### Exercice 1

**Qu’est-ce qu’un Segue et à quoi il sert ?**  
Un Segue est un mécanisme d’UIKit qui définit la transition entre deux écrans dans un storyboard. Il permet de passer d’un `ViewController` à un autre et de transmettre des données si nécessaire.

### Exercice 2

**Qu’est-ce qu’une constraint ? À quoi sert-elle ? Quel est le lien avec AutoLayout ?**  
Une constraint est une règle de positionnement ou de dimension appliquée à une vue (exemple : collée aux bords, centrée, largeur fixe). Elle sert à adapter l’interface à toutes les tailles d’écran. AutoLayout est le système d’UIKit qui utilise ces contraintes pour calculer dynamiquement la disposition des vues.
