'''
Ce fichier est un module utilisé dans main.py
'''

# Importation des modules
import tkinter as tk
from functools import partial
from tkinter.messagebox import *
from random import choice
import string
import math

'''
# ========================================== #
# Fonction - Liste point
# ========================================== #
'''

###
# Procédure créant un widget Toplevel demandant le nom et les coordonnées
# du point à ajouter.
# Entrée(s) :   - list_point: widget Listbox
#               - fen : fenêtre principal
def list_add_point(list_point, fen):
    # Construction de la fenêtre fen
    tp_addPoint = tk.Toplevel()

    # Titre de la fenêtre
    tp_addPoint.title('Ajouter un point')

    # Rediemensionnement vertical, horizontal désactivé
    tp_addPoint.resizable(False, False)

    # Toplevel transient
    # Toplevel toujours devant la fenêtre principal
    tp_addPoint.transient(master=fen)

    # Sélection et vérrouillage du Toplevel
    tp_addPoint.grab_set()

    # Construction des Labels, des Entrys et des Buttons.
    lb_nom = tk.Label(tp_addPoint, text='Nom du point :', anchor='w')
    entry_nom = tk.Entry(tp_addPoint, relief= 'sunken')

    lb_x = tk.Label(tp_addPoint, text='Position x :', anchor='w')
    entry_x = tk.Entry(tp_addPoint, relief= 'sunken')

    lb_y = tk.Label(tp_addPoint, text='Postion y :', anchor='w')
    entry_y = tk.Entry(tp_addPoint, relief= 'sunken')

    button_ajouter = tk.Button(tp_addPoint, text='Ajouter', width=5, command= partial(check_entry,tp_addPoint, entry_nom, entry_x, entry_y, list_point))
    button_annuler = tk.Button(tp_addPoint, text='Annuler', width=5, command= tp_addPoint.destroy)

    # Placement des widgets dans le Toplevel
    lb_nom.grid(row=0, column=0,
                columnspan=2,
                sticky='we',
                padx=10,
                pady=2)
    entry_nom.grid(row=1, column=0,
                   columnspan=2,
                    sticky='we',
                    padx=10,
                    pady=5)

    lb_x.grid(row=2, column=0,
              sticky='we',
              padx=10,
              pady=2)
    entry_x.grid(row=3, column=0,
                 sticky='we',
                 padx=10,
                 pady=5)

    lb_y.grid(row=2, column=1,
              sticky='we',
              pady=2)
    entry_y.grid(row=3, column=1,
                 sticky='we',
                 padx=10,
                 pady=5)

    button_ajouter.grid(row=4, column=0,
                        sticky='we',
                        padx=10,
                        pady=5)
    button_annuler.grid(row=4, column=1,
                        sticky='we',
                        padx=10,
                        pady=5)

    # Centrage du Toplevel au centre de l'écran
    center(tp_addPoint)


###
# Fonction vérifant si les valeurs entrées
# dans les Entrys sont correctes.
# Entrée(s) : nombre : widget Entry
# Retourne(s) : une booléenne
def check_values(nombre):

    # Compteur de point
    count_dot = 0
    # Tableau contenant les valeurs admises
    validElement = ['-','.','0','1','2','3','4','5','6','7','8','9']

    # Si l'Entry n'est pas vide
    if nombre.get() != '':

        # On parcourt chaque caractère de l'Entry
        for i in nombre.get():
            # Si le caractère n'est pas dans le tableau
            if i not in validElement:
                return False
            # Si c'est un point
            if i == '.':
                count_dot += 1
            # Si le '-' n'est pas au début
            if i == '-' and nombre.get().index(i) != 0:
                return False
    # Si l'Entry est vide
    else:
        return False
    # Si il y a plus d'un point
    if count_dot > 1:
        return False

    return True


###
# Procédure vérifiant les Entrys
# et insérant le point dans la liste.
# Entrée(s) :   - tp_addPoint : widget Toplevel
#               - nom : Entry
#               - x : Entry
#               - y : Entry
#               - list_point
def check_entry(tp_addPoint, nom, x, y, list_point):

    # Si toutes les Entrys sont valides
    if nom.get() != '' and check_values(x) == True and check_values(y) == True:

        # Insertion dans la liste "nom (x;y)"
        list_point.insert(tk.END, nom.get() +' (' + clean_value(x) + ';' + clean_value(y) + ')')
        # Destruction du Toplevel
        tp_addPoint.destroy()

    else:
        # Affichage d'une fenêtre de dialogue erreur
        showerror('ERREUR !', 'Entrée invalide !', parent=tp_addPoint)


###
# Fonction nettoyant un nombre
# pour n'avoir que deux décimales.
# Entrée(s) : entry : Entry
# Retourne(s) : un String du nombre "nettoyé"
def clean_value(entry):
    # Conversion du Int en Float
    value = str(float(entry.get()))
    # Si le nombre n'a pas de décimal, càd qu'il finit par ".0"
    if value.endswith('.0') == True:
        # Retourne le nombre
        return value[:value.index('.')]

    else:
        # Retourne le nombre + 2 décimals
        return value[:value.index('.')+3]


