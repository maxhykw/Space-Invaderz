import pyxel
import random
 
 
class Jeu:
 
    def __init__(self):
        """
        Méthode d’initialisation de la classe Jeu.
        """
 
        # taille de la fenêtre du jeu : 128 pixels par 128 pixels
        pyxel.init(256, 256)
 
        # compteur du temps dès le lancement du jeu
        self.temps = 0
        self.tombe_ou_pas = 0

        # initialisation de nombre des éléments à l'arrière plan
        self.etoile = []
        self.grosse_etoile = []

        # position initiale du vaisseau
        self.vaisseau_x = 128
        self.vaisseau_y = 200
        self.vaisseau_vie = 1
 
        # compteur d'énergie pour l'évacuation imédiate du vaisseau
        self.boost_vaisseau = 0
        self.boosting = None

        # sert à contrôler si le jeu est terminé ou pas
        self.controle_et_progres = True
 
        # compteur des points du score accumulés
        self.experience = 0
        self.niveau_suivant = 30
        self.niveau_actuel = 1
 
        # compteur des pieces que les ennemis lachent aleatoirement
        self.coins = 0

        # initialisation de nombre de boulets représentés par les éléments dans la liste
        self.jaune = []
 
        # initialisation de nombre des ennemis représentées par les éléments dans la liste
        self.ennemi = []
 
        # initialisation de nombre des effets d'explosion représentés par les éléments dans la liste
        self.explosion = []
 
        # initialiser le message qui sera afficher en fonction des événements
        self.message = "score"
 
        # mettre toutes les alertes en False pour ne pas les afficher tout de suite
        self.alerte_asteroides = False

        # charger et jouer le fichier contenant la musique
        pyxel.load("projet_music.pyxres")
        pyxel.play(0,0)

        # charger le fichier contenant les différentes textures
        pyxel.load("my_resource.pyxres")

        # démarrer la mise à jour continuelle du jeu
        pyxel.run(self.update, self.draw)
 
    def update(self):
        """
        Méthode principale de la classe, se met à jour continuellement et relance les autres méthodes pour que la classe puisse fonctionner.
        """

        # ajoute le temps passé
        self.temps += 1
        if self.temps - self.tombe_ou_pas == 600:
            self.tombe_ou_pas = 3 * self.temps / 2

        # si le bouton T est pressé, effacer tous les ennemis, faire avancer le temps et ajouter 10 points d'expérience
        if pyxel.btn(pyxel.KEY_T):
            self.temps += 10
            self.experience += 10
            self.ennemi = []

        # si le bouton R est pressé, on réinitialise les affichages et les variables et recommence le jeu à zéro
        if pyxel.btnp(pyxel.KEY_R):
            self.temps = 0
            self.tombe_ou_pas = 0
            self.etoile = []
            self.grosse_etoile = []
            self.vaisseau_x = 128
            self.vaisseau_y = 200
            self.vaisseau_vie = 1
            self.boost_vaisseau = 0
            self.controle_et_progres = True
            self.points = 0
            self.experience = 0
            self.niveau_suivant = 30
            self.niveau_actuel = 1
            self.coin = 0
            self.jaune = []
            self.ennemi = []
            self.explosion = []
            self.message = "score"
            self.alerte_asteroides = False
 
        # mise à jour de l'arrière plan
        self.arriere_plan_ajout()
        self.arriere_plan_mouvement()

        # si le jeu n’est pas fini, accorder au joueur le contrôle du vaisseau et appliquer la méthode qui ajoute les boulets et ennemis a des listes respectives et la méthode permettant d’afficher des alertes à l'écran
        if self.controle_et_progres == True:
            self.vaisseau_controle()
            self.boulet_et_ennemi_ajout()
            self.alerte()
 
        # sinon, attribuer à la variable “message” le texte “game over”
        else:
            self.message = "game over"
 
        # peu importe la condition ci-dessus, les méthodes suivantes sont lancées à chaque mise à jour
        self.boulet_et_ennemi_mouvement()
        self.points_ajout()
        self.exploser_et_supprimer()
 
    def vaisseau_controle(self):
        """
        Methode pour que le joueur puisse contrôler le vaisseau.
        """
 
        # si le bouton “droite“ est appuyé alors le vaisseau bouge à droite
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.vaisseau_x = (self.vaisseau_x + 1) % pyxel.width
 
        # si le bouton “gauche” est appuyé alors le vaisseau bouge à gauche
        if pyxel.btn(pyxel.KEY_LEFT):
            self.vaisseau_x = (self.vaisseau_x - 1) % pyxel.width
 
        # si le bouton “haut” est appuyé alors le vaisseau bouge en haut
        if pyxel.btn(pyxel.KEY_UP):
            self.vaisseau_y = (self.vaisseau_y - 1) % pyxel.height
 
        # si le bouton “bas” est appuyé alors le vaisseau bouge en bas
        if pyxel.btn(pyxel.KEY_DOWN):
            self.vaisseau_y = (self.vaisseau_y + 1) % pyxel.height
 
        # si le bouton D est appuyé alors le vaisseau s'évacue imédiatement à droite
        if pyxel.btn(pyxel.KEY_D):
            self.boosting = "d"

    def arriere_plan_ajout(self):
        """
        Méthode pour réaliser l'arrière plan du jeu.
        """

        # ajouter une étoile à l'arrière plan quand la valeur du temps est une multiple de 2
        if self.temps % 2 == 0:
           self.etoile.append([random.randint(0,256), 0, 1])

        # ajouter une grosse étoile à l'arrière plan quand la valeur du temps est une multiple de 90
        if self.temps % 90 == 0:
           self.grosse_etoile.append([random.randint(0,256), 0, 1])

    def arriere_plan_mouvement(self):
        """
        Méthode pour mettre des mouvements à l'arrière plan.
        """

        # déplacer les positions de toutes les étoiles vers le bas
        for i in range(len(self.etoile)):
            self.etoile[i][1] += 8

        # déplacer les positions de toutes les grandes étoiles vers le bas, mais moins rapidement
        for j in range(len(self.grosse_etoile)):
            self.grosse_etoile[j][1] += 0.325

    def boulet_et_ennemi_ajout(self):
        """
        Méthode pour contrôler l’ajout de boulets et d’ennemis à l'écran.
        """
 
        # si le bouton “espace” est pressé, ajouter à la liste des boulets une nouvelle balle
        if pyxel.btn(pyxel.KEY_SPACE):
            self.jaune.append([self.vaisseau_x + 5, self.vaisseau_y - 1, 1])
 
        # la variable “random_ennemie” prend une valeur aléatoire entre 1 et 15
        if self.temps >= 600:
            random_ennemi = random.randint(1, 10)
        else:
            random_ennemi = random.randint(1, 15)

        random_tombe_ennemi = random.randint(1, 2)

        if self.temps >= 1350:
            random_rebondi_ennemi = random.randint(1, 40)
        else:
            random_rebondi_ennemi = random.randint(1, 60)
 
        # si la valeur prise est égale à 5, alors ajouter à la liste d’ennemis, la liste contenant les informations sur la position aléatoire qu’aura l’ennemi et son point de vie (4)
        if random_ennemi == 1:
            self.ennemi.append([random.randint(1, 255), 0, 4, 1, "not"])

        if random_tombe_ennemi == 1 and self.temps - self.tombe_ou_pas >= 300:
            self.ennemi.append([random.randint(1, 255), 0, 2, 2, "not"])

        if self.temps >= 630:
            if random_rebondi_ennemi == 1:
                self.ennemi.append([128, 0, 4, 3, "not", "g"])
            elif random_rebondi_ennemi == 21:
                self.ennemi.append([128, 0, 4, 3, "not", "d"])
 
    def boulet_et_ennemi_mouvement(self):
        """
        Méthode pour contrôler le mouvement des boulets et des ennemis. Permet aussi de gérer les points de vie associés à chaque balle et à chaque ennemi.
        """
 
        # répéter la boucle autant de fois qu’il y a de valeurs dans la liste “jaune”
        for i in range(len(self.jaune)):
            # permet de déplacer la position du ième boulet vers le haut
            self.jaune[i][1] -= 6
            # répéter la boucle autant de fois qu’il y a de valeurs dans la liste “ennemi”
            for j in range(len(self.ennemi)):
                if self.ennemi[j][3] == 4:
                    # si le ième boulet performe une collision avec la jème ennemi
                    if self.jaune[i][0] - 3 <= self.ennemi[j][0] and self.ennemi[j][0] <= self.jaune[i][0] and self.jaune[i][1] - 3 <= self.ennemi[j][1] and self.ennemi[j][1] <= self.jaune[i][1] + 4:
                        # alors les point de vie du boulet sont nul, il disparaît
                        self.jaune[i][2] = 0
                        # si les point de vie de l’ennemi sont différents de 0, alors on lui déduit 1 point de vie
                        if self.ennemi[j][2] != 0:
                            self.ennemi[j][2] -= 1
                            if self.ennemi[j][4] != "damaged 2":
                                self.ennemi[j][4] = "damaged"

                # si le ième boulet performe une collision avec la jème ennemi
                if self.jaune[i][0] - 7 <= self.ennemi[j][0] and self.ennemi[j][0] <= self.jaune[i][0] and self.jaune[i][1] - 7 <= self.ennemi[j][1] and self.ennemi[j][1] <= self.jaune[i][1] + 8:
                    # alors les point de vie du boulet sont nul, il disparaît
                    self.jaune[i][2] = 0
                    # si les point de vie de l’ennemi sont différents de 0, alors on lui déduit 1 point de vie
                    if self.ennemi[j][2] != 0:
                        self.ennemi[j][2] -= 1
                        if self.ennemi[j][4] != "damaged 2":
                            self.ennemi[j][4] = "damaged"
 
        # répéter la boucle autant de fois qu’il y a d’élément dans la liste “ennemi”
        for i in range(len(self.ennemi)):
            # on applique ces modifications aux valeurs de la liste "ennemi", pour déplacer la ième ennemi
            if self.ennemi[i][3] == 1:
                self.ennemi[i][0] += random.randint(-1, 1)*random.randint(1, 3)
                self.ennemi[i][1] += 1

            if self.ennemi[i][3] == 2:
                self.ennemi[i][1] += 2

            if self.ennemi[i][3] == 3 or self.ennemi[i][3] == 4:
                if self.ennemi[i][5] == "d":
                    self.ennemi[i][0] += 1
                elif self.ennemi[i][5] == "g":
                    self.ennemi[i][0] += -1

                if self.temps % 5 == 0:
                    self.ennemi[i][1] += 1

                if self.ennemi[i][0] == 1 and self.ennemi[i][5] == "g":
                    self.ennemi[i][5] = "d"
                if self.ennemi[i][0] == 248 and self.ennemi[i][5] == "d":
                    self.ennemi[i][5] = "g"

                if self.ennemi[i][2] == 0 and self.ennemi[i][3] == 3:
                    self.ennemi.append([self.ennemi[i][0]+1, self.ennemi[i][1]+1, 11, 4, "not", "d"])
                    self.ennemi.append([self.ennemi[i][0]+1, self.ennemi[i][1]+1, 11, 4, "not", "g"])

            if self.ennemi[i][4] == "damaged":
                self.ennemi[i][4] = "damaged 2"
            elif self.ennemi[i][4] == "damaged 2":
                self.ennemi[i][4] = "not"

            # si le vaisseau performe une collision avec le ième ennemi, alors les points de vie du vaisseau sont de 0
            if self.vaisseau_x - 7 <= self.ennemi[i][0] <= self.vaisseau_x + 7 and self.vaisseau_y - 7 <= self.ennemi[i][1] <= self.vaisseau_y + 7:
                self.vaisseau_vie = 0
 
    def points_ajout(self):
        """
        Méthode pour ajouter les points du score et gérer la manière d’afficher ces scores.
        """
 
        # répéter la boucle autant de fois qu’il y a de valeurs dans la liste “ennemi”
        for i in range(len(self.ennemi)):
            # si les points de vie de la ième ennemi sont nuls, alors ajouter un point du score qui est attribué au type de l'ennemi
            if self.ennemi[i][2] == 0 and self.controle_et_progres == True:
                if self.ennemi[i][3] == 1:
                    self.experience += 2
                elif self.ennemi[i][3] == 2:
                    self.experience += 1
                elif self.ennemi[i][3] == 3:
                    self.experience += 2
                elif self.ennemi[i][3] == 4:
                    self.experience += 4

        if self.experience >= self.niveau_suivant:
            self.niveau_suivant = self.niveau_suivant * 1.5
            self.experience = 0
            self.niveau_actuel += 1
 
        # la variable “nb_chiffre_points“ prend 4 autant de fois que le nombre de chiffres compris dans le score
        self.nb_chiffre_points = (len(str(self.experience))-1) * 4
 
    def exploser_et_supprimer(self):
        """
        Méthode pour produire des explosions.
        Elle permet également de supprimer certains éléments.
        """
 
        # si le vaisseau n’a plus de points de vie quand le jeu n’est pas encore terminé, alors ajouter à la liste “explosion” les coordonnées du vaisseau du joueur et “controle_et_progres” prend la valeur 0 pour que le jeu termine
        if self.vaisseau_vie == 0 and self.controle_et_progres == 1:
            self.explosion.append([self.vaisseau_x, self.vaisseau_y, 0])
            self.controle_et_progres = False
 
        # répéter la boucle autant de fois qu’il y a de valeur dans la liste “ennemi”
        for i in range(len(self.ennemi)):
            # si les points de vie de l’ennemi sont nuls, alors ajouter à la liste “explosion” les coordonnées du ennemi
            if self.ennemi[i][2] == 0:
                if self.ennemi[i][3] <= 2:
                    self.explosion.append([self.ennemi[i][0], self.ennemi[i][1], 0, 1])

                elif self.ennemi[i][3] == 3:
                    self.explosion.append([self.ennemi[i][0], self.ennemi[i][1], 0, 2])
 
        # répéter la boucle autant de fois qu’il y a de valeur dans la liste “explosion”
        for i in range(len(self.explosion)):
            # on ajoute à la 3ème valeur, relatant l'état d’explosion, 1
            self.explosion[i][2] += 1
 
        # nettoyage des listes pour faire disparaître les éléments du jeu
        self.explosion = [i for i in self.explosion if i[2] <= 12]
        self.jaune = [i for i in self.jaune if i[2] != 0 and i[1] >= 0]
        self.ennemi = [i for i in self.ennemi if i[2] != 0 and i[1] <= 256]
 
    def alerte(self):
        """
        Méthode pour donner une alerte en fonction des événements
        """

        # si la différence du compteur en temps et la variable “tombe_ou_pas” plus 70 est supérieur ou égal à 300, on donne l’alerte astéroïdes
        # on synchronise l’apparition du message d’alerte et les astéroïdes, puis on ajoute 70 pour faire apparaître le message un peu avant les astéroïdes
        if self.temps - self.tombe_ou_pas + 70 >= 300 and self.temps - self.tombe_ou_pas + 70 <= 450:
            self.alerte_asteroides = True

        # sinon on ne donne pas l'alerte
        else:
            self.alerte_asteroides = False

    def draw(self):
        """
        Méthode pour l’affichage d’objets à l'écran.
        L’ordre du code impacte sur l’ordre des affichages
        (ex: l’affichage du score est au tout début pour qu’il soit traité comme arrière-plan.)
        """
 
        # vider la fenêtre
        pyxel.cls(0)

        # afficher toutes les étoiles pour animer l'arrière plan
        for j in range(len(self.grosse_etoile)):
            if self.grosse_etoile[j][2] != 0:
                pyxel.text(self.grosse_etoile[j][0], self.grosse_etoile[j][1], "+", 7)
        for i in range(len(self.etoile)):
            if self.etoile[i][2] != 0:
                pyxel.rect(self.etoile[i][0], self.etoile[i][1], 1, 5, 13)

