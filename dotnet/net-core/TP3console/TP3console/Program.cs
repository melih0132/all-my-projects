using Microsoft.EntityFrameworkCore;
using TP3console.Models.EntityFramework;

namespace TP3Console
{
    internal class Program
    {
        static void Main(string[] args)
        {
            // Exemples d'appels :
            Exo2Q2();
            Exo2Q7();
            Console.ReadKey();
        }

        // Exercice 2.2 : Afficher les emails des utilisateurs
        public static void Exo2Q2()
        {
            using (var ctx = new FilmsDbContext())
            {
                foreach (var user in ctx.Utilisateurs)
                {
                    Console.WriteLine(user.Email);
                }
            }
        }

        // Exercice 2.7 : Films commençant par "Le" (insensible à la casse)
        public static void Exo2Q7()
        {
            using (var ctx = new FilmsDbContext())
            {
                var films = ctx.Films
                    .Where(f => EF.Functions.ILike(f.Nom, "Le%"))
                    .ToList();

                foreach (var film in films)
                {
                    Console.WriteLine(film.Nom);
                }
            }
        }

        // Ajout d'un utilisateur
        public static void AjouterUtilisateur()
        {
            using (var ctx = new FilmsDbContext())
            {
                var nouvelUtilisateur = new Utilisateur
                {
                    Login = "john_doe",
                    Pwd = "secret",
                    Email = "john.doe@example.com"
                };

                ctx.Utilisateurs.Add(nouvelUtilisateur);
                ctx.SaveChanges();
            }
        }

        // Modification d'un film
        public static void ModifierFilm()
        {
            using (var ctx = new FilmsDbContext())
            {
                var film = ctx.Films.First(f => f.Nom == "L'armee des douze singes");
                film.Description = "Un film de science-fiction post-apocalyptique.";
                film.Idcategorie = ctx.Categories.First(c => c.Nom == "Drame").Idcategorie;
                ctx.SaveChanges();
            }
        }

        // Suppression d'un film (avec ses avis)
        public static void SupprimerFilm()
        {
            using (var ctx = new FilmsDbContext())
            {
                var filmASupprimer = ctx.Films
                    .Include(f => f.Avis)
                    .First(f => f.Nom == "L'armee des douze singes");

                ctx.Avis.RemoveRange(filmASupprimer.Avis);
                ctx.Films.Remove(filmASupprimer);
                ctx.SaveChanges();
            }
        }
    }
}