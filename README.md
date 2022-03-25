# PRO3600-22-SELL-25

Projet d'informatique 1A : NAAMA, COLE, ZOUGHEBI, BRUN, ABRI

Le descriptif de l'application et  partie back/front end est précisé dans les fichiers source.

Pour l'instant notre application en stade de prototype n'est pas capable de reconnaître les images envoyées depuis l'application, mais uniquement celle du jeu de données de validation
avec une précision allant jusqu'à 79% pour 4/5 "tours" du réseau de neurones (appelés epochs), ce qui est améliorable (cf results.png )

La matrice de confusion présente nos résultats sur un large pool de données : jusqu'à 162 images biens prédites pour les architectures de type Quine Anne sur 175 tests (cf matrice.png)

Pour utiliser le prototype pour une prédiction : il suffit d'importer une image test dans le répertoire courant, puis de la renommer imagetest.jpg et d'executer les cellues correspondantes. La prédiction sera affichée sous forme de string sur le terminal (cf prediction.png)