###
# Procédure supprimant l'élément sélectionné
# du widget Listbox.
# Entrée(s) : list_point : widget Listbox
def list_delete_point(list_point):
    # Si aucun élément n'est sélectioné
    if list_point.curselection() == ():
        # Affichage d'une fenêtre de dialogue erreur
        showerror('ERREUR !', 'Aucun élément sélectionné')
    else:
        # Récupération de la position dans la liste
        # de l'élément selectioné
        index = list_point.curselection()
        # Suppression de l'élément
        list_point.delete(index)
        # Sélection du nouvel élément à sa place
        list_point.selection_set(index)


###
# Procédure déplaçant l'élément sélectionné
# au dessus dans le widget Listbox.
# Entrée(s) : list_point : widget Listbox
def move_up(list_point):
    # Si aucun élément n'est sélectioné
    if list_point.curselection() == ():
        # Affichage d'une fenêtre de dialogue erreur
        showerror('ERREUR !', 'Aucun élément sélectionné')
    else:
        # Récupération de la position dans la liste
        # de l'élément selectioné
        indice = list_point.curselection()[0]

        # Si l'élément sélectionné n'est pas le premier de la liste
        if indice > 0:
            # Insertion de l'élément sélectionné au dessus de l'élément précédent
            list_point.insert(indice-1, list_point.get(indice))
            # Suppression de l'élément sélectioné
            list_point.delete(list_point.curselection())
            # Sélection du nouvel élément ajouté
            list_point.selection_set(indice-1)


###
# Procédure déplaçant l'élément sélectionné
# en dessous dans le widget Listbox.
# Entrée(s) :list_point : widget Listbox
def move_down(list_point):
    # Si aucun élément n'est sélectioné
    if list_point.curselection() == ():
        # Affichage d'une fenêtre de dialogue erreur
        showerror('ERREUR !', 'Aucun élément sélectionné')
    else:
        # Récupération de la position dans la liste
        # de l'élément selectioné
        indice = list_point.curselection()[0]
        # Si l'élément sélectionné n'est pas le dernier de la liste
        if indice < list_point.size()-1:
            # Insertion de l'élément sélectionné après l'élément suivant
            list_point.insert(indice+2, list_point.get(indice))
            # Suppression de l'élément sélectioné
            list_point.delete(list_point.curselection())
            # Sélection du nouvel élément ajouté
            list_point.selection_set(indice+1)



'''
# ========================================== #
# Fonction - Edition canvas
# ========================================== #
'''

###
# Procédure assignant au clic gauche dans le canevas 'can' la procédure
# add_point
# Entrée(s) :   - can: le canevas principal
#               - frame: le cadre où se trouve le canevas 'can'
#               - grid_value: la valeur rattachée à la grille
#               - list_point: widget Listbox contenant les coordonnées et noms de tout les points
#               - numberZoom: variable stockant le nombre de zoom réalisé
#               - inclinaison: variable stockant l'inclinaison du canevas
def click_to_add(can,frame,list_point,grid_value,numberZoom, inclinaison):
    # on retire toute précédente assignation sur le clic gauche de la souris
    can.unbind('<Button-1>')

    # cette commande change l'aspect du curseur sur le canevas
    can.config(cursor= 'plus')

    # on assigne au clic gauche de la souris la procédure add_point
    can.bind("<Button-1>",lambda x:add_point(x,frame,can,list_point,grid_value,numberZoom, inclinaison))


###
# Procédure assignant au clic gauche dans le canevas 'can' la procédure
# del_point
# Entrée(s) :   - can: le canevas principal
#               - frame: le cadre où se trouve le canevas 'can'
#               - grid_value: la valeur rattachée à la grille
#               - list_point: widget Listbox contenant les coordonnées et noms de tout les points
#               - numberZoom: variable stockant le nombre de zoom réalisé
#               - inclinaison: variable stockant l'inclinaison du canevas
def click_to_del(can,frame,list_point,grid_value, numberZoom, inclinaison):
    # on retire toute précédente assignation sur le clic gauche de la souris
    can.unbind('<Button-1>')

    # cette commande change l'aspect du curseur sur le canevas
    can.config(cursor= 'X_cursor')

    # on assigne au clic gauche de la souris la procédure del_point
    can.bind("<Button-1>",lambda x:del_point(x,frame,can,list_point,grid_value,numberZoom, inclinaison))


###
# Procédure assignant au clic gauche dans le canevas 'can' la procédure
# move_point
# Entrée(s) :   - can: le canevas principal
#               - frame: le cadre où se trouve le canevas 'can'
#               - list_point: widget Listbox contenant les coordonnées et noms de tout les points
#               - grid_value: la valeur rattachée à la grille
#               - numberZoom: variable stockant le nombre de zoom réalisé
#               - inclinaison: variable stockant l'inclinaison du canevas
#               - x_center,y_center: variable stockant les coordonnées du centre
#               du canevas
def click_to_move(can,frame,list_point,grid_value, numberZoom, inclinaison, x_center, y_center):
    # on retire toute précédente assignation sur le clic gauche de la souris
    can.unbind('<Button-1>')

    # cette commande change l'aspect du curseur sur le canevas
    can.config(cursor= 'hand2')

    # on assigne au clic gauche de la souris la procédure move_point
    can.bind("<Button-1>",lambda x:move_point(x,frame,can,list_point,grid_value,numberZoom, inclinaison, x_center, y_center))