# si les points de vie sont différents de 0, alors afficher l'image 1 de l'éditeur qui est un vaisseau jouable par le joueur
        if self.vaisseau_vie != 0:
            pyxel.blt(self.vaisseau_x, self.vaisseau_y, 0, 2, 2, 12, 13, 0)

        for i in range(self.experience):
            pyxel.rect(i*248/self.niveau_suivant + 6, 12, 248/self.niveau_suivant + 1, 3, 3)
        pyxel.rect(0, 12, 2, 3, 1)
        pyxel.rect(2, 12, 4, 3, 5)
        pyxel.rect(250, 12, 4, 3, 5)
        pyxel.rect(254, 12, 2, 3, 1)
        pyxel.rect(2, 10, 252, 2, 1)
        pyxel.rect(2, 14, 252, 2, 1)

        
 
        # répéter la boucle autant de fois qu’il y a de valeur dans la liste “jaune”
        for i in range(len(self.jaune)):
            # si les points de vie du ième boulet sont différents de 0, alors afficher un carre 1x4 de couleur 10 qui est un boulet de canon tiré par le vaisseau
            if self.jaune[i][2] != 0:
                pyxel.rect(self.jaune[i][0], self.jaune[i][1], 1, 4, 10)
 
        # répéter la boucle autant de fois qu’il y a de valeur dans la liste “ennemi”
        for i in range(len(self.ennemi)):
            # si les points de vie du ième ennemi sont différents de 0, alors afficher un carre 8x8 de couleur 8 qui est un ennemi
            if self.ennemi[i][2] != 0:
                if self.ennemi[i][4] == "damaged 2":
                    if self.ennemi[i][3] == 4:
                        # ?
                        pyxel.rect(self.ennemi[i][0], self.ennemi[i][1], 4, 4, 10)

                    else:
                        # ennemi de couleur 10 (jaune, orange) 8x8
                        pyxel.blt(self.ennemi[i][0], self.ennemi[i][1], 1, 3, 13, 11, 12, 0)

                elif self.ennemi[i][3] == 1:
                    # ennemi de couleur 8 (violet) 8x8
                    pyxel.blt(self.ennemi[i][0], self.ennemi[i][1], 1, 3, 27, 11, 36, 0)

                # astéroïdes 8x8
                elif self.ennemi[i][3] == 2:
                    x = random.randint(1, 4)
                    if x == 1:
                        pyxel.blt(self.ennemi[i][0], self.ennemi[i][1], 2, 1, 1, 13, 13, 0)
                    
                    elif x == 2:
                        pyxel.blt(self.ennemi[i][0], self.ennemi[i][1], 2, 2, 17, 14, 28, 0) 

                    elif x == 3:
                        pyxel.blt(self.ennemi[i][0], self.ennemi[i][1], 2, 1, 33, 13, 45, 0)

                    elif x == 4:
                        pyxel.blt(self.ennemi[i][0], self.ennemi[i][1], 2, 1, 50, 12, 61, 0)
                
                # ennemi de couleur 4 (marron) 8x8
                elif self.ennemi[i][3] == 3:
                    pyxel.blt(self.ennemi[i][0], self.ennemi[i][1], 1, 34, 2, 44, 12, 0)

                # mini astéroïdes 4x4
                elif self.ennemi[i][3] == 4:
                    pyxel.blt(self.ennemi[i][0], self.ennemi[i][1], 2, 21, 6, 25, 10, 0)

 
        # pour afficher une explosion
        # répéter la boucle autant de fois qu’il y a de valeur dans la liste “explosion”
        for i in range(len(self.explosion)):
            # si l’état d’explosion du ième élément compris dans la liste est inférieur ou égal à 3, alors afficher un carre 2x2 de couleur 8 qui est une explosion
            if self.explosion[i][2] <= 3:
                pyxel.rect(self.explosion[i][0] + 3, self.explosion[i][1] + 3, 2, 2, 8)
 
            # sinon, si l’état du même élément compris dans la liste est supérieur à 3 et inférieur ou égal à 6, alors afficher un carre 4x4 de couleur 14 qui est qui est la continuitée de l’explosion
            elif 3 < self.explosion[i][2] <= 6:
                pyxel.rect(self.explosion[i][0] + 2, self.explosion[i][1] + 2, 4, 4, 14)
 
            # sinon, si l’état du même élément compris dans la liste est supérieur à 6 et inférieur ou égal à 9, alors afficher un carre 8x8 de couleur 15 qui est la continuitée de l’explosion
            elif 6 < self.explosion[i][2] <= 9:
                pyxel.rect(self.explosion[i][0], self.explosion[i][1], 8, 8, 15)
 
            # si toutes ces conditions ne sont pas vérifiées, alors afficher un carre 12x12 de couleur 7 qui est la continuitee de l’explosion
            else:
                pyxel.rect(self.explosion[i][0] - 2, self.explosion[i][1] - 2, 12, 12, 7)
 
        # si l’alerte astéroïdes est donnée, alors on affiche un message d’alerte et on ajoute des bordures rouge et orange
        if self.alerte_asteroides == True:
            pyxel.text(60, 60, "alerte asteroides", 7)
            pyxel.rect(0, 0, 2, 256, 8)
            pyxel.rect(0, 0, 256, 2, 8)
            pyxel.rect(254, 0, 2, 256, 8)
            pyxel.rect(2, 2, 2, 256, 9)
            pyxel.rect(2, 2, 256, 2, 9)
            pyxel.rect(252, 2, 2, 256, 9)

        #si un ennemi est tue alors faire tomber une piece aleatoirement
        pyxel.circ(5,5,2,10)
        pyxel.text(12,3,f"= {self.coins}",10) 

        # si le message qui doit être affichée est “game over”, alors afficher l’écran final
        if self.message == "game over":
            pyxel.rect(0, 84, 256, 84, 0)
            pyxel.rect(0, 80, 256, 4, 4)
            pyxel.rect(0, 168, 256, 4, 4)
            pyxel.rect(80, 80, 4, 20, 4)
            pyxel.rect(172, 80, 4, 20, 4)
            pyxel.rect(80, 100, 96, 4, 4)
            pyxel.text(92, 86, "game over", 2)
            pyxel.text(86, 122, "your score:", 7)
            pyxel.text(124 - self.nb_chiffre_points, 144, f"{self.experience}", 8)
 
Jeu()


