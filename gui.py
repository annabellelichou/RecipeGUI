# Functions used to create Graphical User Interfaces

from agro_GUI.agro_widgets import*

app=Agro_App("Recipes")

def page_connexion():
    """
    Log in page, if email and password given match to the ones in the database, user id is changed 
    from 0 (which means that no user is currently logged in) to the id of the client.
    """
    app.clear()
    id_utilisateur=0 #To automatically log out someone who chose "Log out" button from Home Page
    app.inserer_titre('Log In',1)
    app.inserer_champ_text('email', 'Email :',width=30)
    app.inserer_champ_passwd('mot_passe', 'Password :',width=30)
    app.inserer_bouton('Continue',connexion)
    app.inserer_bouton('Create a new account',page_creation_compte_client)
    app.manage_view()


def page_creation_compte_client():
    """
    Frame to create a new client
    """
    app.clear()
    app.inserer_titre('Create a new account',1)
    app.inserer_champ_text('nom', 'Last name :',width=30)
    app.inserer_champ_text('prenom', 'First name :',width=30)
    app.inserer_champ_text('email', 'Email :',width=50)
    app.inserer_champ_text('mot_passe', 'Password :',width=30)
    app.inserer_bouton('Continue',creation_compte_client)
    app.inserer_bouton('Back to Log In Page',page_connexion)
    app.manage_view()

def page_accueil():
    """
    Home Page, when someone logged in
    """
    app.clear()
    mon_curseur.execute('SELECT prenom, nom FROM client WHERE id=?',[id_utilisateur])
    liste_resultats=mon_curseur.fetchall()
    prenom,nom=liste_resultats[0][0],liste_resultats[0][1]
    titre='Welcome '+prenom+' '+nom
    app.inserer_titre(titre,2)
    app.inserer_bouton('Look for Recipes',page_recherche_recette)
    app.inserer_bouton('All my consumptions',page_consommations)
    app.inserer_bouton('Account settings',page_parametre_compte)
    app.inserer_bouton('Log out',page_connexion) #Back to log in page
    app.manage_view()


def page_transition_creation_compte_connexion(email):
    """
    Frame with a small sentence indicating that the new account has been created
    """
    app.clear()
    app.inserer_titre('Your account has successfully been created',1)
    app.inserer_bouton('Back to Log In Page',page_connexion)
    app.manage_view()

def page_modifier_mot_passe():
    """
    To change change
    """
    app.clear()
    app.inserer_titre('Change my password',1)
    app.inserer_champ_text('nouveau_mot_passe1','New password :',width=30)
    app.inserer_champ_text('nouveau_mot_passe2','Confirm new password :',width=30)
    app.inserer_bouton('Continue',modifier_mot_passe)
    app.inserer_bouton('Back to account settings',page_parametres_compte)
    app.inserer_bouton('Back to Home Page',page_accueil)
    app.manage_view()

def page_parametre_compte():
    """
    Account Settings Frame
    """
    app.clear()
    app.inserer_titre('Account Settings',1)
    app.inserer_bouton('Change my password',page_modifier_mot_passe)
    app.inserer_bouton('Back to Home Page',page_accueil)
    app.manage_view()

