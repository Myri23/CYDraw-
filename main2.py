from tkinter import *
from tkinter import messagebox, filedialog
import re


# Fenêtre principale
window = Tk()
window.geometry('900x590')
window.minsize(width=900, height=600)
window.title('Draw ++')

# Variables globales
opened_files = [] # Liste pour stocker les chemins des fichiers ouverts.
current_file_index = None # Index du fichier actuellement ouvert dans la liste.
file_buttons_frame = Frame(window, bg="#333333", height=30)
file_buttons_frame.pack(side="top", fill="x")

# Fonction pour sauvegarder sous un nouveau fichier
def save_as():
    global current_file_index

    file_path = filedialog.asksaveasfilename(defaultextension=".dpp",
                                             filetypes=[("Draw++ files", "*.dpp")])
    if file_path:
        try:
            with open(file_path, "w") as file:
                file.write(text_area.get(1.0, END))  # Sauvegarde du contenu
            messagebox.showinfo("Success", "Fichier sauvegardé avec succès.")
            
            # Met à jour opened_files et current_file_index
            if current_file_index is None or opened_files[current_file_index] == "Untitled":
                opened_files[current_file_index] = file_path
            else:
                opened_files.append(file_path)
                current_file_index = len(opened_files) - 1

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer : {e}")



def save():
    global current_file_index

    # Si le fichier courant est "Untitled", on demande un emplacement pour sauvegarder
    if current_file_index is None or opened_files[current_file_index] == "Untitled":
        save_as()
    else:
        # Sauvegarde dans le fichier existant
        file_path = opened_files[current_file_index]
        try:
            with open(file_path, "w") as file:
                file.write(text_area.get(1.0, END))  # Sauvegarder tout le contenu
            messagebox.showinfo("Success", f"Fichier sauvegardé : {file_path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder le fichier : {e}")