###
# Fonction retournant un nombre réel tronqué à la seconde décimale
# Entrée(s) : x: nombre réel
# Retourne(s) : un nombre réel tronqué à la seconde décimale
def clean_float(x):
    return int(x) + float(str(x-int(x))[:4])


###
# Procédure cette procédure ajoute un point du canevas où l'on clique à la
# liste des points de contrôles et l'affiche dans le canevas
# Entrée(s) :   - event: un évènement Tkinter, ici event et le clic gauche, on
#               peut en extraire les coordonnées du clic gauche sur le widgets
#               où il est lié.
#               - frame: le cadre où se trouve le canevas 'can'
#               - can: le canevas principal
#               - list_point: widget Listbox contenant les coordonnées et noms de tout les points
#               - grid_value: la valeur rattachée à la grille
#               - numberZoom: variable stockant le nombre de zoom réalisé
#               - inclinaison_var: variable stockant l'inclinaison du canevas
def add_point(event,frame,can,list_point, grid_value, numberZoom, inclinaison_var):

    # h est la moitié de la hauteur du cadre contenant le canevas can
    # w la moitié de sa Largeur
    # on utilise h et w pour calculer la distance du curseur au centre de du
    # canevas
    h = frame.winfo_height()/2
    w = frame.winfo_width()/2

    # 14.5 et 13 représentent le décalage entre la fenêtre et le curseur en
    # pixels, et on choisit que 10 pixels représentent 1 unité de coordonnées,
    # d'où la division par 10
    x = float(((event.x)+14.5 -w)/10)
    y = float(((event.y)+13 -h)/-10)

    # dans cette partie on modifie les coordonnées  x et y selon le
    # niveau de zoom où on se trouve
    if numberZoom.get() < 0:
        for i in range(0,numberZoom.get(),-1):
            x = x * 1.111
            y = y * 1.111
    elif numberZoom.get() > 0:
        for i in range(0,numberZoom.get(),1):
            x = x * 0.889
            y = y * 0.889

    # dans cette partie on modifie les coordonnées  x et y selon le
    # niveau de rotation où on se trouve
    center = complex(0)
    radian = math.radians(inclinaison_var.get())
    coord = complex(x,y)
    newcoord =  complex(math.cos(radian), math.sin(radian)) * (coord - center) + center
    x = newcoord.real
    y = newcoord.imag

    # on appelle la fonction clean_float qui renvoie le nombre réel tronqué
    # au centième
    x = clean_float(x)
    y = clean_float(y)

    # string.ascii_lowercase est une liste contenant tout l'alphabet en
    # minuscule la fonction choice renvoie un élément aléatoire d'une liste
    # cette ligne assigne donc un nom de deux lettres aléatoirement choisies
    # à notre point
    nom = choice(string.ascii_lowercase) + choice(string.ascii_lowercase)

    # on ajoute dans le widget list_point les coordonnées du point et le nom
    # sous le format 'nom (x,y)'
    list_point.insert(tk.END, nom +' (' + str(x) + ';' + str(y) + ')')


###
# Procédure cette procédure retire un point de la liste des points de
# contrôle sur le canevas proche de là où l'on clique
# Cette procédure procède comme suit: -(1) on récupère les coordonnées de tout
#                           les points de contrôles
#                                     -(2) on prend les points situés dans un
#                           rayon de 10 pixels autour de l'endroit où l'on
#                           clique
#                                    -(3) on supprime le point le plus proche
#                           de l'endroit où l'on clique
# Entrée(s) :   - event: un évènement Tkinter, ici event et le clic gauche, on
#               peut en extraire les coordonnées du clic gauche sur le widgets
#               où il est lié.
#               - frame: le cadre où se trouve le canevas 'can'
#               - can: le canevas principal
#               - list_point: widget Listbox contenant les coordonnées et noms de tout les points
#               - grid_value: la valeur rattachée à la grille
#               - numberZoom: variable stockant le nombre de zoom réalisé
#               - inclinaison_var: variable stockant l'inclinaison du canevas
def del_point(event,frame,can,list_point,grid_value, numberZoom, inclinaison_var):

    # h est la moitié de la hauteur du cadre contenant le canevas can
    # w la moitié de sa Largeur
    # on utilise h et w pour calculer la distance du curseur au centre de du
    # canevas
    h = frame.winfo_height()/2
    w = frame.winfo_width()/2

    # 14.5 et 13 représentent le décalage entre la fenêtre et le curseur en
    # pixels, et on choisit que 10 pixels représentent 1 unité de coordonnées,
    # d'où la division par 10
    x = float(((event.x)+14.5 -w)/10)
    y = float(((event.y)+13 -h)/-10)

    # dans cette partie on modifie les coordonnées  x et y selon le
    # niveau de zoom où on se trouve
    if numberZoom.get() < 0:
        for i in range(0,numberZoom.get(),-1):
            x = x * 1.111
            y = y * 1.111
    elif numberZoom.get() > 0:
        for i in range(0,numberZoom.get(),1):
            x = x * 0.889
            y = y * 0.889

    # dans cette partie on modifie les coordonnées  x et y selon le
    # niveau de rotation où on se trouve
    center = complex(0)
    radian = math.radians(inclinaison_var.get())
    coord = complex(x,y)
    newcoord =  complex(math.cos(radian), math.sin(radian)) * (coord - center) + center
    x_centre = newcoord.real
    y_centre = newcoord.imag

    # étape (1)
    # point_coordinates est une liste qui contiendra les coordonnées de tous
    # les points contenu dans le widget list_point sous forme de tuple (x,y),
    # c'est à dire une liste de la forme [(x1,y1),(x2,y2),..(xn,yn)]
    point_coordinates = []
    for obj in list_point.get(0,tk.END) :
        i=obj.find('(')
        j=obj.find(';')
        k=obj.find(')')
        x=float(obj[i+1:j])
        y=float(obj[1+j:k])
        point_coordinates.append((x,y))

    # étape (2)
    # near_points est une liste contenant les coordonnées des points se situant
    # dans un cercle de rayon 10 pixels autour de l'endroit où l'utilisateur
    # a cliqué
    near_points = []
    index = 0
    for x,y in point_coordinates :
        dx = abs(x_centre-x)
        dy = abs(y_centre-y)
        if dx**2 + dy**2 < 1 :
            near_points.append((x,y,index))
        index = index + 1

    # nearest_points_distance est une liste contenant les distances entre le
    # point où l'on a cliqué et les points les plus proche de l'endroit où l'on
    # a cliqué
    nearest_points_distance = []
    for x,y,i in near_points:
        dx = abs(x_centre-x)
        dy = abs(y_centre-y)
        distance = math.sqrt(dx + dy)
        nearest_points_distance.append((distance,i))

    # étape (3)
    # si la liste des poins les plus proches n'est pas vide on regarde le
    # point le plus proche du point on l'on a cliqué et on le supprime de la
    # liste des points de contrôles
    if nearest_points_distance != [] :
        minimal_distance = min ([x for x in nearest_points_distance[0]])
        for distance,i  in nearest_points_distance:
            if abs(minimal_distance-distance) < 1  :
                index_to_delete = i
                list_point.delete(index_to_delete,None)
                break


