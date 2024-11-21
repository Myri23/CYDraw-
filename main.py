from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

window = Tk()
window.geometry('900x500')
window.minsize(width=900,height=500)
window.maxsize(width=1100,height=600)
window.title('Draw ++')

# Initialisation des variables globales
opened_files = []
current_file_index = None

#création menu principal
my_menu=Menu(window)

#creating submenus
file_sm=Menu(my_menu,tearoff=0)
edit_sm=Menu(my_menu,tearoff=0)

# Créer le sous-menu pour basculer entre les fichiers
switch_sm = Menu(file_sm, tearoff=0)

def update_line_numbers():
    """Met à jour les numéros de ligne en fonction du contenu de la zone de texte."""
    line_numbers.config(state='normal')  # Activer l'édition temporaire
    line_numbers.delete(1.0, END)  #Effacer les anciens numéros de ligne

    # Obtenir le nombre total de lignes dans la zone de texte principale
    total_lines = int(text_area.index('end-1c').split('.')[0])

    # Ajouter les numéros de ligne correspondants
    for i in range(1, total_lines + 1):
        line_numbers.insert(END, f"{i}\n")

    line_numbers.config(state='disabled')  # Désactiver l'édition pour empêcher la modification manuelle

# Fonction pour basculer entre les fichiers ouverts
def switch_file(index):
    global current_file_index
    current_file_index = index  # Mettre à jour l'index du fichier courant
    file_path = opened_files[current_file_index]  # Récupérer le fichier courant
    with open(file_path, 'r') as file:
        content = file.read()  # Lire le contenu du fichier
    text_area.delete(1.0, END)  # Effacer le contenu précédent de la zone de texte
    text_area.insert(END, content)  # Insérer le contenu du fichier dans la zone de texte

# Fonction pour supprimer un fichier du menu
def remove_file(index):
    global current_file_index
    # Vérifier si le fichier à supprimer est celui actuellement affiché
    if index == current_file_index:
        # Effacer le texte de la zone de texte
        text_area.delete(1.0, END)  # Effacer le texte affiché
    opened_files.pop(index)  # Supprimer le fichier de la liste
    update_switch_menu()  # Mettre à jour le sous-menu pour refléter les changements
    # Si on supprime le fichier actuellement affiché, on doit en afficher un autre
    if current_file_index is not None:
        if current_file_index >= index:  # Si le fichier supprimé était avant ou le même que le courant
            current_file_index -= 1  # Diminuer l'index courant
        if current_file_index >= 0:  # S'assurer qu'il y a encore un fichier affiché
            switch_file(current_file_index)  # Afficher le fichier courant
        else:
            current_file_index = None  # Aucune fichier à afficher

# Fonction pour mettre à jour le sous-menu Switch
def update_switch_menu():
    switch_sm.delete(0, END)  # Effacer le contenu précédent du sous-menu
    for index, file_path in enumerate(opened_files):  # Itérer sur les fichiers ouverts
        # Ajouter l'option pour basculer vers le fichier
        switch_sm.add_command(label=f"Switch to {file_path.split('/')[-1]}",
                               command=lambda i=index: switch_file(i))
        # Ajouter l'option pour supprimer le fichier
        switch_sm.add_command(label=f"Remove {file_path.split('/')[-1]}",
                               command=lambda i=index: remove_file(i))

# Fonction pour ajouter un fichier à la liste
def add_file_to_menu(file_path):
    opened_files.append(file_path)  # Ajouter le chemin du fichier à la liste
    update_switch_menu()  # Mettre à jour le sous-menu
    switch_file(len(opened_files) - 1)  # Afficher le dernier fichier ouvert

def open_file():
    # Ouvrir une boîte de dialogue pour sélectionner le fichier
    file_paths = filedialog.askopenfilenames(title="Select Files", 
                                               filetypes=(("All files", "*.*"),))  # Filtrer tous les fichiers

    if file_paths:  # Si des fichiers sont sélectionnés
        for file_path in file_paths:  # Ajouter chaque fichier sélectionné à la liste
            add_file_to_menu(file_path)

