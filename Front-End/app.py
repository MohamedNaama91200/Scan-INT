import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename
from fastai.vision import *
import json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 #méthode de flask qui empêche le telechargement de fichiers dont la taille est > 2Mb
                                                   #si c'est le cas elle return un erreur 413 
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png'] #liste dans laquelle on met les extention acceptées par notre code ( pour des raisons de sécurité
app.config['UPLOAD_PATH'] = 'uploads' #dossier vers lequel les images vont etre transferées

#=========================validation image=========================================

def validate_image(stream): #méthode qui vérrifie si le fichier uploader est vraiment une image 
                            #pour cela, elle va inspecter le header du fichier pour indentifier la nature de ce dernier
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header) #methode qui permet d'inspecter le header et renvoit la nature du fichier donc ici jpg ou png
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg') # finalement, on veut que la fonction renvoit une extention plus que la nature du fichier, d'ou le rajout du '.'

@app.errorhandler(413) #décorateur qui lorssqu'une erreur 413 est lancée, return "file is to large" à la place d'une simple page web sur laquelle on voit affiché "error413"
def too_large(e):
    return "File is too large", 413

#========================mise de l'image dans le dossier============================

@app.route('/') #decorateur qui lance la méthode home qui permet d'afficher le fichier html home.html
def home():
    return render_template('/home.html')

@app.route('/app.html') #route lancée lorsque le serveur local recoit une methode GET de la par du site web 
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('app.html', files=files) #renvoi 

@app.route('/app.html', methods=['POST']) #lorsque le serveur local recoit une methode post, cette route est lancée par le décorateur 
def upload_files():
    uploaded_file = request.files['file'] #méthode qui recupère le fichier dans le <forme> de html (celui déposé par l'utilisateur) 
    filename = secure_filename(uploaded_file.filename) #la variable filename prend le nom du fichier déposer par l'utilisateur 
                                                       #la méthode secure_filename permet d'applatire le nom du fichier. en d'autres termes il evite des personnes mal intentionner upload des fichiers dont les noms pourraient avoir des actions sur notre ordinateur 
    if filename != '': #si l'utilisateur ne dépose aucun fichier, filename prend la valeur '', il est donc important de verifier si filename est different de ''
        file_ext = os.path.splitext(filename)[1] #méthode qui renvoit de maniere séparée la route comme premiere argument et l'extention comme deuxieme arg
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
            file_ext != validate_image(uploaded_file.stream): #s'assure que l'extension renvoyée par notre méthode validate_image(stream) se trouve bien dans notre liste d'extentions 
                                                        #on vérifie alors si l'extension du fichier envoyée par l'utilisateur se trouve dans la liste definie plus haut 
            return "Invalid image", 400 # si ce n'est pas la cas alors, on renvoit "Invalid image" et une erreur 400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename)) #enregistre le fichier dans le repertoir courrant sous le nom de filename
    return '', 204 #si le nom ou le fichier est vide, lance une erreur 204

#=========================================analyse de l'image=====================================

@app.route("/analyse.html") #décorateur qui lance l'analyse de la solution lorsque l'utilisateur appuie sur le boutton analyser du site web
def solutions():
    learner = load_learner('/Users/elliotcole/Documents/TSP/S2/dvp_info/site') #methode de fastai qui permet de lire le contenu du fichier pickle 
                                                                               #ou le fichier pickle est la resultante de notre reseau de neurone
    uploads = "/Users/elliotcole/Documents/TSP/S2/dvp_info/site/uploads"
    file = [f for f in os.listdir(uploads)]
    if len(file)<=1:
        pred = "veuillez insérer une image"
    else :
        img = open_image(uploads + "/" + file[-1]) 
        prediction,pred_idx,outputs = learner.predict(img) #on lance la prediction de notre image 
        pred = prediction.obj #on stock la predition dans un variable pred 
        os.remove(uploads +'/'+file[-1])
    return render_template("solution1.html", pred = pred) #on affiche la page solution1.html sur le site a l'utilisatuer avec la predition 

#====================================annexe==============================================================

@app.route('/home.html') #méthode qui permet le bon fonctionnement du site web lorsqu'on veut aller sur la page home de notre site 
def home1():
    return render_template('home.html')
