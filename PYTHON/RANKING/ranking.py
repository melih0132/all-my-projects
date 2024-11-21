import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
from typing import Optional, Tuple


class RankingApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Application de Classement")
        self.root.geometry("1000x600")  # Fenêtre plus grande pour une meilleure lisibilité
        self.root.minsize(800, 500)  # Taille minimum pour éviter les problèmes d'affichage
        
        # Variables
        self.ranking_name = tk.StringVar()
        self.item_name = tk.StringVar()
        self.item_score = tk.StringVar()
        self.current_ranking_id: Optional[int] = None
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_rankings)
        
        # Configuration de la base de données
        self.setup_database()
        # Configuration du style
        self.setup_styles()
        # Création de l'interface
        self.create_widgets()
        # Chargement initial des données
        self.load_rankings()

    def setup_database(self):
        """Initialise la connexion à la base de données et crée les tables si nécessaire."""
        self.conn = sqlite3.connect('rankings.db')
        self.cursor = self.conn.cursor()
        
        # Utilisation de FOREIGN KEY pour maintenir l'intégrité référentielle
        self.cursor.execute('''PRAGMA foreign_keys = ON''')
        
        # Création des tables avec contraintes appropriées
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS rankings (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            ranking_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            score REAL NOT NULL CHECK(score >= 0 AND score <= 10),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ranking_id) REFERENCES rankings(id) ON DELETE CASCADE,
            UNIQUE(ranking_id, name)
        )''')
        
        self.conn.commit()

    def setup_styles(self):
        """Configure les styles de l'application pour une apparence moderne."""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Couleurs
        bg_color = "#f0f0f5"
        accent_color = "#4a90e2"
        
        self.root.configure(bg=bg_color)
        
        # Configuration des styles pour les différents widgets
        style.configure("MainFrame.TFrame", background=bg_color)
        style.configure("Header.TLabel", 
                       font=("Helvetica", 16, "bold"),
                       background=bg_color,
                       foreground="#2c3e50")
        style.configure("Subheader.TLabel",
                       font=("Helvetica", 12),
                       background=bg_color,
                       foreground="#34495e")
        
        # Style des boutons
        style.configure("Action.TButton",
                       font=("Helvetica", 10),
                       background=accent_color,
                       padding=10)
        
        # Style des entrées
        style.configure("Custom.TEntry",
                       font=("Helvetica", 10),
                       padding=5)

    def create_widgets(self):
        """Crée et dispose les widgets de l'interface."""
        # Configuration du grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Création des frames principaux
        left_frame = ttk.Frame(self.root, style="MainFrame.TFrame", padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        right_frame = ttk.Frame(self.root, style="MainFrame.TFrame", padding=10)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        self._create_left_frame(left_frame)
        self._create_right_frame(right_frame)

    def _create_left_frame(self, parent: ttk.Frame):
        """Crée les widgets du panneau gauche."""
        # Titre
        ttk.Label(parent, 
                 text="Classements",
                 style="Header.TLabel").pack(pady=(0, 10))
        
        # Barre de recherche
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame,
                 text="🔍",
                 style="Subheader.TLabel").pack(side=tk.LEFT, padx=5)
        ttk.Entry(search_frame,
                 textvariable=self.search_var,
                 style="Custom.TEntry").pack(side=tk.LEFT,
                                           fill=tk.X,
                                           expand=True)
        
        # Liste des classements
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.ranking_listbox = tk.Listbox(list_frame,
                                        font=("Helvetica", 10),
                                        selectmode=tk.SINGLE,
                                        activestyle='none',
                                        highlightthickness=1)
        self.ranking_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.ranking_listbox.bind("<<ListboxSelect>>", self.on_ranking_select)
        
        # Scrollbar pour la liste
        scrollbar = ttk.Scrollbar(list_frame,
                                orient=tk.VERTICAL,
                                command=self.ranking_listbox.yview)
        self.ranking_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Boutons de gestion des classements
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame,
                  text="Nouveau Classement",
                  style="Action.TButton",
                  command=self.create_new_ranking).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame,
                  text="Supprimer Classement",
                  style="Action.TButton",
                  command=self.delete_ranking).pack(fill=tk.X, pady=2)

    def _create_right_frame(self, parent: ttk.Frame):
        """Crée les widgets du panneau droit."""
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(3, weight=1)
        
        # En-tête
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Label(header_frame,
                 text="Détails du Classement",
                 style="Header.TLabel").pack()
        
        # Formulaire
        form_frame = ttk.Frame(parent)
        form_frame.grid(row=1, column=0, sticky="ew", pady=10)
        
        # Grid configuration pour le formulaire
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Labels et entrées
        ttk.Label(form_frame,
                 text="Nom:",
                 style="Subheader.TLabel").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Entry(form_frame,
                 textvariable=self.item_name,
                 style="Custom.TEntry").grid(row=0, column=1, sticky="ew", padx=5)
        
        ttk.Label(form_frame,
                 text="Score:",
                 style="Subheader.TLabel").grid(row=1, column=0, sticky="w", padx=5)
        score_entry = ttk.Entry(form_frame,
                              textvariable=self.item_score,
                              style="Custom.TEntry")
        score_entry.grid(row=1, column=1, sticky="ew", padx=5)
        
        # Validation des entrées
        score_entry.bind('<KeyRelease>', self._validate_score_input)
        
        # Boutons d'action
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=2, column=0, sticky="ew", pady=10)
        
        ttk.Button(buttons_frame,
                  text="Ajouter Item",
                  style="Action.TButton",
                  command=self.add_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame,
                  text="Modifier Sélection",
                  style="Action.TButton",
                  command=self.edit_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame,
                  text="Supprimer Sélection",
                  style="Action.TButton",
                  command=self.delete_item).pack(side=tk.LEFT, padx=5)
        
        # Liste des items
        list_frame = ttk.Frame(parent)
        list_frame.grid(row=3, column=0, sticky="nsew", pady=10)
        
        self.item_listbox = tk.Listbox(list_frame,
                                     font=("Helvetica", 10),
                                     selectmode=tk.SINGLE,
                                     activestyle='none')
        self.item_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.item_listbox.bind('<<ListboxSelect>>', self.on_item_select)
        
        scrollbar = ttk.Scrollbar(list_frame,
                                orient=tk.VERTICAL,
                                command=self.item_listbox.yview)
        self.item_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _validate_score_input(self, event):
        """Valide l'entrée du score en temps réel."""
        value = self.item_score.get()
        if value:
            try:
                score = float(value)
                if not (0 <= score <= 10):
                    self.item_score.set(value[:-1])
            except ValueError:
                self.item_score.set(value[:-1])

    def filter_rankings(self, *args):
        """Filtre la liste des classements selon la recherche."""
        search_term = self.search_var.get().lower()
        self.update_ranking_listbox(search_term)

    def create_new_ranking(self):
        """Crée un nouveau classement."""
        name = simpledialog.askstring("Nouveau Classement",
                                    "Nom du classement:",
                                    parent=self.root)
        if name and name.strip():
            try:
                self.cursor.execute("INSERT INTO rankings (name) VALUES (?)",
                                  (name.strip(),))
                self.conn.commit()
                self.update_ranking_listbox()
                messagebox.showinfo("Succès",
                                  f"Le classement '{name}' a été créé.")
            except sqlite3.IntegrityError:
                messagebox.showerror("Erreur",
                                   "Un classement avec ce nom existe déjà.")

    def delete_ranking(self):
        """Supprime le classement sélectionné."""
        if not self.current_ranking_id:
            messagebox.showerror("Erreur",
                               "Aucun classement sélectionné.")
            return
            
        name = self.ranking_name.get()
        if messagebox.askyesno("Confirmation",
                             f"Voulez-vous vraiment supprimer le classement '{name}' ?"):
            self.cursor.execute("DELETE FROM rankings WHERE id=?",
                              (self.current_ranking_id,))
            self.conn.commit()
            self.current_ranking_id = None
            self.ranking_name.set("")
            self.update_ranking_listbox()
            self.item_listbox.delete(0, tk.END)

    def load_rankings(self):
        """Charge les classements depuis la base de données."""
        self.update_ranking_listbox()

    def update_ranking_listbox(self, search_term: str = ""):
        """Met à jour la liste des classements."""
        self.ranking_listbox.delete(0, tk.END)
        query = """
            SELECT name 
            FROM rankings 
            WHERE LOWER(name) LIKE ? 
            ORDER BY name ASC
        """
        self.cursor.execute(query, (f"%{search_term}%",))
        for ranking in self.cursor.fetchall():
            self.ranking_listbox.insert(tk.END, ranking[0])

    def on_ranking_select(self, event):
        """Gère la sélection d'un classement."""
        selection = self.ranking_listbox.curselection()
        if not selection:
            return
            
        ranking_name = self.ranking_listbox.get(selection[0])
        self.ranking_name.set(ranking_name)
        
        # Récupère l'ID du classement
        self.cursor.execute("SELECT id FROM rankings WHERE name=?",
                          (ranking_name,))
        result = self.cursor.fetchone()
        if result:
            self.current_ranking_id = result[0]
            self.update_item_listbox()
        else:
            self.current_ranking_id = None

    def update_item_listbox(self):
        """Met à jour la liste des items du classement sélectionné."""
        self.item_listbox.delete(0, tk.END)
        if not self.current_ranking_id:
            return
            
        self.cursor.execute("""
            SELECT name, score 
            FROM items 
            WHERE ranking_id=? 
            ORDER BY score DESC, name ASC
        """, (self.current_ranking_id,))
        
        for idx, (name, score) in enumerate(self.cursor.fetchall(), 1):
            self.item_listbox.insert(tk.END, f"{idx}. {name}: {score:.1f}")

    def on_item_select(self, event):
        """Gère la sélection d'un item."""
        selection = self.item_listbox.curselection()
        if not selection:
            return
            
        item_text = self.item_listbox.get(selection[0])
        # Extrait le nom et le score (ignore le numéro d'index)
        name = item_text.split(": ")[0].split(". ", 1)[1]
        score = float(item_text.split(": ")[1])
        
        self.item_name.set(name)
        self.item_score.set(f"{score:.1f}")

    def validate_inputs(self) -> Tuple[bool, str]:
        """Valide les entrées utilisateur.
        
        Returns:
            Tuple[bool, str]: (validation_success, error_message)
        """
        item_name = self.item_name.get().strip()
        
        if not self.current_ranking_id:
            return False, "Aucun classement sélectionné."
            
        if not item_name:
            return False, "Le nom de l'item ne peut pas être vide."
            
        try:
            score = float(self.item_score.get().strip())
            if not (0 <= score <= 10):
                return False, "Le score doit être entre 0 et 10."
        except ValueError:
            return False, "Le score doit être un nombre."
            
        return True, ""

    def add_item(self):
        """Ajoute un nouvel item au classement."""
        is_valid, error_msg = self.validate_inputs()
        if not is_valid:
            messagebox.showerror("Erreur de validation", error_msg)
            return

        item_name = self.item_name.get().strip()
        item_score = float(self.item_score.get().strip())

        try:
            self.cursor.execute("""
                INSERT INTO items (ranking_id, name, score)
                VALUES (?, ?, ?)
            """, (self.current_ranking_id, item_name, item_score))
            
            self.conn.commit()
            self.update_item_listbox()
            
            # Réinitialise les champs
            self.item_name.set("")
            self.item_score.set("")
            
            messagebox.showinfo("Succès", f"Item '{item_name}' ajouté avec succès.")
            
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Erreur",
                f"Un item nommé '{item_name}' existe déjà dans ce classement."
            )

    def edit_item(self):
        """Modifie l'item sélectionné."""
        selection = self.item_listbox.curselection()
        if not selection:
            messagebox.showerror("Erreur", "Aucun item sélectionné.")
            return

        is_valid, error_msg = self.validate_inputs()
        if not is_valid:
            messagebox.showerror("Erreur de validation", error_msg)
            return

        item_text = self.item_listbox.get(selection[0])
        original_name = item_text.split(": ")[0].split(". ", 1)[1]
        
        new_name = self.item_name.get().strip()
        new_score = float(self.item_score.get().strip())

        try:
            self.cursor.execute("""
                UPDATE items 
                SET name = ?, score = ?
                WHERE ranking_id = ? AND name = ?
            """, (new_name, new_score, self.current_ranking_id, original_name))
            
            self.conn.commit()
            self.update_item_listbox()
            
            messagebox.showinfo("Succès", f"Item modifié avec succès.")
            
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Erreur",
                f"Un item nommé '{new_name}' existe déjà dans ce classement."
            )

    def delete_item(self):
        """Supprime l'item sélectionné."""
        selection = self.item_listbox.curselection()
        if not selection:
            messagebox.showerror("Erreur", "Aucun item sélectionné.")
            return

        item_text = self.item_listbox.get(selection[0])
        item_name = item_text.split(": ")[0].split(". ", 1)[1]

        if messagebox.askyesno(
            "Confirmation",
            f"Voulez-vous vraiment supprimer l'item '{item_name}' ?"
        ):
            self.cursor.execute("""
                DELETE FROM items 
                WHERE ranking_id = ? AND name = ?
            """, (self.current_ranking_id, item_name))
            
            self.conn.commit()
            self.update_item_listbox()
            
            # Réinitialise les champs
            self.item_name.set("")
            self.item_score.set("")
            
            messagebox.showinfo("Succès", f"Item '{item_name}' supprimé.")

    def export_ranking(self):
        """Exporte le classement actuel au format CSV."""
        if not self.current_ranking_id:
            messagebox.showerror("Erreur", "Aucun classement sélectionné.")
            return

        try:
            from tkinter import filedialog
            import csv
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Exporter le classement"
            )
            
            if filename:
                self.cursor.execute("""
                    SELECT name, score 
                    FROM items 
                    WHERE ranking_id = ? 
                    ORDER BY score DESC, name ASC
                """, (self.current_ranking_id,))
                
                items = self.cursor.fetchall()
                
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Nom', 'Score'])  # En-têtes
                    writer.writerows(items)
                
                messagebox.showinfo(
                    "Succès",
                    f"Le classement a été exporté vers {filename}"
                )
                
        except Exception as e:
            messagebox.showerror(
                "Erreur d'exportation",
                f"Une erreur est survenue lors de l'exportation : {str(e)}"
            )

    def backup_database(self):
        """Crée une sauvegarde de la base de données."""
        try:
            from tkinter import filedialog
            import shutil
            from datetime import datetime
            
            backup_filename = filedialog.asksaveasfilename(
                defaultextension=".db",
                filetypes=[("Database files", "*.db")],
                initialfile=f"rankings_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db",
                title="Sauvegarder la base de données"
            )
            
            if backup_filename:
                # Ferme la connexion actuelle
                self.conn.close()
                
                # Copie le fichier de la base de données
                shutil.copy2('rankings.db', backup_filename)
                
                # Réouvre la connexion
                self.conn = sqlite3.connect('rankings.db')
                self.cursor = self.conn.cursor()
                
                messagebox.showinfo(
                    "Succès",
                    f"Base de données sauvegardée vers {backup_filename}"
                )
                
        except Exception as e:
            messagebox.showerror(
                "Erreur de sauvegarde",
                f"Une erreur est survenue lors de la sauvegarde : {str(e)}"
            )
            # Réouvre la connexion en cas d'erreur
            self.conn = sqlite3.connect('rankings.db')
            self.cursor = self.conn.cursor()

    def on_closing(self):
        """Gère la fermeture de l'application."""
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
            self.conn.close()
            self.root.destroy()


def main():
    root = tk.Tk()
    app = RankingApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()