# Importation des modules
import tkinter as tk
from tkinter import ttk
from function import *
from functools import partial
import tkinter.font as tkFont
import math

###
# Procédure construisant la fenêtre.
def cons_window():

    # Construction de la fenêtre fen
    fen = tk.Tk()
    # Titre de la fenêtre
    fen.title('Bézier')



    '''
    # ========================================== #
    # Frame canevas
    # ========================================== #
    '''
    # Construction de la frame
    frame_canvas = tk.Frame(fen,                # Parent
                            bd= 2,              # Epaisseur de la bordure
                            relief= 'ridge',    # Type de bordure
                            padx=10,            # Marge horizontal
                            pady=10             # Marge Vertical
                            )

    # Construction du canvas
    can = tk.Canvas(frame_canvas,   # Parent
                    bg='white',     # Couleur du fond
                    width=1,
                    height=1,
                    )


    can.pack(fill=tk.BOTH,  # Remplissage de chaque coté
             expand=1)      # Expansion



    '''
    # ========================================== #
    # Frame interaction
    # ========================================== #
    '''

    # Construction de la frame
    frame_interaction = tk.Frame(fen,               # Parent
                                 bd= 2,             # Epaisseur bordure
                                 relief= 'ridge',   # Type de bordure
                                 padx=10,           # Marge horizontale
                                 pady=10)           # Marge verticale

    # Construction d'une frame temporaire
    # les boutons d'édition des points
    frame_edition_tmp = tk.Frame(frame_interaction)

    # Construction des boutons radios poussoirs ajouter, supprimer et déplacer
    lb_edit = tk.Label(frame_edition_tmp, text='Éditer les points (Décocher avec Clic Droit)')
    edit_var = tk.IntVar() # Variable stockant le mode d'édition
    rbutton_add = tk.Radiobutton(frame_edition_tmp,     # Parent
                                 text='Ajouter',        # Texte affiché
                                 variable=edit_var,     # Variable de contrôle
                                 value=1,               # Valeur du boutons
                                 indicatoron=0,         # Sans indicateur
                                 height=2,               # Hauteur
                                 command =lambda: click_to_add(can,frame_canvas,list_point, combobox_quadrillage.get(), numberZoom, inclinaison_var)
                                 )
    rbutton_add.bind('<Button-3>',lambda event: deselect_rbutton(rbutton_add, can)) # Déselctionne le bouton avec un click droit
    rbutton_del = tk.Radiobutton(frame_edition_tmp,     # Parent
                                 text='Supprimer',      # Texte affiché
                                 variable=edit_var,     # Variable de contrôle
                                 value=2,               # Valeur du boutons
                                 indicatoron=0,         # Sans indicateur
                                 height=2,              # Hauteur
                                 command =lambda: click_to_del(can,frame_canvas,list_point,combobox_quadrillage.get(), numberZoom, inclinaison_var)
                                 )
    rbutton_del.bind('<Button-3>',lambda event: deselect_rbutton(rbutton_del, can)) # Déselctionne le bouton avec un click droit
    rbutton_move = tk.Radiobutton(frame_edition_tmp,    # Parent
                                  text='Déplacer',      # Texte affiché
                                  variable=edit_var,    # Variable de contrôle
                                  value=3,              # Valeur du boutons
                                  indicatoron=0,        # Sans indicateur
                                  height=2,             # Hauteur
                                  command =lambda: click_to_move(can,frame_canvas,list_point,combobox_quadrillage.get(), numberZoom, inclinaison_var, x_center, y_center)
                                  )
    rbutton_move.bind('<Button-3>',lambda event: deselect_rbutton(rbutton_move, can)) # Déselctionne le bouton avec un click droit

    # Placement des boutons dans la frame edition_tmp
    lb_edit.pack(anchor='w')        # Positonner à droite
    rbutton_add.pack(fill=tk.BOTH,  # Remplissage de chaque coté
                     expand=1,      # Expansion
                     pady=2)        # Marge verticale
    rbutton_del.pack(fill=tk.BOTH,  # Remplissage
                     expand=1,      # Expansion
                     pady=2)        # Marge verticale
    rbutton_move.pack(fill=tk.BOTH, # Remplissage de chaque coté
                      expand=1,     # Expansion
                      pady=2)       # Marge verticale


    # Construction d'une frame temporaire
    # contenant le label et les boutons zoom
    frame_zoom_tmp = tk.Frame(frame_interaction)

    # Création de la police
    font = tkFont.Font(size=12,         # Taille
                       weight='bold'    # Gras
    )

    numberZoom = tk.IntVar() # Variable stockant le nombre de zoom réalisé
    numberZoom.set(0)
    # Construction du label zoom et des boutons + et -
    lb_zoom = tk.Label(frame_zoom_tmp, text= 'Zoom')

    button_zoomPlus = tk.Button(frame_zoom_tmp, # Parent
                                text='+',       # Texte
                                font=font,      # Police utilisée

                                height=2,       # Hauteur
                                command= partial(zoom, can, 1.1, numberZoom)
                                )
    button_zoomPlus.bind('<Button-1>', lambda event: deselect_all(rbutton_add, rbutton_del, rbutton_move, can)) # Déselection des boutons éditer les points
    button_zoomMoins = tk.Button(frame_zoom_tmp,    # Parent
                                 text='-',          # Texte
                                 font=font,         # Police utilisée

                                 height=2,          # Hauteur
                                 command= partial(zoom, can, 0.9, numberZoom)
                                 )
    button_zoomMoins.bind('<Button-1>', lambda event: deselect_all(rbutton_add, rbutton_del, rbutton_move, can)) # Déselection des boutons éditer les points

    # Placement dans la frame temporaire zoom
    lb_zoom.pack(anchor='w')                # Positonner à gauche
    button_zoomPlus.pack(side=tk.LEFT,      # Positionnement par rapport à gauche
                         fill=tk.BOTH,      # Remplissage de chaque coté
                         expand=1           # Expansion
                         )
    button_zoomMoins.pack(side=tk.RIGHT,    # Positionnement par rapport à droite
                          fill=tk.BOTH,     # Remplissage de chaque coté
                          expand=1          # Expansion
                          )


    # Construction d'une frame temporaire
    # contenant le label et le ... translation
    frame_translation_tmp = tk.Frame(frame_interaction)

    # Initialisation des variables de contrôle
    # Stockant le centre du canvas
    x_center = tk.IntVar()
    x_center.set(0)
    y_center = tk.IntVar()
    y_center.set(0)

    pas = 30 # Pas de déplacement du canvas

    # Construction du label translation et ...
    lb_translation = tk.Label(frame_translation_tmp, text='Translation')

    button_leftup = tk.Button(frame_translation_tmp, width= 10, height= 2, text='↖',
                              command= lambda: move(can, pas, pas, x_center, y_center))
    button_leftup.bind('<Button-1>', lambda event: deselect_all(rbutton_add, rbutton_del, rbutton_move, can)) # Déselection des boutons éditer les points

    button_up = tk.Button(frame_translation_tmp, width= 10, height= 2, text='↑',
                          command= lambda: move(can, 0, pas, x_center, y_center))
    button_up.bind('<Button-1>', lambda event: deselect_all(rbutton_add, rbutton_del, rbutton_move, can)) # Déselection des boutons éditer les points

    button_rightup = tk.Button(frame_translation_tmp, width= 10, height= 2, text='↗',
                               command= lambda: move(can, -pas, pas, x_center, y_center))
    button_rightup.bind('<Button-1>', lambda event: deselect_all(rbutton_add, rbutton_del, rbutton_move, can)) # Déselection des boutons éditer les points

    button_left = tk.Button(frame_translation_tmp, width= 10, height= 2, text='←',
                            command= lambda: move(can, pas, 0, x_center, y_center))
    button_left.bind('<Button-1>', lambda event: deselect_all(rbutton_add, rbutton_del, rbutton_move, can)) # Déselection des boutons éditer les points

    button_right = tk.Button(frame_translation_tmp, width= 10, height= 2, text='→',
                             command= lambda: move(can, -pas, 0, x_center, y_center))
    button_right.bind('<Button-1>', lambda event: deselect_all(rbutton_add, rbutton_del, rbutton_move, can)) # Déselection des boutons éditer les points

    button_leftdown = tk.Button(frame_translation_tmp, width= 10, height= 2, text='↙',
                                command= lambda: move(can, pas, -pas, x_center, y_center))
    button_leftdown.bind('<Button-1>', lambda event: deselect_all(rbutton_add, rbutton_del, rbutton_move, can)) # Déselection des boutons éditer les points

    button_down = tk.Button(frame_translation_tmp, width= 10, height= 2, text='↓',
                            command= lambda: move(can, 0, -pas, x_center, y_center))
    button_down.bind('<Button-1>', lambda event: deselect_all(rbutton_add, rbutton_del, rbutton_move, can)) # Déselection des boutons éditer les points

    button_rightdown = tk.Button(frame_translation_tmp, width= 10, height= 2, text='↘',
                                 command= lambda: move(can, -pas, -pas, x_center, y_center))
    button_rightdown.bind('<Button-1>', lambda event: deselect_all(rbutton_add, rbutton_del, rbutton_move, can)) # Déselection des boutons éditer les points

    # Placement dans la frame temporaire translation
    lb_translation.grid(row=0,      # Ligne
                        column=0,   # Colonne
                        sticky='w', # Positionnement à gauche
                        columnspan=3 # Nombre de colonne occupé
                        )
    button_leftup.grid(row=1, column=0, padx=1, pady=1, sticky= 'nswe')
    button_up.grid(row=1, column=1, padx=1, pady=1, sticky= 'nswe')
    button_rightup.grid(row=1, column=2, padx=1, pady=1, sticky= 'nswe')
    button_left.grid(row=2, column=0, padx=1, pady=1, sticky= 'nswe')
    button_right.grid(row=2, column=2, padx=1, pady=1, sticky= 'nswe')
    button_leftdown.grid(row=3, column=0, padx=1, pady=1, sticky= 'nswe')
    button_down.grid(row=3, column=1, padx=1, pady=1, sticky= 'nswe')
    button_rightdown.grid(row=3, column=2, padx=1, pady=1, sticky= 'nswe')

    # Configuration de des lignes de la frame
    frame_translation_tmp.rowconfigure(0, weight=1)
    frame_translation_tmp.rowconfigure(1, weight=1)
    frame_translation_tmp.rowconfigure(2, weight=1)
    frame_translation_tmp.rowconfigure(3, weight=1)

    # Construction d'une frame temporaire
    # contenant le label et l'échelle rotation
    frame_rotation_tmp = tk.Frame(frame_interaction)

    inclinaison_var = tk.IntVar() # Variable stockant l'inclinaison du canvas
    inclinaison_var.set(0)
    lb_rotation_var = tk.StringVar() # Variable stockant le texte du label
    lb_rotation_var.set('Rotation (' + str(inclinaison_var.get()//360) + 'x360 +' + str(inclinaison_var.get()%360) + '°)')

    # Construction du label 'Rotation' et de l'échelle allant de 0 à 360.
    lb_rotation = tk.Label(frame_rotation_tmp, textvariable= lb_rotation_var)

    icon_1 = tk.PhotoImage(file="icon/rotate_right.png") # Création d'une image
    button_rotateRight = tk.Button(frame_rotation_tmp, # Parent
                                   font=font,          # Police utilisée
                                   image= icon_1,      # Icon dans le bouton
                                   command= partial(rotate, can, 10, inclinaison_var, lb_rotation_var)
                                  )
    button_rotateRight.bind('<Button-1>', lambda event: deselect_all(rbutton_add, rbutton_del, rbutton_move, can)) # Déselection des boutons éditer les points
    icon_2 = tk.PhotoImage(file="icon/rotate_left.png") # Création d'une image
    button_rotateLeft = tk.Button(frame_rotation_tmp,    # Parent
                                  font=font,             # Police utilisée
                                  image= icon_2,         # Icon dans le bouton
                                  command= partial(rotate, can, -10, inclinaison_var, lb_rotation_var)
                                 )
    button_rotateLeft.bind('<Button-1>', lambda event: deselect_all(rbutton_add, rbutton_del, rbutton_move, can)) # Déselection des boutons éditer les points


    # Placement dans la frame temporaire rotation
    lb_rotation.pack(anchor='w')        # Position à gauche
    button_rotateRight.pack(side=tk.LEFT,      # Positionnement par rapport à gauche
                            fill=tk.BOTH,      # Remplissage de chaque coté
                            expand=1           # Expansion
                           )
    button_rotateLeft.pack(side=tk.RIGHT,    # Positionnement par rapport à droite
                           fill=tk.BOTH,     # Remplissage de chaque coté
                           expand=1          # Expansion
                           )


    # Construction d'une frame temporaire
    # contenant le label frame et le combobox
    frame_quadrillage_tmp = tk.Frame(frame_interaction)

    # Construction du label 'Quadrillage' et du combobox
    lb_quadrillage = tk.Label(frame_quadrillage_tmp, text='Quadrillage')
    tab_quadrillage = ['Vide', 'Axe', 'Grille (1)','Grille (2)', 'Grille (3)'] # Tableau des type de courbe
    combobox_quadrillage = ttk.Combobox(frame_quadrillage_tmp,                                                          # Parent
                                        values=tab_quadrillage,                                                         # Valeur du widget
                                        postcommand= lambda: deselect_all(rbutton_add, rbutton_del, rbutton_move, can)  # Deselection des radio boutons
                                        )
    combobox_quadrillage.set('Vide')  # Valeur affiché, mis en place
    combobox_quadrillage.bind('<<ComboboxSelected>>',lambda event: displayPoint(can, list_point, combobox_quadrillage.get(), inclinaison_var, numberZoom, 'all', x_center, y_center)) # Fonction executé

    # Placement dans la frame temporaire quadrillage
    lb_quadrillage.pack(anchor='w')                 # Position à gauche

    combobox_quadrillage.pack(fill=tk.X, pady=2)    # Remplissage horizontal et marge verticale

    # Création d'un bouton pour reset les paramêtres du canvas
    button_resetCanvas = tk.Button(frame_interaction,
                                   text='Réinitialiser',
                                   height = 2,
                                   command= lambda: reset_option(can, list_point, combobox_quadrillage.get(), inclinaison_var, numberZoom, x_center, y_center, lb_rotation_var))

    # Placement des widgets dans la frame interaction
    frame_edition_tmp.pack(fill=tk.BOTH,        # Remplissage de chaque coté
                           expand=1,            # Expansion
                           pady=15)             # Marge verticale
    frame_zoom_tmp.pack(fill=tk.BOTH,           # Remplissage de chaque coté
                        expand=1,               # Expansion
                        pady=15)                # Marge verticale
    frame_translation_tmp.pack(fill=tk.BOTH,    # Remplissage de chaque coté
                               expand=1,        # Expansion
                               pady=15)         # Marge verticale
    frame_rotation_tmp.pack(fill=tk.BOTH,       # Remplissage de chaque coté
                            expand=1,           # Expansion
                            pady=15)            # Marge verticale
    frame_quadrillage_tmp.pack(fill=tk.BOTH,    # Remplissage de chaque coté
                               expand=1,        # Expansion
                               pady=15)         # Marge verticale
    button_resetCanvas.pack(fill=tk.BOTH,       # Remplissage de chaque coté
                            expand=1,           # Expansion
                            pady=15)            # Marge verticale

    # Configuration de la taille des lignes et des colonnes
    # dans frame_interaction
    frame_interaction.rowconfigure(0, weight=1) # Taille de la ligne
    frame_interaction.rowconfigure(1, weight=1) # Taille de la ligne
    frame_interaction.rowconfigure(2, weight=1) # Taille de la ligne
    frame_interaction.rowconfigure(3, weight=1) # Taille de la ligne
    frame_interaction.rowconfigure(4, weight=1) # Taille de la ligne
    frame_interaction.rowconfigure(5, weight=1) # Taille de la ligne



    '''
    # ========================================== #
    # Frame liste des points
    # ========================================== #
    '''

    # Construction de la frame
    frame_listPoint = tk.Frame(fen,                 # Parent
                               bd= 2,               # Epaisseur de la bordure
                               relief= 'ridge',     # Type de bordure
                               padx=10,             # Marge horizontale
                               pady=10)             # Marge horizontale


    # Construction du label liste de de film
    lb_listPoint = tk.Label(frame_listPoint, text='Liste des points')


    # Construction d'une frame temporaire contenant la liste et la scrollbar
    frame_list_tmp = tk.Frame(frame_listPoint)

    # Construction de la liste et de la scrollbar
    scrollbar_list = tk.Scrollbar(frame_list_tmp,       # Parent
                                  orient= tk.VERTICAL,  # Orientation
                                  jump= 1)              # Saut
    number_point = tk.IntVar() # Variable stockant le nombre de point dans la liste
    number_point.set(0)
    list_point = tk.Listbox(frame_list_tmp,                     # Parents
                            yscrollcommand=scrollbar_list.set,  # Défilement verticale
                            selectmode= 'single',               # Type de sélection
                            activestyle= 'none',                # Style de sélection
                            width=40,                           # Largeur
                            )
    scrollbar_list.config(command=list_point.yview) # Association de la scrollbar à la liste


    # Placement dans la frame temporaire list
    scrollbar_list.pack(fill=tk.Y,      # Remplissage verticale
                        side=tk.RIGHT)  # Positionnement à droite
    list_point.pack(fill=tk.BOTH,       # Remplissage de chaque coté
                    expand=1)           # Expansion

    # Construction d'une frame temporaire
    # contenant les boutons ajouter et supprimer
    frame_editList_1_tmp = tk.Frame(frame_listPoint)

    # Construction des boutons ajouter et supprimer
    button_add = tk.Button(frame_editList_1_tmp,                                                            # Parent
                           text='Ajouter',                                                                  # Texte sur le bouton
                           height=2,                                                                        # Hauteur
                           width=1,                                                                         # Epaisseur
                           command= lambda: list_add_point(list_point, fen))    # Fonction associé au bouton
    button_remove = tk.Button(frame_editList_1_tmp,                             # Parent
                              text='Supprimer',                                 # Texte sur le bouton
                              height=2,                                         # Hauteur
                              width=1,                                          # Largeur
                              command= lambda: list_delete_point(list_point))   # Fonction associé au bouton

    # Placement dans la frame temporaire editList_1_tmp
    button_add.pack(side=tk.LEFT,   # Positionnement à gauche
                    fill=tk.X,      # Remplissage horizontale
                    expand=1,       # Expansion
                    padx=2,         # Marge horizontale
                    pady=2)         # Marge verticale
    button_remove.pack(side=tk.RIGHT,   # Positionnement à droite
                       fill=tk.X,       # Remplissage horizontale
                       expand=1,        # Expansion
                       padx=2,          # Marge horizontale
                       pady=2)          # Marge verticale


    # Construction d'une frame temporaire
    # contenant les boutons ajouter et supprimer
    frame_editList_2_tmp = tk.Frame(frame_listPoint)

    # Construction des boutons déplacer vers le haut et vers le bas
    button_moveUp = tk.Button(frame_editList_2_tmp,                     # Parent
                              text='↑',                                 # Texte sur le bouton
                              height=2,                                 # Hauteur
                              width=1,                                  # Epaisseur
                              command= partial(move_up, list_point)     # Fonction associé au bouton
                              )
    button_moveDown = tk.Button(frame_editList_2_tmp,                   # Parent
                                text='↓',                               # Texte sur le bouton
                                height=2,                               # Hauteur
                                width=1,                                # Epaisseur
                                command= partial(move_down, list_point) # Fonction associé au bouton
                                )

    # Placement dans la frame temporaire editList_2_tmp
    button_moveUp.pack(side=tk.LEFT,        # Positionnement par rapport à gauche
                       fill=tk.X,           # Remplissage horizontale
                       expand=1,            # Expansion
                       padx=2,              # Marge horizontale
                       pady=2)              # Marge verticale
    button_moveDown.pack(side=tk.RIGHT,     # Positionnement par rapport à droite
                         fill=tk.X,         # Remplissage horizontale
                         expand=1,          # Expansion
                         padx=2,            # Marge horizontale
                         pady=2)            # Marge verticale


    # Placement dans la frame listePoint
    lb_listPoint.pack(anchor='w')   # Positionnement à gauche
    frame_list_tmp.pack(fill=tk.BOTH,   # Remplissage de chaque coté
                        expand=1,       # Expansion
                        pady=2)         # Marge verticale
    frame_editList_1_tmp.pack(fill=tk.X)    # Remplissage horizontale
    frame_editList_2_tmp.pack(fill=tk.X)    # Remplissage horizontale


    # Configuration de la taille des lignes et des colonnes
    # dans frame_listPoint
    frame_listPoint.rowconfigure(1, weight=1)   # Taille de la ligne
    frame_listPoint.rowconfigure(2, weight=0)   # Taille de la ligne



    '''
    # ========================================== #
    # Frame option
    # ========================================== #
    '''

    # Construction de la frame
    frame_option = tk.Frame(fen,                # Parent
                            bd= 2,              # Epaisseur de la bordure
                            relief= 'ridge',    # Type de bordure
                            padx=10,            # Marge horizontale
                            pady=10)            # Marge verticale

    # Construction du combobox et du label type de courbe
    lb_type = tk.Label(frame_option, text='Type de courbe')
    tab_type = ['Bézier', 'Spline (HS)', 'B-spline (HS)','Nurb (HS)'] # Tableau des type de courbe
    combobox_type = ttk.Combobox(frame_option,      # Parent
                                 values=tab_type,   # Valeur du widget
                                 )
    combobox_type.set('Bézier')  # Valeur affiché, mis en place
    combobox_type.bind('<<ComboboxSelected>>',lambda event: update_fen(list_point,
                                                                       can,
                                                                       combobox_quadrillage.get(),
                                                                       numberZoom,
                                                                       inclinaison_var,
                                                                       x_center,
                                                                       y_center,
                                                                       combobox_type,
                                                                       display_degre,
                                                                       degre_var
                                                                       ))

    # Construction du spinbox et du label degré
    lb_degre = tk.Label(frame_option, text='Degré')
    degre_var = tk.StringVar() # Variable stockant le degre
    degre_var.set(' ')
    display_degre = tk.Label(frame_option, textvariable= degre_var, bg = 'white', width=20, anchor= 'w', bd= 1, relief= 'sunken')
    # spinbox_degre = tk.Spinbox(frame_option,            # Parent
    #                            textvariable= degre_var, # Variable de contrôle
    #                            from_=1,                 # Début
    #                            to=4,                    # Fin
    #                            increment=1              # Pas
    #                            )

    # Construction du LabelFrame et des boutons radios courbe ouverte ou fermée
    lbFrame_statut = tk.LabelFrame(frame_option, text='Courbe')

    statut_var = tk.BooleanVar() # Variable stockant le statut de la courbe
    statut_var.set(False) # Mise en place de la variable
    rbutton_open = tk.Radiobutton(lbFrame_statut,       # Parent
                                  text='Ouverte',       # Texte affiché
                                  variable=statut_var,  # Variable de contrôle
                                  value=False)          # Valeur du bouton radio
    rbutton_close = tk.Radiobutton(lbFrame_statut,      # Parent
                                   text='Fermée',       # Texte affiché
                                   variable=statut_var, # Variable de contrôle
                                   value=True)          # Valeur du bouton radio

    # Placement dans lbFrame_statut
    rbutton_open.grid(row=0,        # Ligne
                      sticky='w',   # Coller à gauche
                      padx=10,      # Marge horizontale
                      pady=5)       # Marge verticale
    rbutton_close.grid(row=1,       # Ligne
                       sticky='w',  # Coller à gauche
                       padx=10,     # Marge horizontale
                       pady=5)      # Marge verticale

    # Construction du spinbox et du label pas
    lb_pas = tk.Label(frame_option, text='Pas')
    tab_pas = ['0.01', '0.05', '0.1', '0.5', '1'] # Tableau des tailles de pas
    spinbox_pas = tk.Spinbox(frame_option,      # Parent
                             values=tab_pas)    # Valeurs du widget

    # Placement des widgets dans la frame option
    lb_type.grid(row=0, column=0,   # Ligne et colonne
                 sticky='w',        # Coller à gauche
                 padx=10)           # Marge horizontale

    combobox_type.grid(row=1, column=0, # Ligne et colonne
                       padx=15,         # Marge horizontale
                       sticky='we')     # Coller à gauche et à droite

    lb_degre.grid(row=0, column=1,  # Ligne et colonne
                  sticky='w',       # Marge horizontale
                  padx=10)          # Marge horizontale

    display_degre.grid(row=1, column= 1,    # Ligne et colonne
                       padx=15,             # Marge horizontale
                       sticky='we')         # Coller à gauche et à droite

    lbFrame_statut.grid(row= 0, column=2,   # Ligne et colonne
                        sticky='we',        # Coller à gauche et à droite
                        padx=10,            # Marge horizontale
                        rowspan=2)          # Place de la ligne

    lb_pas.grid(row=0, column=3,    # Ligne et colonne
                sticky='w',         # Coller à gauche
                padx=10)            # Marge horizontale

    spinbox_pas.grid(row=1, column= 3,      # Ligne et colonne
                     padx=15,               # Marge horizontale
                     sticky='we')           # Coller à gauche et à droite



    # Configuration de la taille des lignes et des colonnes
    # dans frame_option
    frame_option.columnconfigure(0, weight=1) # Taille de la colonne
    frame_option.columnconfigure(1, weight=1) # Taille de la colonne
    frame_option.columnconfigure(2, weight=1) # Taille de la colonne
    frame_option.columnconfigure(3, weight=1) # Taille de la colonne
    frame_option.rowconfigure(0, weight=1) # Taille de la ligne
    frame_option.rowconfigure(1, weight=1) # Taille de la ligne



    '''
    # ========================================== #
    # Frame courbe
    # ========================================== #
    '''

    # Construction de la frame
    frame_courbe = tk.Frame(fen,                # Parent
                            bd= 2,              # Epaisseur bordure
                            relief= 'ridge',    # Type bordure
                            padx=10,            # Marge horizontale
                            pady=10)            # Marge verticale

    # Construction des boutons tracer et effacer
    button_trace = tk.Button(frame_courbe,  # Parent
                             text='Tracer', # Texte affiché
                             command=lambda : trace(can,combobox_type,degre_var,list_point,spinbox_pas,statut_var, combobox_quadrillage.get(), inclinaison_var, numberZoom, x_center, y_center))
    button_erase = tk.Button(frame_courbe,      # Parent
                             text='Effacer',    # Texte affiché
                             command=lambda : displayPoint(can, list_point, combobox_quadrillage.get(), inclinaison_var, numberZoom, 'all', x_center, y_center))

    # Placement des widgets dans la frame courbe
    button_trace.pack(fill=tk.BOTH, # Remplissage de chaque coté
                      pady=2,       # Marge verticale
                      expand=1      # Expansion
                      )
    button_erase.pack(fill=tk.BOTH, # Remplissage de chaque coté
                      pady=2,       # Marge verticale
                      expand=1)     # Expansion



    '''
    # ========================================== #
    # Boutton quitter
    # ========================================== #
    '''

    # Construction du bouton quitter
    button_quit = tk.Button(fen,                # Parent
                            text='Quitter',     # Texte affiché
                            height=2,           # Hauteur
                            activebackground='#FF3333', # Couleur du bouton active
                            command=quit
                            )



    '''
    # ========================================== #
    # Placement dans la fenêtre
    # ========================================== #
    '''

    frame_interaction.grid(row=0,column=0,  # Ligne 0 colonne 0
                           padx=10,         # Marge horizontale
                           pady=10,         # Marge verticale
                           sticky='nswe')   # Coller à chaque coté
    frame_canvas.grid(row=0, column= 1,     # Ligne 0 colonne 1
                      padx=10,              # Marge horizontale
                      pady=10,              # Marge verticale
                      sticky='nswe')        # Coller à chaque coté
    frame_listPoint.grid(row=0,column=2,    # Ligne 0 colonne 2
                         padx=10,           # Marge horizontale
                         pady=10,           # Marge verticale
                         sticky='nswe')     # Coller à chaque coté
    frame_option.grid(row=1,column=0,       # Ligne 1 colonne 0
                      padx=10,              # Marge horizontale
                      pady=10,              # Marge verticale
                      columnspan=2,         # Nombre de colonne occupé
                      sticky='nswe')        # Coller à chaque coté
    frame_courbe.grid(row=1, column=2,      # Ligne 1 colonne 2
                      padx=10,              # Marge horizontale
                      pady=10,              # Marge verticale
                      sticky='nswe')        # Coller à chaque coté
    button_quit.grid(row=2, column=0,       # Ligne 2 colonne 0
                     columnspan=3,          # Nombre de colonne occupé
                     sticky='nswe',         # Coller à chaque coté
                     padx=10,               # Marge horizontale
                     pady=10)               # Marge verticale



    '''
    # ========================================== #
    # Configuration de la taille des lignes et des colonnes
    # dans la fenêtre
    # ========================================== #
    '''

    fen.columnconfigure(0, weight=0) # Taille de la colonne
    fen.columnconfigure(1, weight=1) # Taille de la colonne
    fen.columnconfigure(2, weight=0) # Taille de la colonne
    fen.rowconfigure(0, weight=1) # Taille de la ligne
    fen.rowconfigure(1, weight=0) # Taille de la ligne
    fen.rowconfigure(2, weight=0) # Taille de la ligne


    '''
    # ========================================== #
    # Autres
    # ========================================== #
    '''
    # Association à la fenêtre la fonction check_list_update
    # qui est appelé à chaque clique droit, dé-clique droit, appuie sur le clavier, entrer de la souris dans la fenêtre
    fen.bind('<Button-1>', lambda event: check_list_update(number_point, can, list_point, combobox_quadrillage.get(), numberZoom, inclinaison_var, x_center, y_center, combobox_type, degre_var, statut_var))
    fen.bind('<ButtonRelease-1>', lambda event: check_list_update(number_point, can, list_point, combobox_quadrillage.get(), numberZoom, inclinaison_var, x_center, y_center, combobox_type, degre_var, statut_var))
    fen.bind('<Key>', lambda event: check_list_update(number_point, can, list_point, combobox_quadrillage.get(), numberZoom, inclinaison_var, x_center, y_center, combobox_type, degre_var, statut_var))
    fen.bind('<Enter>', lambda event: check_list_update(number_point, can, list_point, combobox_quadrillage.get(), numberZoom, inclinaison_var, x_center, y_center, combobox_type, degre_var, statut_var))

    # Mise en place de la dimension minimum de la fenêtre
    fen.update_idletasks() # Mise à jour de l'affichage
    fen.minsize(width=fen.winfo_width(), height=fen.winfo_height()) # Taille minimale de la fenêtre

    # Centrage de la fenêtre
    center(fen)

    # Association à la fenêtre la fonction update_canvas
    # qui est appelé à chaque redimensionnement de la fenêtre
    fen.bind("<Configure>", lambda event: center_canvas(frame_canvas, can, fen))

    # Lancement de la boucle princpal
    fen.mainloop()


if __name__ == "__main__":
    # Création de la fenêtre
    cons_window()