def page_afficher_recette(id_recette):
    """
    Show a given recipe
    """
    app.clear()
    mon_curseur.execute('SELECT libelle,recette,image,difficulte,nb_personnes,temps_preparation FROM plat WHERE id=?',[id_recette])
    liste_resultats=mon_curseur.fetchall()
    titre,recette,url,difficulte,nb_personnes,temps_preparation=liste_resultats[0][0],liste_resultats[0][1],liste_resultats[0][2],liste_resultats[0][3],liste_resultats[0][4],liste_resultats[0][5]
    
    liste_bullets=['Difficulty : '+str(difficulte),'Servings : '+str(nb_personnes),'Time : '+str(temps_preparation)]
    liste_entetes=['Ingredient','Quantity','Reference Unit']
    liste_valeurs=liste_ingredients_plat(id_recette)
    # liste_entetes2=['Calories','Protéines','Glucides','Lipides','Fibres']
    # calories,protéines,glucides,lipides,fibres=calcule_valeur_energetique(id_recette)
    # liste_valeurs2=[[calories,protéines,glucides,lipides,fibres]]
    app.inserer_image('img\\'+url) #Picture of the recipe
    app.inserer_titre(titre,1) #Name of the recipe
    app.inserer_listebullets(liste_bullets)
    app.inserer_text('Ingrédients :',pos='LEFT')
    app.inserer_tableau(liste_valeurs,liste_entetes) #Array: ingredients, quantities and reference units
    app.inserer_text(recette,pos='CENTER') #Prep. instructions
    # app.inserer_text('Valeur nutritionelle par part :',pos='LEFT')
    # app.inserer_tableau(liste_valeurs2,liste_entetes2)
    app.inserer_bouton('Back to Home page',page_accueil)
    app.inserer_bouton('Add to my consumption',page_nouvelle_consommation(id_recette))
    app.manage_view()

def page_recherche_recette():
    """
    Page to look for a recipe
    """
    app.clear()
    app.inserer_titre('Look for a recipes',1)
    liste_id1,liste_ingredients1=liste_ingredients()
    app.inserer_champ_paragraphe('mots_cles','Key Words (separated by comma) :',nb_lignes=3)
    app.inserer_listebox('ingredients','Ingredients :',liste_ingredients1,liste_id1,select_mode=EXTENDED)
    #Will show a listbox of all ingredients existing in database and return the ids of the ones selected by the client
    #app.inserer_listebox('ingredients_abs','Exclude recipes containing :', liste_ingredients1,liste_id1,select_mode='EXTENDED')
    app.inserer_checkbutton('vegetarien','Vegetarian')
    #app.inserer_scale('difficulte_max','Difficulty max :',0,5,pas=1)
    liste_boutons=['Search','Back to Home Page']
    liste_actions=[recherche_plat,page_accueil]
    app.inserer_list_boutons(liste_boutons,liste_actions)
    app.manage_view()

def page_resultat_recherche_recette(liste_id_plats,liste_libelle_plats):
    """
    Page which show the recipe that match a research in a listbox
    """
    app.clear()
    app.inserer_titre('Results of your research',1)
    app.inserer_listebox('plat','Recipes corresponding to your research :',liste_libelle_plats,liste_id_plats,select_mode=SIMPLE)
    app.inserer_bouton('See the recipe',redirection_fiche_recette)
    app.inserer_bouton('Back to recipe search',page_recherche_recette)
    app.inserer_bouton('Back to Home Page',page_accueil)

def page_nouvelle_consommation(id_plat):
    """
    We can access this page from a recipe instruction page,
    it allows the client to add this recipe to it's consumptions
    """
    app.clear()
    app.inserer_titre('Add a new consumption',1)
    app.inserer_spinbox_float('nb_parts','Number of servings consumed :',1,10,1)
    app.inserer_calendrier('date','Date :')
    app.inserer_champ_text('heure','Time (h:min:sec):')
    app.inserer_bouton('Validate',enregistrer_nouvelle_consommation(id_plat))
    app.inserer_bouton('Back to home page',page_accueil)
    app.inserer_bouton('Back to recipe page',page_afficher_recette(id_plat))

def page_consommations():
    """
    Page to see all consumption of a client
    """
    app.clear()
    app.inserer_titre('My consumptions',1)  libelle, nb_parts, date, heure
    liste_valeurs=toutes_consommations(id_utilisateur)
    liste_entetes=['Recipe','Number of servings','Date','Time'] 
    app.inserer_tableau(liste_valeurs,liste_entetes)
    app.inserer_bouton('Back to Home Page',page_accueil)
    app.manage_view()