###
# Procédure procédure permettant de déplacer un point sur le canevas can
# Entrée(s) :   - event: un évènement Tkinter, ici event et le clic gauche, on
#               peut en extraire les coordonnées du clic gauche sur le widgets
#               où il est lié.
#               - frame: le cadre où se trouve le canevas 'can'
#               - can: le canevas principal
#               - list_point: widget Listbox contenant les coordonnées et noms de tout les points
#               - grid_value: la valeur rattachée à la grille
#               - numberZoom: variable stockant le nombre de zoom réalisé
#               - inclinaison_var: variable stockant l'inclinaison du canevas
#               - x_center,y_center: variable stockant les coordonnées du centre
#               du canevas
def move_point(event,frame,can,list_point,grid_value, numberZoom, inclinaison_var, x_center, y_center):

    # h est la moitié de la hauteur du cadre contenant le canevas can
    # w la moitié de sa Largeur
    # on utilise h et w pour calculer la distance du curseur au centre de du
    # canevas
    h = frame.winfo_height()/2
    w = frame.winfo_width()/2

    # 14.5 et 13 représentent le décalage entre la fenêtre et le curseur en
    # pixels, et on choisit que 10 pixels représentent 1 unité de coordonnées,
    # d'où la division par 10
    x = float(((event.x)+14.5 -w)/10)
    y = float(((event.y)+13 -h)/-10)

    # dans cette partie on modifie les coordonnées  x et y selon le
    # niveau de zoom où on se trouve
    if numberZoom.get() < 0:
        for i in range(0,numberZoom.get(),-1):
            x = x * 1.111
            y = y * 1.111
    elif numberZoom.get() > 0:
        for i in range(0,numberZoom.get(),1):
            x = x * 0.889
            y = y * 0.889

    # dans cette partie on modifie les coordonnées  x et y selon le
    # niveau de rotation où on se trouve
    center = complex(0)
    radian = math.radians(inclinaison_var.get())
    coord = complex(x,y)
    newcoord =  complex(math.cos(radian), math.sin(radian)) * (coord - center) + center
    x_centre = newcoord.real
    y_centre = newcoord.imag

    # les étapes qui suivent sont détaillées dans del_point, pour savoir quel
    #point on bouge on trouve le point le plus proche du curseur au moment où
    #l'on clique
    point_coordinates = []
    for obj in list_point.get(0,tk.END) :
        i=obj.find('(')
        j=obj.find(';')
        k=obj.find(')')
        x=float(obj[i+1:j])
        y=float(obj[1+j:k])
        point_coordinates.append((x,y))


    near_points = []
    index = 0
    for x,y in point_coordinates :
        dx = abs(x_centre-x)
        dy = abs(y_centre-y)
        if dx**2 + dy**2 < 1 :
            near_points.append((x,y,index))
        index = index + 1

    nearest_points_distance = []
    for x,y,i in near_points:
        dx = abs(x_centre-x)
        dy = abs(y_centre-y)
        distance = math.sqrt(dx + dy)
        nearest_points_distance.append((distance,i))
    if nearest_points_distance != [] :
        minimal_distance = min ([x for x in nearest_points_distance[0]])
        for distance,i  in nearest_points_distance:
            if abs(minimal_distance-distance) < 1  :
                index_item = i
                # ici si on bouge la souris après avoir clic gauche la procédure
                # update_point est appelé et modifie les coordonnées du point
                # que l'on bouge dans la listbox list_point ce qui en le bouge
                # dans le canevas can
                can.bind('<B1-Motion>', lambda event: update_point(event, frame,can,list_point,grid_value, numberZoom, inclinaison_var, index_item, x_center, y_center))
                # dès que l'on relâche la souris, on arrêtte d'appeler la
                # procédure update_point
                can.bind('<ButtonRelease-1>', lambda event: can.unbind('<B1-Motion>'))
                break


