

def verifie_mot_passe(email,mot_passe):
    """
    Check wether the password given correspond to the email given
    """
    mon_curseur.execute('SELECT id, password FROM client WHERE email=?',[email])
    liste_resultats=mon_curseur.fetchall()
    if bool(liste_resultats):
        #If the result of the query isn't empty then email exists in database and correspond to a password
        if mot_passe==liste_resultats[0][1]:
            return True,liste_resultats[0][0]
            # Check if password match email given, if so return True and the id of the client
        else :
            return False,0
            #password not correct
    else:
        return False,0

def email_deja_utilise(email):
    """
    Return True if email given is already in the database, False otherwise
    """
    mon_curseur.execute('SELECT email FROM client WHERE email=?',[email])
    liste_resultats=mon_curseur.fetchall()
    if bool(liste_resultats):
        # Empty query result means that this email does not already exists in the database
        return True
    else:
        return False

def connexion():
    """
    Email and password checks
    Then redirect to other frames if email and password are valids
    """
    app.get_datas()
    email,mot_passe=app.datas['email'],app.datas['mot_passe']
    valide,id=verifie_mot_passe(email,mot_passe)
    if valide:
        id_utilisateur=id
        page_accueil() #Redirect to Home Page
    else:
        app.clear()
        app.inserer_text('Invalid Email and/or password',pos='CENTER')
        app.inserer_bouton('Return to Log In page',page_connexion)
        app.inserer_bouton('Create a new account',page_creation_compte_client)


def creation_compte_client():
    """
    To register a new account in the database
    """
    app.get_datas()
    app.clear()
    nom,prenom,email,mot_passe=app.datas['nom'],app.datas['prenom'],app.datas['email'],app.datas['mot_passe']   
    champs_completes=(bool(nom) and bool(prenom) and bool(email))
    if email_deja_utilise(email):
        #email déjà enregistré dans base de donnée = client possède déjà un compte
        app.inserer_titre('Error : This email adress is already taken',1)
        app.inserer_bouton('Create a new account',page_creation_compte_client)
        app.inserer_bouton('Back to Log In Page',page_connexion)
    elif not champs_completes:
        #Last name, First name and email cannot be empty
        page_creation_compte_client()
        app.inserer_titre('Error : you must complete Last name, First name and email fields',3)
    else:
        #if all fields are valid, a new account is created
        mon_curseur.execute('SELECT max(id) FROM client')
        liste_resultats=mon_curseur.fetchall()
        id=liste_resultats[0][0]+1
        mon_curseur.execute('INSERT INTO client (nom, prenom, email,password) VALUES (?,?,?,?)',[nom,prenom,email,mot_passe])
        ma_connexion.commit()
        page_transition_creation_compte_connexion(email)

def modifier_mot_passe():
    """
    To change the password of an user
    """
    app.get_datas()
    mot_passe1,mot_passe2=app.datas['nouveau_mot_passe1'],app.datas['nouveau_mot_passe2']
    if mot_passe1==mot_passe2:
        mon_curseur.execute('UPDATE client SET password=? WHERE id=?',[mot_passe1,id_utilisateur])
        ma_connexion.commit()
        page_parametre_compte()
        app.inserer_titre('Your password has been changed',1)
    else:
        page_modifier_mot_passe()
        app.inserer_titre('Error : password you gave were differents',2)

def liste_ingredients_plat(id_plat):
    """
    Return the ingredients, quantities and reference unit to make a given recipe
    """
    mon_curseur.execute('SELECT ingredient.libelle,composition.quantite,composition.unite_reference FROM plat,composition,ingredient WHERE plat.id=? AND plat.id=composition.id_plat AND composition.id_ingredient=ingredient.id',[id_plat])
    liste_resultats=mon_curseur.fetchall()
    return liste_valeurs

def liste_ingredients():
    """
    Return all ingredients names and id existing in database (2 lists: one for id, one for names)
    """
    liste_id=[]
    liste_ingredients=[]
    mon_curseur.execute('SELECT id,libelle FROM ingredient ORDER BY libelle')
    liste_resultats=mon_curseur.fetchall()
    liste_id=[a[0] for a in liste_resultats]
    liste_ingredients=[a[1] for a in liste_resultats]
    return liste_id,liste_ingredients 


def liste_plats():
    """
    Return 2 lists : all recipes existing in database and their id 
    """
    liste_id=[]
    liste_plats=[]
    mon_curseur.execute('SELECT id,libelle FROM plat ORDER BY libelle')
    liste_resultats=mon_curseur.fetchall()
    liste_id=[a[0] for a in liste_resultats]
    liste_plats=[a[1] for a in liste_resultats]
    return liste_id,liste_plats

def recherche_plat():
    """
    Function used to construct a query to select all recipes corresponding to the criteria
    chosen in the page Look for a recipe
    """
    app.get_datas()
    mots_cles=app.datas['mots_cles']
    ingredients=app.datas['ingredients']

    query=""

    if bool(mots_cles):
        """ If mot_cles not empty, key words have been passed then we want to find
        all recipe whose name include one or more of the given key words"""
        query+="SELECT id,libelle FROM plat WHERE libelle LIKE "
        
        key_words=mots_cles.split(',')
        key_words=[a.strip() for a in key_words]
        #List of all key words
        
        n=len(key_words)
        for i in range(n):
            query+=(i!=0)*"OR libelle LIKE "+"'%"+key_words[i]+"%'"

    if bool(ingredients):
        """ Same here, if ingredients have been passed, then we want to find recipes
        which contains one or more of these ingredients
        Return 2 lists : one of the id of the recipes matching the research and one with
        the name of those recipes"""

        id_ingredients=str(tuple(ingredients))
        id_ingredients=id_ingredients.replace(' ','')
        #To get a string that looks like that : (id1,id2...,idn)

        if bool(mots_cles):
            query+="INTERSECT"
        query+="SELECT plat.id, plat.libelle FROM plat, composition, ingredient WHERE plat.id=composition.id_plat AND composition.id_ingredient=ingredient.id AND ingredient.id IN ?"

    mon_curseur.execute(query,id_ingredients)
    liste_resultats=mon_curseur.fetchall()
    list_id_plats=[a[0] for a in liste_plats]
    liste_libelle_plats=[a[1] for a in liste_resultats]

    page_resultat_recherche_recette(liste_id_plats,liste_libelle_plats)

def redirection_fiche_recette():
    """
    When someone chose a recipe, egt the id of that recipe and redirect to the page showing recipe instructions
    """
    app.get_data()
    id_recette=app.datas['plat']
    page_afficher_recette(id_recette)

def enregistrer_nouvelle_consommation(id_plat):
    """
    To add a new consumption to the database
    """
    app.get_datas()
    id_plat,nb_parts,date,heure=app.datas['plat'],app.datas['nb_parts'],app.datas['date'],app.datas['heure']
    mon_curseur.execute('INSERT INTO consommation (id_client, id_plat, nb_parts, date, heure) VALUES (?,?,?,?,?)',[id_utilisateur,id_plat,nb_parts,date,heure])
    ma_connexion.commit()
    page_accueil()

def toutes_consommations(id_utilisateur):
    """
    To get all consumption of a client
    """
    mon_curseur.execute('SELECT libelle, nb_parts, date, heure FROM consommation, plat WHERE plat.id=consommation.id_plat AND consommation.id_client=? ORDER by date',[id_utilisateur])
    list_resultats=mon_curseur.fetchall()
    return list_resultats