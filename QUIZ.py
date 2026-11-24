import json
import random
import os
import datetime


# CREATION DES QUESTIONS

def enregistrer_question():
    questions = []

    for i in range(10):
        print(f"\n--- Question {i+1} ---")

        texte = input("Question : ")

        reponses = []
        for j in range(3):
            reponse = input(f"Réponse {j+1} : ")
            reponses.append(reponse)

        while True:
            try:
                bonne_reponse = int(input("Numéro de la bonne réponse (1, 2 ou 3) : "))
                if 1 <= bonne_reponse <= 3:
                    break
                print("Choisis un numéro entre 1 et 3.")
            except ValueError:
                print("Entre un nombre valide.")

        questions.append({
            "question": texte,
            "reponses": reponses,
            "bonne_reponse": bonne_reponse
        })

    with open("questions.json", "w", encoding="utf-8") as fichier:
        json.dump(questions, fichier, indent=4, ensure_ascii=False)


# CHARGEMENT DES QUESTIONS

def charger_questions():
    with open("questions.json", "r", encoding="utf-8") as fichier:
        return json.load(fichier)


# LANCEMENT DU QUIZ

def question():
    questions = charger_questions()

    if not questions:
        print("Aucune question disponible.")
        return

    selection = random.sample(questions, min(10, len(questions)))
    score = 0

    for i, quest in enumerate(selection, 1):
        print(f"\n--- Question {i}/{len(selection)} ---")
        print(quest["question"])

        reponses = quest["reponses"]
        indices = list(range(len(reponses)))
        random.shuffle(indices)

        reponses_melangees = [reponses[j] for j in indices]

        for j, reponse in enumerate(reponses_melangees, 1):
            print(f"{j}. {reponse}")

        while True:
            try:
                choix = int(input("Ta réponse : "))
                if 1 <= choix <= len(reponses_melangees):
                    break
                print("Numéro invalide.")
            except ValueError:
                print("Entre un nombre valide.")

        bonne_reponse = quest["bonne_reponse"] - 1
        bonne_reponse_melangee = indices.index(bonne_reponse)

        if choix - 1 == bonne_reponse_melangee:
            print("Bonne réponse !")
            score += 1
        else:
            print("Mauvaise réponse !")
            print("La bonne réponse était :",
                  reponses[bonne_reponse])

    pourcentage = score / len(selection) * 100

    print("\n========== RÉSULTAT ==========")
    print(f"Score : {score}/{len(selection)}")
    print(f"Réussite : {pourcentage:.1f}%")

    enregistrer_resultat(score, len(selection))


# ENREGISTREMENT DES RÉSULTATS

def enregistrer_resultat(score, total):
    historique = charger_resultats()

    historique.append({
        "score": score,
        "total": total,
        "pourcentage": round(score / total * 100, 1),
        "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    })

    with open("resultats.json", "w", encoding="utf-8") as fichier:
        json.dump(historique, fichier, indent=4, ensure_ascii=False)

    print("Résultat enregistré !")


# CHARGEMENT DES RÉSULTATS

def charger_resultats():
    if os.path.exists("resultats.json"):
        try:
            with open("resultats.json", "r", encoding="utf-8") as fichier:
                return json.load(fichier)
        except json.JSONDecodeError:
            print("Le fichier des résultats est invalide.")
    return []


# AFFICHAGE DE L'HISTORIQUE

def afficher_resultats():
    historique = charger_resultats()

    if not historique:
        print("Aucun résultat enregistré.")
        return

    print("\n========== HISTORIQUE ==========")

    for i, resultat in enumerate(historique, 1):
        print(f"\nPartie {i}")
        print("Date :", resultat["date"])
        print("Score :", resultat["score"], "/", resultat["total"])
        print("Réussite :", resultat["pourcentage"], "%")


# MENU PRINCIPAL

def menu():
    print("\n" + "~" * 50)
    print("             SUPER QUIZ")
    print("~" * 50)
    print("1 - Commencer un quiz")
    print("2 - Afficher les résultats précédents")
    print("3 - Quitter")


# INITIALISATION DES FICHIERS

def charger_memoire():
    if not os.path.exists("questions.json"):
        print("Création du fichier de questions.")
        enregistrer_question()

    if not os.path.exists("resultats.json"):
        with open("resultats.json", "w", encoding="utf-8") as fichier:
            json.dump([], fichier)


# PROGRAMME PRINCIPAL

def quiz():
    charger_memoire()

    while True:
        menu()

        try:
            choix = int(input("Votre choix : "))

            if choix == 1:
                question()

            elif choix == 2:
                afficher_resultats()

            elif choix == 3:
                print("Fermeture du programme.")
                break

            else:
                print("Choix invalide.")

        except ValueError:
            print("Veuillez entrer un nombre valide.")


quiz()