###
# Procédure procédure qui met à jour les coordonnées d'un point après
#           déplacement ce qui permet un mouvement fluide
# Entrée(s) :   - event: un évènement Tkinter, ici event et le clic gauche, on
#               peut en extraire les coordonnées du clic gauche sur le widgets
#               où il est lié.
#               - frame: le cadre où se trouve le canevas 'can'
#               - can: le canevas principal
#               - list_point: widget Listbox contenant les coordonnées et noms de tout les points
#               - grid_value: la valeur rattachée à la grille
#               - numberZoom: variable stockant le nombre de zoom réalisé
#               - inclinaison_var: variable stockant l'inclinaison du canevas
#               - index : l'indice du point dans la list_point qu'on édite
#               - x_center,y_center: variable stockant les coordonnées du centre
#               du canevas
def update_point(event, frame,can,list_point,grid_value, numberZoom, inclinaison_var, index, x_center, y_center):

    # même suite d'instruction pour obtenir les coordonnées précises du points
    # où le curseur se trouve
    h = frame.winfo_height()/2
    w = frame.winfo_width()/2

    x = float(((event.x)+14.5 -w)/10)
    y = float(((event.y)+13 -h)/-10)

    if numberZoom.get() < 0:
        for i in range(0,numberZoom.get(),-1):
            x = x * 1.111
            y = y * 1.111
    elif numberZoom.get() > 0:
        for i in range(0,numberZoom.get(),1):
            x = x * 0.889
            y = y * 0.889

    center = complex(0)
    radian = math.radians(inclinaison_var.get())
    coord = complex(x,y)
    newcoord =  complex(math.cos(radian), math.sin(radian)) * (coord - center) + center
    x_centre = newcoord.real
    y_centre = newcoord.imag


    # modification des coordonnées du point bougé de la manière suivante,
    # on retient les coordonnées où le curseur est, on retire le point dans la
    # listbox et on le remet avec les coordonnées retenues au même endroit dans
    # la listbox, à l'indice 'index'
    element = list_point.get(index)
    element = element[0: element.find('(')+1] + str(x_centre) + ';' + str(y_centre) + ')'

    list_point.delete(index)
    list_point.insert(index, element)

    # on appelle la fonction displayPoint qui dessine tous les points
    displayPoint(can, list_point, grid_value, inclinaison_var, numberZoom, 'all', x_center, y_center)


###
# Procédure déselectionnant le Radiobutton.
# Entrée(s) :   - rbutton : widget Radiobutton
#               - can : widget Canvas
def deselect_rbutton(rbutton, can):
    rbutton.deselect() # Déselection du Radiobutton
    can.config(cursor= 'arrow') # Changement du curseur
    can.unbind('<Button-1>') # Dissociation de l'event lié à Button-1 sur le Canvas


###
# Procédure déselectionnant tous les Radiobuttons.
# Entrée(s) :   - rbutton_1 : widget Radiobutton
#               - rbutton_2 : widget Radiobutton
#               - rbutton_3 : widget Radiobutton
#               - can : widget Canvas
def deselect_all(rbutton_1, rbutton_2, rbutton_3, can):
    # Déselection des Radiobuttons
    rbutton_1.deselect()
    rbutton_2.deselect()
    rbutton_3.deselect()

    can.config(cursor= 'arrow') # Changement du curseur
    can.unbind('<Button-1>') # Dissociation de l'event lié à Button-1 sur le Canvas


'''
# ========================================== #
# Fonction - Courbe
# ========================================== #
'''

###
# Fonction récupérant les coordonnées
# de tout les points dans le widget Listbox.
# Entrée(s) :   - list_point : widget Listbox
#               - can : widget Canvas
#               - is_open : BooleanVar
# Retourne(s) : - x_coordinates : tableau contenant les coordonnées x
#               - y_coordinates : tableau contenant les coordonnées y
def get_coordinates(list_point,can,is_open):
    # on crée deux listes x_coordinates et y_coordinates qui contiendront
    # les coordonnées en x et en y de tout les points dans le widget list_point
    x_coordinates = []
    y_coordinates = []

    # obj est une chaine de caractère dans laquelle on regarde les indices
    # des parenthèses et des points-virgules  pour sélectionner les bonnes
    # données
    for obj in list_point.get(0,tk.END) :
        i=obj.find('(')
        j=obj.find(';')
        k=obj.find(')')
    # on convertit ces données en flottant pour pouvoir les traiter en tant
    # que valeur numérique, le x10 c'est parce qu'on a choisit que 10 pixels
    # seraient une unité de coordonnées
        x=float(obj[i+1:j])*10
        y=float(obj[1+j:k])*-10

        x_coordinates.append(x)
        y_coordinates.append(y)

    # si on choisit de fermer la courbe, alors on ajoute les coordonnées du
    # premier point en dernier élément des listes x_cooordinates, y_coordinates

    if is_open:
        x_coordinates.append(x_coordinates[0])
        y_coordinates.append(y_coordinates[0])

    return x_coordinates,y_coordinates