# Fonction pour ouvrir un fichier
def open_file():
    global current_file_index, opened_files
    # Ouvre une boîte de dialogue pour choisir un fichier.
    file_path = filedialog.askopenfilename(defaultextension=".dpp", 
                                           filetypes=[("Text Files", "*.dpp"), ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                # On récupère Le contenu du fichier qui est chargé
                content = file.read()
                text_area.delete(1.0, END)
                # Le contenu du fichier est chargé dans la zone de texte.
                text_area.insert(1.0, content)
            if file_path not in opened_files:
                opened_files.append(file_path)
            current_file_index = opened_files.index(file_path)
            update_line_numbers()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier : {e}")
    update_file_buttons()

# Fonction pour créer un nouveau fichier
def create_new_file():
    global current_file_index, opened_files

    # Vérifie s'il existe déjà un fichier "Untitled" non sauvegardé
    if current_file_index is not None and opened_files[current_file_index] == "Untitled":
        opened_files.pop(current_file_index)

    # Efface la zone de texte pour un nouveau fichier
    text_area.delete(1.0, END)

    # Ajouter un nouveau fichier temporaire "Untitled"
    opened_files.append("Untitled")
    current_file_index = len(opened_files) - 1
    print("Nouveau fichier créé : Untitled")

    # Met à jour les numéros de ligne
    update_file_buttons()
    update_line_numbers()






# Fonction pour mettre à jour dynamiquement les numéros de ligne visibles
def update_line_numbers(*args):
    # Rend le widget des numéros de ligne modifiable temporairement.
    line_numbers.config(state='normal')
    # Efface le contenu existant des numéros de ligne.
    line_numbers.delete(1.0, END)

    # Récupérer la première et dernière ligne visible
    # Calcule la première ligne visible dans text_area en utilisant @0,0 (coordonnées de la zone).
    first_visible_line = int(text_area.index('@0,0').split('.')[0])
    # Calcule la dernière ligne visible à partir de la hauteur du widget.
    last_visible_line = int(text_area.index('@0,%d' % text_area.winfo_height()).split('.')[0])

    # Afficher uniquement les numéros des lignes visibles
    # Crée une chaîne contenant les numéros de ligne visibles.
    line_content = "\n".join(str(i) for i in range(first_visible_line, last_visible_line + 1))
    # Insère les numéros de ligne.
    line_numbers.insert(1.0, line_content)

    # Rend le widget à nouveau non modifiable.
    line_numbers.config(state='disabled')

def switch_file(index):
    """Bascule vers un fichier de la liste des fichiers ouverts."""
    global current_file_index
    if 0 <= index < len(opened_files):
        current_file_index = index
        file_path = opened_files[index]
        try:
            with open(file_path, "r") as file:
                content = file.read()
                text_area.delete(1.0, END)  # Efface le contenu actuel
                text_area.insert(END, content)  # Charge le nouveau contenu
            update_line_numbers()
            print(f"Switched to file: {file_path}")  # Pour le debug
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier : {e}")

def remove_file(index):
    """Ferme un fichier ouvert et met à jour les boutons."""
    global current_file_index

    # Vérifie si l'index est valide
    if 0 <= index < len(opened_files):
        closed_file = opened_files.pop(index)  # Retire le fichier de la liste
        print(f"Fichier fermé : {closed_file}")

        # Si on ferme le fichier actuel
        if current_file_index == index:
            if opened_files:  # Basculer vers le premier fichier de la liste
                current_file_index = 0
                switch_file(current_file_index)
            else:  # Plus aucun fichier ouvert
                current_file_index = None
                text_area.delete(1.0, END)  # Efface la zone de texte

        # Si on ferme un fichier avant le fichier courant, ajuster l'index
        elif current_file_index > index:
            current_file_index -= 1

        # Mettre à jour les boutons des fichiers ouverts
        update_file_buttons()


def switch_file_from_popup(index, popup):
    """Permet de basculer vers un fichier depuis la boîte de dialogue."""
    switch_file(index)
    popup.destroy()  # Ferme la fenêtre pop-up


def update_file_buttons():
    """Met à jour la liste des fichiers ouverts en haut de l'application."""
    global file_buttons_frame

    # Effacer les anciens boutons
    for widget in file_buttons_frame.winfo_children():
        widget.destroy()

    # Créer un bouton pour chaque fichier ouvert
    for index, file_path in enumerate(opened_files):
        file_name = file_path.split("/")[-1]  # Nom sans chemin complet

        # Conteneur pour le bouton du fichier et le bouton "fermer"
        button_container = Frame(file_buttons_frame, bg="#2B2B2B")
        button_container.pack(side="left", padx=2)

        # Bouton pour switcher vers le fichier
        Button(button_container, text=file_name, bg="#4CAF50", fg="white",
               font=("Helvetica", 10), command=lambda i=index: switch_file(i),
               bd=0, relief="flat", activebackground="#45a049", cursor="hand2").pack(side="left")

        # Bouton pour fermer le fichier (croix rouge)
        Button(button_container, text="x", bg="#FF6347", fg="white",
               font=("Helvetica", 10, "bold"), command=lambda i=index: remove_file(i),
               bd=0, relief="flat", activebackground="#FF4500", cursor="hand2").pack(side="right")

# Fonction pour synchroniser le défilement entre la zone de texte et les numéros de ligne
def on_scroll(*args): 
    # args : permet de récupérer les arguments passés par le défilement (scroll ou moveto).
    if args and args[0] in ('moveto', 'scroll'):
        # Fait défiler les deux widgets en synchronisation.
        text_area.yview(*args)
        line_numbers.yview(*args)
        # Met à jour les numéros de ligne après chaque défilement.
        update_line_numbers()


# Synchronisation après redimensionnement
def on_resize(event): # event représente l'événement de redimensionnement.
    update_line_numbers()
  
def check_syntax():
    """
    Vérifie les erreurs de syntaxe dans le contenu de la zone de texte principale.
    Met en évidence les erreurs et propose des corrections.
    """
    # Afficher la zone de correction lorsque le bouton "Check" est cliqué
    correction_area.config(state='normal')  # Rendre la zone de correction modifiable temporairement

    # Récupération du texte et initialisation
    content = text_area.get("1.0", "end-1c")  # Texte de la zone principale
    lines = content.split("\n")
    error_found = False

    # Effacer les anciens surlignages et corrections
    text_area.tag_delete("error_underline")
    correction_area.delete(1.0, END)  # Effacer le contenu de la zone de correction

    # Parcours des lignes pour vérifier les erreurs
    for idx, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line and not stripped_line.endswith(";"):  # Condition pour une erreur
            error_found = True

            # Soulignement rouge pour la ligne avec erreur
            start_idx = f"{idx + 1}.0"
            end_idx = f"{idx + 1}.end"
            text_area.tag_add("error_underline", start_idx, end_idx)
            text_area.tag_config("error_underline", underline=1, foreground="red")

            # Ajout d'une correction proposée dans la zone dédiée
            corrected_line = stripped_line + ";"
            correction_area.insert(
                END,
                f"Ligne {idx + 1} : {corrected_line}\n",
                "correction"
            )

    # Si aucune erreur détectée
    if not error_found:
        messagebox.showinfo("Succès", "Aucune erreur détectée !")
    
    # Désactiver la zone de correction après modifications
    correction_area.config(state='disabled')

    # Style pour les corrections (vert)
    correction_area.tag_config("correction", foreground="green")



# Configuration de la barre latérale
# Frame : Un conteneur pour organiser les widgets.
sidebar = Frame(window, bg="#2B2B2B", width=200) # gris foncé.
sidebar.pack(fill="y", side="left") # Remplit verticalement et se place à gauche.


# Titre de la barre latérale
Label(sidebar, text="Draw++", bg="#2B2B2B", fg="white", font=("Helvetica", 18, "bold")).pack(pady=20)

# Ajout des boutons centrés dans la barre latérale
def create_styled_button(parent, text, command):
    # parent : Le conteneur dans lequel placer le bouton.
    # text : Le texte affiché sur le bouton.
    # command : La fonction exécutée lorsqu'on clique sur le bouton.

    return Button(parent, text=text, command=command, bg="#4CAF50", fg="white",
                  font=("Helvetica", 12, "bold"), bd=0, relief="flat", padx=10, pady=5,
                  activebackground="#45a049", cursor="hand2", highlightthickness=0)

button_frame = Frame(sidebar, bg="#2B2B2B")
button_frame.pack(expand=True)

for btn_text, cmd in [("Save", save), ("Save As", save_as), ("Open File", open_file), ("New File", create_new_file), ("Check", check_syntax)]:
    button = create_styled_button(button_frame, btn_text, cmd)
    # Espacement vertical et alignement horizontal.
    button.pack(pady=10, fill="x", padx=10) 

# Frame pour contenir line_numbers et text_area
text_frame = Frame(window)
text_frame.pack(side="top", fill="both", expand=True)

# Numéros de ligne (placés dans text_frame)
line_numbers = Text(text_frame, width=4, padx=5, takefocus=0, border=0, 
                    background="#333333", foreground="#AAAAAA", 
                    font=("Consolas", 12), state='disabled', spacing1=0)
line_numbers.pack(side="left", fill="y")  # Toujours à gauche, remplit verticalement

# Zone principale de texte (placée dans text_frame)
text_area = Text(text_frame, undo=True, wrap="word", yscrollcommand=on_scroll, 
                 bg="#1E1E1E", fg="#FFFFFF", insertbackground="white", 
                 font=("Consolas", 12), borderwidth=0, highlightthickness=0)
text_area.pack(side="right", fill="both", expand=True)  # Remplit le reste de l'espace

# Zone de correction (en dessous de text_frame)
correction_area = Text(window, wrap="word", state='disabled', background="#333333", 
                       height=4, borderwidth=0, highlightthickness=0)
correction_area.pack(side="bottom", fill="x", padx=1, pady=1)


# Synchronisation des événements pour mettre à jour les numéros de ligne
text_area.bind("<KeyRelease>", update_line_numbers) # Lie les événements de frappe 
text_area.bind("<Configure>", on_resize) #  et de redimensionnement pour maintenir les numéros de ligne à jour.
text_area.bind("<KeyPress>", update_line_numbers)  # Mise à jour avec la frappe de touche

# Suppression de la barre de défilement (uniquement logique interne)
# Synchronise le défilement de la zone de texte à la verticl
text_area.config(yscrollcommand=on_scroll) 

# Mise à jour initiale des numéros de ligne
update_line_numbers()

# Lancer l'application
window.mainloop()
