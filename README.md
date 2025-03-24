# SpaceProgrammerZ

**SpaceProgrammerZ** est un jeu rétro inspiré de *Space Invaders*, programmé avec **Pyxel**. J’avais envie de produire un jeu rétro, old school, plongé dans la nostalgie, dans mon temps libre. :)

---

## Fonctionnalités

- Déplacement fluide du vaisseau
- Tirs de projectiles
- Apparition aléatoire d’ennemis avec différents comportements :
  - Chute directe
  - Mouvement rebondi
  - Ennemis qui se divisent
- Gestion des points de vie
- Collisions avec explosions animées
- Score et système d'expérience
- Alerte "Ceinture d'astéroïdes"
- Ressources : textures personnalisées et musique intégrée
- Réinitialisation du jeu avec `R`

---

## Contrôles

| Touche     | Action                            |
|------------|-----------------------------------|
| ← ↑ ↓ →    | Déplacer le vaisseau              |
| `ESPACE`   | Tirer un projectile               |
| `D`        | Boost latéral instantané          |
| `T`        | Effacer tous les ennemis (debug)  |
| `R`        | Recommencer la partie             |

---

## LES ÉTAPES DU PROJET
1.	Idée initiale : Faire un jeu d’hommage à Space Invaders
2.	Prototype :
o	Affichage d’un carré bleu 8x8
o	Déplacement avec les flèches
o	Ajout d’un rectangle jaune comme projectile
o	Animation de montée du projectile
o	Apparition aléatoire de carrés rouges
o	Disparition du vaisseau en cas de collision
o	Calcul des collisions avec intervalles
o	Points de vie pour ennemis et projectiles
o	Explosion des sprites
o	Message “game over”
o	Compteur de score
3.	Transformation en projet complet :
o	Ajout d’un arrière-plan
o	Nouveaux ennemis
o	Apparences personnalisées
o	Événement scripté (ceinture d’astéroïdes)
o	Bande audio
o	Système d’alerte
o	Agrandissement de la surface de jeu

---


## Technologies

- **Python 3**
- **[Pyxel](https://github.com/kitao/pyxel)** – moteur de jeu rétro 8bit
- `.pyxres` : utilisé pour charger les musiques et graphismes

---

## Lancer le jeu

```bash
pip install pyxel
python jeu_SpaceProgrammerZ.py