###
# Fonction une implémentation de l'algorithme de deCasteljau de manière
# récursive, évalue en un point t, la valeur en x ou en y de la courbe de
# Bézier passant par les points de controles données en paramètres.
#  * si liste est la liste des abscisses de tout les points de controles alors
# deCasteljau renvoie x_c(t) l'abscisse du point de la courbe de Bézier
# correspondant à la valeur de t.
# Entrée(s) :   -liste: une liste de réels, les coordonnées en x ou en y
#               -i: au premier appel, l'indice du premier élément de la liste de
#           coordonnées
#               -j: au premier appel, l'indice du dernier élément de la liste de
#           coordonnées
#               -t: un réel compris entre 0 et 1 inclus
# Retourne(s) : la coordonnée en x ou en y d'un point de la courbe de Bézier
# en t, selon les points de contrôles
def deCasteljau(liste,i,j,t):
    if j == 0:
        return liste[i]
    return deCasteljau(liste,i+1,j-1,t)*t + deCasteljau(liste,i,j-1,t)*(1-t)


###
# Procédure trace, trace la courbe de bérize
# Entrée(s) :   - can: le canevas principal
#               - list_point: widget Listbox contenant les coordonnées et noms de tout les points
#               - degre_var: variable stockant le degré de la courbe que l'on doit évaluer
#               - spinbox_pas: widget contenant la valeur indiquant le pas choisit par l'utilisateur
#               - statut_var: widget contenant la valeur indiquant si la courbe est fermée ou pas
#               - grid_value: la valeur rattachée à la grille
#               - numberZoom: variable stockant le nombre de zoom réalisé
#               - inclinaison_var: variable stockant l'inclinaison du canevas
#               - index : l'indice du point dans la list_point qu'on édite
#               - x_center,y_center: variable stockant les coordonnées du centre
#               du canevas
# Retourne(s) :
def trace(can, combobox_type, degre_var, list_point, spinbox_pas, statut_var, grid_value, inclinaison, numberZoom, x_center, y_center):

    reset_canvas(can, grid_value, 'all')

    # On récupère le type de courbe
    curve_type = combobox_type.get()

    # On récupère le pas, ou plutôt son inverse qui va définir
    # le nombre de points que l'on va calculer
    step = int(pow(float(spinbox_pas.get()),-1))

    # On récupère le paramètre courbe fermée/ouverte
    is_open = statut_var.get()

    # On récupère la liste des coordonnées en x et en y dans deux listes de
    # même taille x_list,y_list
    x_list,y_list = get_coordinates(list_point,can,is_open)

    # On regarde si le type de courbe est 'Bézier' et si la liste des
    # coordonnées n'est pas vide
    if curve_type == 'Bézier' and x_list != []:
        # x_m liste des coordonnées en abscisse des points
        # de la courbe paramètrique
        x_m = []

        # y_m liste des coordonnées en ordonnée des points
        # de la courbe paramètrique
        y_m = []

        for k in range(step+1):

            # t une valeur entre 0 et 1
            t = k/step

            # on appelle la fonction deCasteljau qui évalue en un point t
            # la valeur du polynome caractérisé par les points de contrôles
            # dans x_list et y_list
            x_m.append(deCasteljau(x_list,0,len(x_list)-1,t))
            y_m.append(deCasteljau(y_list,0,len(y_list)-1,t))


            # de manière à ne pas stocker tout les points en même temps
            # dès que la liste x_m contient deux éléments on trace la droite
            # reliant le point (x_m[0],y_m[0]) au point (x_m[1],y_m[1])
            # et on supprime le premier élément des deux listes
            if len(x_m)==2:
                can.create_line(x_m[0],y_m[0],x_m[1],y_m[1])
                x_m.pop(0)
                y_m.pop(0)

    elif curve_type == 'Spline':
        # pas d'implémentation de l'algorithme de DeBoor pour les B-Spline \:
        pass

    displayPoint(can,list_point, None, inclinaison, numberZoom, None, x_center, y_center)



'''
# ========================================== #
# Fonction - Paramètre courbe
# ========================================== #
'''



'''
# ========================================== #
# Fonction - Paramètre fenêtre
# ========================================== #
'''

###
# Procédure centrant la fenêtre.
# Entrée(s) : fen : fenêtre
def center(fen):
    # Mise à jour de l'affichage
    fen.update_idletasks()

    # Récupération de la taille de l'écran
    w = fen.winfo_screenwidth()
    h = fen.winfo_screenheight()

    # Récupération de la taille de la fenêtre
    size = tuple(int(_) for _ in fen.geometry().split('+')[0].split('x'))

    # Coordonnées où le coté haut droit de la fenêtre
    # doit être placé.
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2

    # Placement de la fenêtre
    fen.geometry("%dx%d+%d+%d" % (size + (x, y)))