# Fonction pour "Enregistrer sous..."
def save_as():
    # Ouvrir une fenêtre de dialogue pour que l'utilisateur choisisse le nom du fichier SANS l'extension
    file_path = filedialog.asksaveasfilename(initialfile="File",  # Nom par défaut
                                             title="Save your .dpp file",
                                             defaultextension=".dpp",  # Extension par défaut .dpp
                                             filetypes=[("Draw++ files", "*.dpp")])  # Seule l'extension .dpp est permise
    # Si un fichier est sélectionné
    if file_path:
        # Ajouter '.dpp' si ce n'est pas déjà fait (vérification par sécurité)
        if not file_path.endswith(".dpp"):
            file_path += ".dpp"
        
        try:
            # Ouvrir le fichier en mode écriture
            with open(file_path, "w") as file:
                # Écrire le contenu de la zone de texte dans le fichier
                file.write(text_area.get(1.0, END))  # 1.0 correspond au début du texte, END à la fin
            print(f"Fichier sauvegardé sous : {file_path}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")



def edit_file():
    global text_area, line_numbers
    # Création de la zone de numéros de ligne
    line_numbers = Text(window, width=4, padx=3, takefocus=0, border=0, background="lightgrey", state='disabled')
    line_numbers.place(relx=0.05, rely=0.1, relheight=0.7)

    # Création de la zone de texte
    text_area = Text(window, undo=True, wrap="word")
    text_area.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.7)

    # Lier les événements pour mettre à jour les numéros de ligne
    text_area.bind("<KeyRelease>", lambda event: update_line_numbers())
    text_area.bind("<MouseWheel>", lambda event: update_line_numbers())

    # Initialiser les numéros de ligne au début
    update_line_numbers()
    
    file_path = filedialog.askopenfilename(defaultextension=".txt", 
                                           filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    
    if file_path:
        # Lire le contenu du fichier et l'afficher dans la zone de texte
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                text_area.insert(END, content)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier : {e}")
            return





def create_new_file():
    """Création d'une nouvelle zone de texte avec les numéros de ligne."""
    global text_area, line_numbers

    # Détruire les anciennes zones de texte (si existantes)
    for widget in window.winfo_children():
        if isinstance(widget, Text):
            widget.destroy()

    # Création de la zone de numéros de ligne
    line_numbers = Text(window, width=4, padx=3, takefocus=0, border=0, background="lightgrey", state='disabled')
    line_numbers.place(relx=0.05, rely=0.1, relheight=0.7)

    # Création de la zone de texte
    text_area = Text(window, undo=True, wrap="word")
    text_area.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.7)

    # Lier les événements pour mettre à jour les numéros de ligne
    text_area.bind("<KeyRelease>", lambda event: update_line_numbers())
    text_area.bind("<MouseWheel>", lambda event: update_line_numbers())

    # Initialiser les numéros de ligne au début
    update_line_numbers()

 



#filling submenus
file_sm.add_command(label="Save")
file_sm.add_command(label="Save as", command=save_as)
file_sm.add_command(label="Create new file",command=create_new_file)
file_sm.add_command(label="Edit File", command=edit_file)
file_sm.add_command(label="Switch save")
edit_sm.add_command(label="Copy")
edit_sm.add_command(label="Paste")

#lier le sous menus aux boutons du menu
my_menu.add_cascade(label="File",menu=file_sm)
my_menu.add_cascade(label="Edit",menu=edit_sm)


#lier le menu principal à la page
window.config(menu=my_menu)



window.mainloop()


"""
Pour vérifier la syntaxe - à améliorer

def check_syntax():
    content = text_area.get("1.0", "end-1c")  # Récupérer le texte de la zone
    try:
        # Simuler une vérification de grammaire
        lines = content.split("\n")
        for line in lines:
            if not line.endswith(";"):
                raise SyntaxError(f"Ligne invalide (pas de point-virgule) : {line}")
        messagebox.showinfo("Succès", "Aucune erreur de syntaxe détectée !")
    except SyntaxError as e:
        messagebox.showerror("Erreur de syntaxe", str(e))

edit_sm.add_command(label="Check Syntax", command=check_syntax)
"""