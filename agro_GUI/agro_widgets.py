# coding: utf8
"""
Created on Thu Feb 25 16:41:46 2016

@author: chmartin
"""
from tkinter import *

from agro_GUI.agro_calendar import Calendar

import calendar


class InputError(Exception):
    """Exception à lever lors d'erreurs sur les paramètres

    Attributs:
        message -- message explicatif
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class Agro_App(Tk):
    """Classe principale de création et gestion de fenêtre

    Attributs:
        titre -- titre de la fenêtre dans le bandeau
        var_datas -- dictionnaire des variables ratachées au différents champs
        de saisie présents dans la fenêtre
        datas -- données récupérées à un instant particulier
        ind_ligne -- compteur de lignes pour la mise en page dans la fenêtre
        (TO DO --> attribut privé)
    """

    def __init__(self, titre):
        """
        Constructeur
        titre : string -- titre que l'on voir figurer dans le bandeau de la
        fenêtre que l'on veut créer
        """
        super(Agro_App, self).__init__()
        self.title(titre)

        self.var_datas = {}
        self.datas = {}
        self.ind_ligne = 0
        vsb = Scrollbar(self, orient=VERTICAL)
        vsb.grid(row=0, column=1, sticky=N+S)
        hsb = Scrollbar(self, orient=HORIZONTAL)
        hsb.grid(row=1, column=0, sticky=E+W)
        self.canvas = Canvas(self, borderwidth=2, background='white',
                                yscrollcommand=vsb.set,
                                xscrollcommand=hsb.set)
        vsb.config(command=self.canvas.yview)
        hsb.config(command=self.canvas.xview)
        self.canvas.grid(row=0, column=0, sticky=N+S+E+W)

        self.window = Frame(self.canvas)
        self.canvas.create_window(0, 0,  window=self.window)

        Frame(self.window, width=self.winfo_screenwidth() - 50, height=2,
                bg='#778899').grid(row=0, columnspan=3, sticky=N + E + W)
        Frame(self.window, width=self.winfo_screenwidth() - 50, height=2,
                bg='#778899').grid(row=2, columnspan=3, sticky=S + E + W)
        Frame(self.window, width=2, height=self.winfo_screenheight() - 130,
                bg='#778899').grid(row=1, column=0, sticky=N + S + W)
        Frame(self.window, width=2, height=self.winfo_screenheight() - 130,
                bg='#778899').grid(row=1, column=2, sticky=N + S + E)

        self.clear()

    def manage_view(self):
        """
        Méthode de mise à jour de la dimension et du focus de la fenêtre
        A appeler chaque fois que l'on modifie le contenu de la fenêtre
        """
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.xview_moveto(0.0)
        self.canvas.yview_moveto(0.0)

        root_height = self.winfo_screenheight() - 100
        root_width = self.winfo_screenwidth() - 25

        self.geometry(str(root_width)+"x"+str(root_height)+"+10+10")
        self.maxsize(self.frame.winfo_reqwidth() + 25,
                     self.frame.winfo_reqheight() + 25)
        self.minsize(root_width, root_height)

        for i in range(self.ind_ligne):
            Grid.rowconfigure(self.frame, i, weight=1)

        Grid.columnconfigure(self.frame, 0, weight=1)

    def show(self):
        """
        Méthode d'affichage de la fenêtre
        A appeler une unique fois après avoir mis en place le premier contenu
        de la fenêtre
        Cette méthode lance la boucle d'évènement de la fenêtre
        """
        self.mainloop()

    def clear(self):
        """
        Méthode de suppression du contenu de la fenêtre
        Elle supprime la totalité de son contenu
        """
        self.var_datas = {}
        self.ind_ligne = 0
        try:
            self.frame.destroy()
        except:
            pass
        finally:

            self.frame = Frame(self.window)
            self.frame.grid(row=1, column=1, sticky=N + S + E + W)

            Grid.rowconfigure(self, 0, weight=1)
            Grid.columnconfigure(self, 0, weight=1)

    ###########################################################################
    #           Gestion des données                                           #
    ###########################################################################

    def remove_datas(self):
        self.var_datas = {}
        self.datas = {}

    def get_datas(self):
        """
        Méthode de récupération des données saisies dans les différents champs
        présents dans la fenêtre au moment où la méthode est déclenchée
        """
        for key, value in self.var_datas.items():

            if isinstance(value, list) and len(value) == 2:

                liste, list_valeurs = value
                self.datas[key] = [list_valeurs[ind]
                                   for ind in liste.curselection()]
            elif isinstance(value, Listbox):

                self.datas[key] = [value.get(ind)
                                   for ind in value.curselection()]
            elif isinstance(value, list) and len(value) == 3:

                label_value = value[0].get()
                if label_value:
                    ind_value = value[1].index(label_value)
                    self.datas[key] = value[2][ind_value]
                else:
                    self.datas[key] = None
            elif isinstance(value, Text):
                self.datas[key] = value.get('1.0', END)
                
                if self.datas[key][-1]=='\n' :
                    self.datas[key]=self.datas[key][:-1]
                    
                #self.datas[key] = self.datas[key].replace('\n', '')
            elif isinstance(value, Calendar):
                self.datas[key] = value.selection
            else:
                self.datas[key] = value.get()
        self.var_datas = {}

    ###########################################################################
    #           Mise en forme                                                 #
    ###########################################################################

    def inserer_text(self, text, pos='LEFT'):
        """
        Méthode d'insertion d'un texte dans la fenêtre avec une police par
        défaut
        text : string -- paramètre obligatoire qui représente le texte que l'on
        veut ajouter
        pos : string -- paramètre optionnel permettant de préciser le
        positionnement du texte par défaut le texte est positionné à gauche :
        'LEFT' 'CENTER' permet de le placer au centre 'RIGHT' permet de le
        placer à droite
        """
        dico_pos = {'LEFT': W, 'RIGHT': E, 'CENTER': CENTER}
        dico_align = {'LEFT': LEFT, 'RIGHT': RIGHT, 'CENTER': CENTER}
        Label(self.frame, text=text, anchor=dico_pos[pos],
              justify=dico_align[pos]).grid(row=self.ind_ligne,
                                            sticky=NSEW, padx=5,
                                            pady=5)

        self.ind_ligne += 1

    def inserer_titre(self, text, niveau):
        """
        Méthode d'insertion d'un titre de niveau 1, 2 ou 3 dans la fenetre sur
        laquelle on l'applique avec des styles prédéfinis pour chaque niveau
        text : string -- paramètre obligatoire qui représente le texte à insérer
        niveau : int -- paramètre obligatoire qui représente le niveau du titre
                        Seules les valeurs 1, 2 et 3 sont admises
        """
        if niveau not in range(1, 4):
            raise InputError('Seules les valeurs 1, 2 et 3 sont admises pour '
                             'le paramètre niveau !')

        styles = {1: ['Helvetica 20 bold', NSEW, CENTER, 0, 20],
                  2: ['Helvetica 16 bold', W + NS, W, 5, 5],
                  3: ['Helvetica 14', W + NS, W, 5, 5]}
        label = Label(self.frame, text=text, font=styles[niveau][0],
                      anchor=styles[niveau][2], width=len(text) + 10)
        label.grid(row=self.ind_ligne, sticky=styles[niveau][1],
                   padx=styles[niveau][3], pady=styles[niveau][4])
        self.ind_ligne += 1
        return label

    def inserer_listebullets(self, list_text):
        """
        Méthode d'insertion d'une liste de textes précédés par un point
        list_text : list -- paramètre obligatoire qui représente la liste des
                            textes que l'on veut insérer
        """
        fr = Frame(self.frame)
        fr.grid(row=self.ind_ligne, sticky=N+S+W+E, padx=50, pady=10)
        self.ind_ligne += 1

        for value in list_text:
            Label(fr, text=u'\u25C6    '+value, anchor=W,
              justify=LEFT).grid(sticky=NSEW, padx=5,
                                            pady=5)
        
        

    def inserer_tableau(self, table_valeurs, liste_entetes=None):
        """
        Méthode d'insertion d'un tableau de valeurs avec une mise en page en
        lignes et en colonnes
        table_valeurs : list -- paramètre obligatoire, liste de liste des
        valeurs que l'on veut afficher
        liste_entetes : list -- paramètre optionnel qui représente les
        intitulés des colonnes s'il y a lieu
        """
        fr = LabelFrame(self.frame, text='')
        fr.grid(row=self.ind_ligne, padx=20, pady=10)
        self.ind_ligne += 1

        ind_row = 0
        if liste_entetes:
            
            if len(liste_entetes) == len(table_valeurs[0]):
                ind_col = 0
                for entete in liste_entetes:
                    Label(fr, text=str(entete), font='Helvetica 10 bold',
                          bg='#D8D8D8', width=len(str(entete)) + 4,
                          anchor=W).grid(row=ind_row, column=ind_col,
                                         sticky=N+S+W+E, padx=0, pady=1)
                    ind_col += 1
                ind_row += 1
            else:
                raise InputError('Les paramètres liste_entetes et '
                                 'table_valeurs doivent être de même '
                                 'longueur !')

        for ligne_valeurs in table_valeurs:
            ind_col = 0
            bg_color = self.cget('bg')
            for valeur in ligne_valeurs:
                if ind_row % 2:
                    bg_color = '#FFFFFF'
                Label(fr, text=str(valeur), width=len(str(valeur)) + 4,
                      bg=bg_color, anchor=W).grid(row=ind_row, column=ind_col,
                                                  sticky=N+S+E+W, padx=0,
                                                  pady=1)
                ind_col += 1
            ind_row += 1

    def inserer_separateur(self, longueur, couleur='#778899'):
        """
        Méthode d'insertion d'un séparateur dans la fenêtre (barre horizontale)
        longueur : int -- paramètre obligatoire indiquant la taille à
        l'horizontale de la barre que l'on veut insérer
        couleur : str -- paramètre optionnel indiquant la couleur de la barre
        au format html
        """
        Frame(self.frame, width=longueur, height=2, bg=couleur).grid(
            row=self.ind_ligne, padx=5, pady=5)
        self.ind_ligne += 1

    def inserer_barre(self, hauteur, couleur='#778899'):
        """
        Méthode d'insertion d'un séparateur dans la fenêtre (barre verticale)
        hauteur : int -- paramètre obligatoire indiquant la taille à
        la verticale de la barre que l'on veut insérer
        couleur : str -- paramètre optionnel indiquant la couleur de la barre
        au format html
        """
        Frame(self.frame, width=2, height=hauteur, bg=couleur).grid(
            row=self.ind_ligne, column=0, padx=5, pady=5)

    def sauter_ligne(self):
        """
        Méthode d'insertion d'un ligne vide dans la fenêtre
        """
        Label(self.frame, text='').grid(row=self.ind_ligne, sticky=NSEW)
        self.ind_ligne += 1

    def inserer_image(self, url):
        """
        Méthode d'insertion d'une image dans la fenêtre
        url : str -- paramètre obligatoire représentant le chemin d'accès à
        l'image que l'on souhaite ajouter
        """
        image = PhotoImage(file=url)
        panel = Label(self.frame, image=image, width=image.width() + 10,
                      height=image.height() + 10)
        panel.grid(row=self.ind_ligne)
        panel.image = image
        self.ind_ligne += 1

    ###########################################################################
    #           Widgets                                                       #
    ###########################################################################

    def inserer_bouton(self, label, action):
        """
        Méthode d'insertion d'un bouton clickable dans la fenêtre
        label : str -- paramètre obligatoire représentant le texte à afficher
        sur le bouton
        action : function -- paramètre obligatoire représentant la fonction
        sans paramètre qui sera déclenchée lorsque le bouton sera actionné
        """
        Button(self.frame, text=label, command=action,
               width=len(label) + 6).grid(row=self.ind_ligne, padx=0, pady=10)
        self.ind_ligne += 1

    def inserer_list_boutons(self, list_labels, list_actions):
        """
        Méthode d'insertion d'un ensemble de boutons clickables sur une ligne
        dans la fenêtre
        list_labels : list[str] -- paramètre obligatoire représentant une liste
        de textes à afficher sur les différents boutons
        list_actions : list[function] -- paramètre obligatoire représentant une
        liste de fonctions sans paramètre qui seront déclenchées lorsque les
        boutons seront actionnés
        Les paramètres list_labels et list_actions doivent être de même
        longueur.
        """
        if len(list_labels) != len(list_actions):
            raise InputError('Les paramètres list_labels et list_actions '
                             'doivent être de même longueur !')

        fr = Frame(self.frame)
        fr.grid(row=self.ind_ligne, sticky=NSEW, padx=5, pady=5)
        self.ind_ligne += 1

        Grid.rowconfigure(fr, 0, weight=1)
        for i, lbl in enumerate(list_labels):
            Button(fr, text=lbl, command=list_actions[i],
                    width=len(lbl) + 6).grid(row=0, column=i, padx=0,
                                            pady=10)
            Grid.columnconfigure(fr, i, weight=1)

    def inserer_champ_text(self, label, text, width=30):
        """
        Méthode d'insertion d'un champ de saisie texte dans la fenêtre
        label : str -- paramètre obligatoire représentant l'identifiant du champ
        text : str -- paramètre obligatoire représentant le texte explicatif
        associé au champ
        width : int -- paramètre optionnel représentant la longueur du champ en
        nombre de caractères
        Les données récupérables sont des chaînes de caractères (une chaîne à
        chaque action de récupération des données)
        """

        fr = Frame(self.frame)
        fr.grid(row=self.ind_ligne, sticky=NS + W, padx=5, pady=5)
        self.ind_ligne += 1

        Label(fr, text=text).grid(row=0, column=0, sticky=NS + W, padx=5,
                                  pady=0)
        var_texte = StringVar()
        self.var_datas[label] = var_texte

        ligne_texte = Entry(fr, textvariable=var_texte, width=width)
        ligne_texte.grid(row=0, column=1, sticky=N+S+W, padx=5, pady=0)

    def inserer_list_champs_text(self, list_labels, list_texts,
                                 list_widths=None):
        """
        Méthode d'insertion d'un ensemble de champs texte sur une ligne dans la
        fenêtre
        list_labels : list[str] -- paramètre obligatoire représentant la liste
        des identifiants des champs
        list_texts : list[str] -- paramètre obligatoire représentant une liste
        de textes à afficher pour expliciter le rôle de chaque champ
        list_width : list[int] -- paramètre optionnel permettant d'indiquer une
        taille pour chaque champ
        Les paramètres list_labels et list_actions doivent être de même
        longueur. Lorsqu'il est fourni, le paramètre list_widths doit également
        être de même longueur.
        Les données récupérables sont des chaînes de caractères (une chaîne par
        champ à chaque action de récupération des données)
        """
        fr = Frame(self.frame)
        fr.grid(row=self.ind_ligne, sticky=NSEW, padx=5, pady=5)
        self.ind_ligne += 1

        Grid.rowconfigure(fr, 0, weight=1)
        if list_widths:
            if (len(list_labels) != len(list_texts)
                    or len(list_labels) != len(list_widths)):
                raise InputError('Les paramètres list_labels, list_texts et '
                                 'list_widths doivent être de même longueur !')

            for i, lbl in enumerate(list_labels):
                Label(fr, text=list_texts[i]).grid(
                    row=0, column=i * 2, sticky=W, padx=5, pady=0)
                str_var = StringVar()
                self.var_datas[lbl] = str_var

                ligne_texte = Entry(fr, textvariable=str_var,
                    width=list_widths[i])
                ligne_texte.grid(row=0, column=2 * i + 1, sticky=W, padx=5,
                                 pady=0)
                Grid.columnconfigure(fr, 2 * i + 1, weight=1)
        else:
            if len(list_labels) != len(list_texts):
                raise InputError('Les paramètres list_labels, list_texts '
                                 'doivent être de même longueur !')
            for i, lbl in enumerate(list_labels):
                Label(fr, text=list_texts[i]).grid(row=0, column=i * 2,
                                                   sticky=W, padx=5, pady=0)
                str_var = StringVar()
                self.var_datas[lbl] = str_var

                ligne_texte = Entry(fr, textvariable=str_var, width=30)
                ligne_texte.grid(row=0, column=2 * i + 1, sticky=W, padx=5,
                                 pady=0)
                Grid.columnconfigure(fr, 2 * i + 1, weight=1)

    def inserer_champ_passwd(self, label, text, width=30):
        """
        Méthode d'insertion d'un champ de saisie texte dans la fenêtre
        Les caractères saisis sont remplacés par des '*'
        Ce type de champ convient par exemple pour la saisie de mots de passe
        label : str -- paramètre obligatoire représentant l'identifiant du champ
        text : str -- paramètre obligatoire représentant le texte explicatif
        associé au champ
        width : int -- paramètre optionnel représentant la longueur du champ en
        nombre de caractères
        Les données récupérables sont des chaînes de caractères (une chaîne à
        chaque action de récupération des données)
        """
        fr = Frame(self.frame)
        fr.grid(row=self.ind_ligne, sticky=N+S+W, padx=5, pady=5)
        self.ind_ligne += 1

        Label(fr, text=text).grid(row=0, column=0, sticky=N + S + W, padx=5,
                                  pady=0)
        var_texte = StringVar()
        self.var_datas[label] = var_texte

        ligne_texte = Entry(fr, textvariable=var_texte, width=width, show='*')
        ligne_texte.grid(row=0, column=1, sticky=N+S+W, padx=5, pady=0)

    def inserer_champ_paragraphe(self, label, text, nb_lignes=3):
        """
        Méthode d'insertion d'un champ de saisie texte de grande taille dans la
        fenêtre
        Ce type de champ est intéressant pour la saisie de textes de longueur
        libre
        label : str -- paramètre obligatoire représentant l'identifiant du champ
        text : str -- paramètre obligatoire représentant le texte explicatif
        associé au champ
        nb_lignes : int -- paramètre optionnel représentant le nombre de ligne
        du champ
        Les données récupérables sont des chaînes de caractères (une chaîne à
        chaque action de récupération des données)
        """
        fr = Frame(self.frame)
        fr.grid(row=self.ind_ligne, sticky=N+S+W+E, padx=5, pady=5)
        self.ind_ligne += 1

        Label(fr, text=text).grid(row=0, column=0, sticky=N + S + W, padx=5,
                                  pady=0)

        txt = Text(fr, wrap='word', height=nb_lignes)
        txt.grid(row=0, column=1, sticky=N + S + E + W)
        self.var_datas[label] = txt

        Grid.columnconfigure(fr, 1, weight=1)

    def inserer_calendrier(self, label, text):
        """
        Méthode d'insertion d'un calendrier dans la fenêtre afin que
        l'utilisateur puisse sélectionner une date
        label : str -- paramètre obligatoire représentant l'identifiant du champ
        text : str -- paramètre obligatoire représentant le texte explicatif
        associé au champ
        Les données récupérables sont des chaînes de caractères formatées ainsi
        : aaaa-mm-dd (une chaîne à chaque action de récupération des données)
        """
        fr = Frame(self.frame)
        fr.grid(row=self.ind_ligne,  padx=20, pady=10, sticky=N+S+W)
        self.ind_ligne += 1

        Label(fr, text=text).grid(row=0, column=0, sticky=N+S+W, padx=5, pady=0)
        ttkcal = Calendar(fr, firstweekday=calendar.SUNDAY)
        ttkcal.grid(row=0, column=1)
        self.var_datas[label] = ttkcal

    def inserer_group_radios(self, label, text, list_labels, list_values=None):
        """
        Méthode d'insertion de listes à choix unique
        label : str -- paramètre obligatoire représentant l'identifiant du champ
        text : str -- paramètre obligatoire représentant le texte explicatif
        associé au champ
        list_labels : list -- paramètre obligatoire représentant la liste des
        textes à afficher en face des boutons de sélection
        list_values : list -- paramètre optionnel représentant la liste des
        valeurs à retourner pour chacun des boutons de sélection ce paramètre
        est à renseigner lorsque l'on souhaite que la légende des boutons
        diffère de la valeur associée

        Si le paramètre list_values est fourni, les listes list_labels et
        list_values doivent être de même longueur
        Les données récupérables sont des éléments de list_labels si
        list_values n'est pas fournie, ou de list_values dans le cas contaire.
        Un seul élement est fourni à chaque récupération des données
        """
        fr = Frame(self.frame)
        fr.grid(row=self.ind_ligne, sticky=N+S+W, padx=5, pady=5)
        self.ind_ligne += 1

        Label(fr, text=text).grid(row=0, column=0, sticky=N+S+W, padx=5, pady=0)
        var_choix = StringVar()
        if list_values:
            if len(list_labels) != len(list_values):
                raise InputError('Les paramètres list_labels et list_values '
                                 'doivent être de même longueur !')
            self.var_datas[label] = [var_choix, list_labels, list_values]
        else:
            self.var_datas[label] = var_choix

        ind_choix = 0
        for choix in list_labels:
            Radiobutton(fr, text=choix, variable=var_choix,
                        value=choix).grid(row=ind_choix, column=1,
                                          sticky=N + S + W, padx=5, pady=0)
            ind_choix += 1

    def inserer_checkbutton(self, label, text):
        """
        Méthode d'insertion d'une case à cocher
        label : str -- paramètre obligatoire représentant l'identifiant du champ
        text : str -- paramètre obligatoire représentant le texte explicatif
        associé au champ
        Si la case n'est pas cochée la valeur récupérable est 0, 1 dans le cas
        contraire
        """
        fr = Frame(self.frame)
        fr.grid(row=self.ind_ligne, sticky=N+S+W, padx=5, pady=5)
        self.ind_ligne += 1
        Label(fr, text=text).grid(row=0, column=0, sticky=N + S + W, padx=5,
                                  pady=0)
        var_case = IntVar()
        self.var_datas[label] = var_case
        check_button = Checkbutton(fr, variable=var_case)
        check_button.grid(row=0, column=1, sticky=N+S+W, padx=5, pady=0)

    def inserer_listebox(self, label, text, list_labels, list_values=None,
                         select_mode=SINGLE):
        """
        Méthode d'insertion de listes de choix dans laquel la sélection peut
        être unique ou multiple
        label : str -- paramètre obligatoire représentant l'identifiant du champ
        text : str -- paramètre obligatoire représentant le texte explicatif
        associé au champ
        list_labels : list -- paramètre obligatoire représentant la liste des
        textes à afficher dans la liste de choix
        list_values : list -- paramètre optionnel représentant la liste des
        valeurs à retourner pour chacun des labels de la liste ce paramètre est
        à renseigner lorsque l'on souhaite que la légende dans la liste diffère
        de la valeur associée
        select_mode : str -- paramètre optionnel représentant le mode de
        sélection SINGLE (valeur par défaut) pour des listes à sélection unique
        EXTENDED pour des listes à sélection multiple

        Si le paramètre list_values est fourni, les listes list_labels et
        list_values doivent être de même longueur
        Les données récupérables sont des éléments de list_labels si
        list_values n'est pas fournie, ou de list_values dans le cas contaire.
        Quel que soit le mode de sélection, une liste d'élements éventuellement
        vide est fournie à chaque récupération des données
        """
        fr = Frame(self.frame)
        fr.grid(row=self.ind_ligne, sticky=N+S+W, padx=5, pady=5)
        self.ind_ligne += 1
        Label(fr, text=text).grid(row=0, column=0, sticky=N+S+W, padx=5, pady=0)
        liste = Listbox(fr, height=min(len(list_labels), 10),
                        selectmode=select_mode, activestyle='none',
                        exportselection=0)
        scroll_y = Scrollbar(fr)
        scroll_y.config(command=liste.yview)
        liste.config(yscrollcommand=scroll_y.set)
        if list_values:
            if len(list_labels) != len(list_values):
                raise InputError('Les paramètres list_labels et list_values '
                                 'doivent être de même longueur !')
            self.var_datas[label] = [liste, list_values]
        else:
            self.var_datas[label] = liste

        for i, label in enumerate(list_labels):
            liste.insert(i, label)

        liste.grid(row=0, column=1, sticky=NS + W, padx=5, pady=0)
        scroll_y.grid(row=0, column=2, sticky='ns')

    def inserer_scale(self, label, text, mini, maxi, pas=1):
        """
        Méthode d'insertion d'un curseur de sélection d'une valeur dans un
        intervalle donné
        label : str -- paramètre obligatoire représentant l'identifiant du champ
        text : str -- paramètre obligatoire représentant le texte explicatif
        associé au champ
        mini : float -- paramètre obligatoire représentant la valeur minimale
        sélectionnable
        maxi : float -- paramètre obligatoire représentant la valeur maximale
        sélectionnable
        pas : float -- paramètre optionnel représentant le pas entre deux
        valeurs possibles
        Les données récupérables sont des valeurs numériques (une à la fois)
        """
        fr = Frame(self.frame)
        fr.grid(row=self.ind_ligne, sticky=NS + W, padx=5, pady=5)
        self.ind_ligne += 1

        Label(fr, text=text).grid(row=0, column=0, sticky=N+S+W, padx=5, pady=0)
        var_scale = DoubleVar()
        self.var_datas[label] = var_scale
        scale = Scale(fr, from_=mini, to=maxi, showvalue=True,
                      variable=var_scale, tickinterval=5, orient='h',
                      length=(maxi-mini)*8, resolution=pas)
        scale.grid(row=0, column=1, sticky=NSEW)

    def inserer_spinbox_float(self, label, text, mini, maxi, pas=1):
        """
        Méthode d'insertion d'une liste déroulante de valeurs dans un
        intervalle donné
        label : str -- paramètre obligatoire représentant l'identifiant du champ
        text : str -- paramètre obligatoire représentant le texte explicatif
        associé au champ
        mini : float -- paramètre obligatoire représentant la valeur minimale
        sélectionnable
        maxi : float -- paramètre obligatoire représentant la valeur maximale
        sélectionnable
        pas : float -- paramètre optionnel représentant le pas entre deux
        valeurs possibles
        Les données récupérables sont des valeurs numériques (une à la fois)
        """
        fr = Frame(self.frame)
        fr.grid(row=self.ind_ligne, sticky=NS + W, padx=5, pady=5)
        self.ind_ligne += 1

        Label(fr, text=text).grid(row=0, column=0, sticky=N+S+W, padx=5, pady=0)
        var_spin = DoubleVar()
        self.var_datas[label] = var_spin

        spinbox = Spinbox(fr, textvariable=var_spin, from_=mini, to=maxi,
                          increment=pas, state='readonly',
                          readonlybackground='#FFFFFF',
                          selectbackground='#FFFFFF',
                          selectforeground='#000000')
        spinbox.grid(row=0, column=1)

    def inserer_spinbox_values(self, label, text, list_labels,
                               list_values=None):
        """
        Méthode d'insertion d'une liste déroulante de valeurs dans une liste de
        labels donnés
        label : str -- paramètre obligatoire représentant l'identifiant du champ
        text : str -- paramètre obligatoire représentant le texte explicatif
        associé au champ
        list_labels : list -- paramètre obligatoire représentant la liste des
        textes à afficher dans la liste de choix
        list_values : list -- paramètre optionnel représentant la liste des
        valeurs à retourner pour chacun des labels de la liste ce paramètre est
        à renseigner lorsque l'on souhaite que la légende dans la liste diffère
        de la valeur associée
        Si le paramètre list_values est fourni, les listes list_labels et
        list_values doivent être de même longueur
        Les données récupérables (une valeur à la fois) sont des éléments de
        list_labels si list_values n'est pas fournie, ou de list_values dans le
        cas contaire.
        """
        fr = Frame(self.frame)
        fr.grid(row=self.ind_ligne, sticky=NS + W, padx=5, pady=5)
        self.ind_ligne += 1

        Label(fr, text=text).grid(row=0, column=0, sticky=N+S+W, padx=5, pady=0)
        var_spin = StringVar()
        if list_values:
            if len(list_labels) != len(list_values):
                raise InputError('Les paramètres list_labels et list_values '
                                 'doivent être de même longueur !')
            self.var_datas[label] = [var_spin, list_labels, list_values]
        else:
            self.var_datas[label] = var_spin

        spinbox = Spinbox(fr, textvariable=var_spin, values=list_labels,
                          state='readonly', readonlybackground='#FFFFFF',
                          selectbackground='#FFFFFF',
                          selectforeground='#000000')
        spinbox.grid(row=0, column=1)