###
# Procédure réinitialisant la fenêtre
# lors du changement de type de courbe.
# Entrée(s) :   - list_point : widget Listbox
#               - can : widget Canvas
#               - grid_value : widget Combobox
#               - numberZoom : IntVar
#               - inclinaison : IntVar
#               - x_center : IntVar
#               - y_center : IntVar
#               - curve_type : widget Combobox stockant le type de courbe
#               - display_degre : widget Label affichant le degre de la courbe
#               - degre_var : StringVar stockant le degre de la courbe
def update_fen(list_point, can, grid_value, numberZoom, inclinaison, x_center, y_center, curve_type, display_degre, degre_var):
    reset_canvas(can, grid_value, 'all') # Réinistialisation du canvas
    list_point.delete(0,tk.END) # Suppression de tout les éléments de la liste
    numberZoom.set(0) # Compteur du nombre de zoom
    inclinaison.set(0) # Inclinaison du Canvas
    x_center.set(0) # Centre x du Canvas
    y_center.set(0) # Centre y du Canvas

    if curve_type.get() == 'Bézier':
        display_degre.config(state=tk.NORMAL)
        display_degre.config(background='white')
        degre_var.set('')
    else:
        display_degre.config(state=tk.DISABLED)
        display_degre.config(background='#AAAAAA')
        degre_var.set('')

###
# Procédure vérifiant s'il y a un changement
# dans le widget Listbox.
# Entrée(s) :   - number_point : IntVar
#               - can : widget Canvas
#               - list_point : widget Listbox
#               - grid_value : valeur du Combobox quadrillage
#               - numberZoom : IntVar
#               - inclinaison : IntVar
#               - x_center : IntVar
#               - y_center : IntVar
#               - curve_type : widget Combobox stockant le type de courbe
#               - degre_var : StringVar stockant le degre de la courbe
#               - statut_var : BooleanVar stockant de la statut de la courbe (ouverte, fermée)
def check_list_update(number_point, can, list_point, grid_value, numberZoom, inclinaison, x_center, y_center, curve_type, degre_var, statut_var):
    # Si le nombre d'éléments dans la liste change
    if list_point.size() != number_point.get():
        number_point.set(list_point.size()) # Changement du nombre d'élément dans la liste

        # Affichage des points
        displayPoint(can, list_point, grid_value, inclinaison, numberZoom, 'all', x_center, y_center)

        # Changement du degré
        if curve_type.get() == 'Bézier':
            if number_point.get() != 0 and statut_var.get() == False:
                degre_var.set(str(number_point.get()-1))
            elif number_point.get() != 0 and statut_var.get() == True:
                degre_var.set(str(number_point.get()))
            else:
                degre_var.set('')
        else:
            pass

'''
# ========================================== #
# Fonction - Paramètre canvas
# ========================================== #
'''

