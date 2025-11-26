import tkinter as tk
from tkinter import messagebox
import pickle

class GestionnaireTachesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Tâches")

        # Interface utilisateur
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.tache_label = tk.Label(self.frame, text="Tâche :")
        self.tache_label.grid(row=0, column=0)

        self.tache_entry = tk.Entry(self.frame, width=30)
        self.tache_entry.grid(row=0, column=1)

        self.ajouter_button = tk.Button(self.frame, text="Ajouter", width=10, command=self.ajouter_tache)
        self.ajouter_button.grid(row=0, column=2)

        self.listbox = tk.Listbox(self.frame, height=10, width=50)
        self.listbox.grid(row=1, column=0, columnspan=2, pady=10)

        self.marquer_button = tk.Button(self.frame, text="Marquer comme faite", command=self.marquer_faite)
        self.marquer_button.grid(row=2, column=0, pady=5)

        self.supprimer_button = tk.Button(self.frame, text="Supprimer", command=self.supprimer_tache)
        self.supprimer_button.grid(row=2, column=1, pady=5)

        self.sauvegarder_button = tk.Button(self.frame, text="Sauvegarder", command=self.sauvegarder_taches)
        self.sauvegarder_button.grid(row=3, column=0, pady=5)

        self.charger_button = tk.Button(self.frame, text="Charger", command=self.charger_taches)
        self.charger_button.grid(row=3, column=1, pady=5)

        # Charger les tâches si disponibles
        self.charger_taches()

    def ajouter_tache(self):
        """Ajoute une nouvelle tâche à la liste."""
        tache = self.tache_entry.get()
        if tache != "":
            self.listbox.insert(tk.END, tache)
            self.tache_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Erreur", "Veuillez entrer une tâche.")

    def marquer_faite(self):
        """Marque la tâche sélectionnée comme faite en la grisant."""
        try:
            index = self.listbox.curselection()[0]
            tache = self.listbox.get(index)
            self.listbox.delete(index)
            self.listbox.insert(index, tache + " [FAITE]")
        except IndexError:
            messagebox.showwarning("Erreur", "Veuillez sélectionner une tâche.")

    def supprimer_tache(self):
        """Supprime la tâche sélectionnée."""
        try:
            index = self.listbox.curselection()[0]
            self.listbox.delete(index)
        except IndexError:
            messagebox.showwarning("Erreur", "Veuillez sélectionner une tâche.")

    def sauvegarder_taches(self):
        """Sauvegarde les tâches dans un fichier en utilisant pickle."""
        taches = self.listbox.get(0, tk.END)
        with open("taches.pkl", "wb") as f:
            pickle.dump(taches, f)
        messagebox.showinfo("Sauvegarde", "Tâches sauvegardées avec succès.")

    def charger_taches(self):
        """Charge les tâches depuis un fichier s'il existe."""
        try:
            with open("taches.pkl", "rb") as f:
                taches = pickle.load(f)
                self.listbox.delete(0, tk.END)
                for tache in taches:
                    self.listbox.insert(tk.END, tache)
        except FileNotFoundError:
            pass

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = GestionnaireTachesApp(root)
    root.mainloop()