using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using FilmRatingsApp.Models;

namespace FilmRatingsApp.Services;
public interface IService
{
    // Méthodes pour Utilisateur
    Task<Utilisateur> GetUtilisateurByEmailAsync(string email);
    Task<List<Utilisateur>> GetUtilisateursAsync();
    Task<bool> AddUtilisateurAsync(Utilisateur utilisateur);
    Task<bool> UpdateUtilisateurAsync(Utilisateur utilisateur);
    Task<bool> DeleteUtilisateurAsync(int id);

    // Méthodes pour Film (à développer dans la suite du TP)
    Task<List<Film>> GetFilmsAsync();
    Task<Film> GetFilmByIdAsync(int id);

    // Méthodes pour Notation (à développer dans la suite du TP)
    Task<List<Notation>> GetNotationsByUtilisateurAsync(int utilisateurId);
}