###
# Procédure réinitialisant le Canvas.
# Entrée(s) :   - can : widget Canvas
#               - grid_value : valeur du Combobox quadrillage
def reset_canvas(can, grid_value, item):
    if grid_value != None:
        # En fonction de grid_value, on associe un certaine valeur
        # à quadrillage
        if grid_value == 'Vide':
            quadrillage = 0
        elif grid_value == 'Axe':
            quadrillage = 1
        elif grid_value == 'Grille (1)':
            quadrillage = 2
        elif grid_value == 'Grille (2)':
            quadrillage = 3
        else:
            quadrillage = 4

        # Suppression des items du Canvas
        can.delete(item)
        x = 1000 # Longueur des axes


        if quadrillage >= 1:
            if quadrillage >= 2:
                if quadrillage == 2:
                    pas = 5
                elif quadrillage == 3:
                    pas = 2
                else:
                    pas = 1

                for i in range(0,(x//5)+1,pas):
                    # Lignes grises
                    can.create_line(-x+10*i,-x,-x+10*i,x,width='1', fill='#DDDDDD')
                    can.create_line(x,-x+10*i,-x,-x+10*i,width='1', fill='#DDDDDD')

            # Tracé des axes et graduations
            can.create_line(0,-x,0,x,fill='black',width='1')
            can.create_line(-x,0,x,0,fill='black',width='1')
            for i in range(x//5):
                can.create_line(-x+10*i,2,-x+10*i,-2,width='2')
                can.create_line(2,-x+10*i,-2,-x+10*i,width='2')

            # Bordure
            can.create_line(x,-x,x,x,fill='black',width='1')
            can.create_line(-x,-x,-x,x,fill='black',width='1')
            can.create_line(-x,x,x,x,fill='black',width='1')
            can.create_line(-x,-x,x,-x,fill='black',width='1')
        else:
            pass


###
# Procédure dessinant tout les points
# dans le widget Listbox.
# Entrée(s) :   - can : widget Canvas
#               - list_point : widget Listbox
#               - grid_value : valeur du Combobox quadrillage
#               - numberZoom : IntVar
#               - inclinaison : IntVar
#               - x_center : IntVar
#               - y_center : IntVar
#               - label_rotation : widget Label
#               - item : Objet sur le Canvas à effacer
# Retourne(s) :
def displayPoint(can, list_point, grid_value, inclinaison, numberZoom, item, x_center, y_center):
    # Réinitialisation du Canvas
    reset_canvas(can, grid_value, item)

    # Récupération des coordonnées de chaque point dans Listbox
    for obj in list_point.get(0,tk.END) :
        i=obj.find('(')
        j=obj.find(';')
        k=obj.find(')')
        x=float(obj[i+1:j])*10
        y=float(obj[1+j:k])*-10

        # Création du point
        can.create_oval(x-2, y-2, x+2, y+2, # Coordonnées
                        fill='red',         # Couleur interne
                        outline='blue',     # Couleur bordure
                        tags='point'        # tag
                        )


    # Zoom du Canvas
    if numberZoom.get() < 0:
        for i in range(0,numberZoom.get(),-1):
            zoom(can, 0.9, None)
    elif numberZoom.get() > 0:
        for i in range(0,numberZoom.get(),1):
            zoom(can, 1.1, None)
    # Rotation des éléments du Canvas
    rotate(can, inclinaison.get(), None, None)
    # Déplacement du Canvas
    move(can, x_center.get(), y_center.get(), None, None)


###
# Procédure centrant le Canvas en fonction de la taille de la fenêtre.
# Entrée(s) :   - frame_canvas : widget Frame contenant le Canvas
#               - can : widget Canvas
#               - fen : fenêtre principale
def center_canvas(frame_canvas, can, fen):
    # Récupération de la taille de la fenêtre
    w_can = (frame_canvas.winfo_width()-20) /2
    h_can = (frame_canvas.winfo_height()-20) /2

    # Centrage du Canvas
    can.configure(scrollregion=(-w_can, -h_can, w_can, h_can))


###
# Procédure modifiant la taille des items.
# Entrée(s) :   - can : widget Canvas
#               - proportion : coefficient d'aggrandissement ou de rétrécissement
#               - numberZoom : IntVar
def zoom(can, proportion, numberZoom):
    # Changement de la taille de tout les items
    can.scale("all", 0, 0, proportion, proportion)

    # Changement du nombre de zoom effectué
    if numberZoom != None:
        if proportion == 1.1:
            numberZoom.set(numberZoom.get()+1)
        elif proportion == 0.9:
            numberZoom.set(numberZoom.get()-1)


###
# Procédure modifiant la positon des points
# par rapport au centre et à l'ange.
# Entrée(s) :   - can : widget Canvas
#               - angle : Variation de l'angle
#               - inclinaison : inclinaison du Canvas
#               - label : widget Label
def rotate(can, angle, inclinaison, label):

    if inclinaison != None:
        # Modification de l'inclinaison du Canvas
        inclinaison.set(inclinaison.get()+angle)
        # Modification du Label
        label.set('Rotation (' + str(inclinaison.get()//360) + 'x360 +' + str(inclinaison.get()%360) + '°)')

    center = complex(0) # Centre du canvas
    radian = math.radians(angle) # Conversion de l'angle
    # Pour chaque item dans le Canvas
    for item_index in can.find_all():
        newxy = [] # Tableau contenant les nouvelles coordonnées de l'item
        xy = can.coords(item_index) # Coordonnées de l'item

        # Si l'item n'a aucun tag (Si ce n'est pas un point)
        if can.gettags(item_index) == ():
            for i in range(0,len(xy),2):
                # Conversion en complexe des coordonnées de l'item
                coord = complex(xy[i], xy[i+1])
                # Calcul des nouvelles coordonnées de l'item
                newcoord =  complex(math.cos(radian), math.sin(radian)) * (coord - center) + center
                newxy.append(newcoord.real)
                newxy.append(newcoord.imag)

        else:
            taille = 2 # Taille des points
            # Conversion en complexe des coordonnées du point
            coord = complex(xy[0]+taille, xy[1]+taille)
            # Calcul des nouvelles coordonnées du point
            newcoord =  complex(math.cos(radian), math.sin(radian)) * (coord - center) + center
            newxy.append(newcoord.real-taille)
            newxy.append(newcoord.imag-taille)
            newxy.append(newcoord.real+taille)
            newxy.append(newcoord.imag+taille)

        # Changement des coordonnées de l'item
        can.coords(item_index, *newxy)


###
# Procédure déplaçant le Canvas
# Entrée(s) :   - can : widget Canvas
#               - x_move : déplacement horizontale
#               - y_move : déplacement verticale
#               - x_var : variable stockant le déplacement totale horizontale
#               - y_var : variable stockant le déplacement totale verticale
def move(can, x_move, y_move, x_var, y_var):

    # Déplacement du Canvas
    can.move('all', x_move, y_move)

    if x_var != None and y_var != None:
        # Changement des variables stockant le déplacement
        x_var.set(x_var.get()+x_move)
        y_var.set(y_var.get()+y_move)


###
# Procédure réinitialisant les paramêtres du Canvas.
# Entrée(s) :   - can : widget Canvas
#               - list_point : widget Listbox
#               - grid_value : valeur du Combobox quadrillage
#               - numberZoom : IntVar
#               - inclinaison : IntVar
#               - x_center : IntVar
#               - y_center : IntVar
#               - label_rotation : widget Label
def reset_option(can, list_point, grid_value, inclinaison, numberZoom, x_center, y_center, label_rotation):
    numberZoom.set(0)
    inclinaison.set(0)
    x_center.set(0)
    y_center.set(0)
    label_rotation.set('Rotation (' + str((inclinaison.get()//360)) + 'x360 +' + str(inclinaison.get()%360) + '°)')

    # Affichage des points
    displayPoint(can,list_point, grid_value, inclinaison, numberZoom, 'all', x_center, y_center)
