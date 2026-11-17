using APIfilms.Models.EntityFramework;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using APIfilms.Models.EntityFramework;
using APIfilms.Models.Repository;

namespace APIfilms.Models.DataManager
{
    public class UtilisateurManager : IDataRepository<Utilisateur>
    {
        private readonly FilmRatingsDBContext filmsDbContext;

        public UtilisateurManager() { }

        public UtilisateurManager(FilmRatingsDBContext context)
        {
            filmsDbContext = context;
        }

        //public ActionResult<IEnumerable<Utilisateur>> GetAll()
        //{
        //    return filmsDbContext.Utilisateurs.ToList();
        //}

        //public ActionResult<Utilisateur> GetById(int id)
        //{
        //    return filmsDbContext.Utilisateurs.FirstOrDefault(u => u.UtilisateurId == id);
        //}

        //public ActionResult<Utilisateur> GetByString(string mail)
        //{
        //    return filmsDbContext.Utilisateurs.FirstOrDefault(u => u.Mail.ToUpper() == mail.ToUpper());
        //}

        //public void Add(Utilisateur entity)
        //{
        //    filmsDbContext.Utilisateurs.Add(entity);
        //    filmsDbContext.SaveChanges();
        //}

        //public void Update(Utilisateur utilisateur, Utilisateur entity)
        //{
        //    filmsDbContext.Entry(utilisateur).State = EntityState.Modified;
        //    utilisateur.UtilisateurId = entity.UtilisateurId;
        //    utilisateur.Nom = entity.Nom;
        //    utilisateur.Prenom = entity.Prenom;
        //    utilisateur.Mail = entity.Mail;
        //    utilisateur.Rue = entity.Rue;
        //    utilisateur.CodePostal = entity.CodePostal;
        //    utilisateur.Ville = entity.Ville;
        //    utilisateur.Pays = entity.Pays;
        //    utilisateur.Latitude = entity.Latitude;
        //    utilisateur.Longitude = entity.Longitude;
        //    utilisateur.Pwd = entity.Pwd;
        //    utilisateur.Mobile = entity.Mobile;
        //    utilisateur.NotesUtilisateur = entity.NotesUtilisateur;
        //    filmsDbContext.SaveChanges();
        //}

        //public void Delete(Utilisateur utilisateur)
        //{
        //    filmsDbContext.Utilisateurs.Remove(utilisateur);
        //    filmsDbContext.SaveChanges();
        //}

        public async Task<ActionResult<IEnumerable<Utilisateur>>> GetAllAsync()
        {
            var utilisateurs = await filmsDbContext.Utilisateurs.ToListAsync();
            return new ActionResult<IEnumerable<Utilisateur>>(utilisateurs);
        }

        public async Task<ActionResult<Utilisateur>> GetByIdAsync(int id)
        {
            var utilisateur = await filmsDbContext.Utilisateurs.FirstOrDefaultAsync(u => u.UtilisateurId == id);
            return new ActionResult<Utilisateur>(utilisateur);
        }

        public async Task<ActionResult<Utilisateur>> GetByStringAsync(string mail)
        {
            var utilisateur = await filmsDbContext.Utilisateurs
                .FirstOrDefaultAsync(u => u.Mail.ToUpper() == mail.ToUpper());
            return new ActionResult<Utilisateur>(utilisateur);
        }

        public async Task AddAsync(Utilisateur entity)
        {
            await filmsDbContext.Utilisateurs.AddAsync(entity);
            await filmsDbContext.SaveChangesAsync();
        }

        public async Task UpdateAsync(Utilisateur utilisateurToUpdate, Utilisateur entity)
        {
            // On ne met pas à jour l’identifiant
            filmsDbContext.Entry(utilisateurToUpdate).State = EntityState.Modified;
            utilisateurToUpdate.Nom = entity.Nom;
            utilisateurToUpdate.Prenom = entity.Prenom;
            utilisateurToUpdate.Mail = entity.Mail;
            utilisateurToUpdate.Rue = entity.Rue;
            utilisateurToUpdate.CodePostal = entity.CodePostal;
            utilisateurToUpdate.Ville = entity.Ville;
            utilisateurToUpdate.Pays = entity.Pays;
            utilisateurToUpdate.Latitude = entity.Latitude;
            utilisateurToUpdate.Longitude = entity.Longitude;
            utilisateurToUpdate.Pwd = entity.Pwd;
            utilisateurToUpdate.Mobile = entity.Mobile;
            utilisateurToUpdate.NotesUtilisateur = entity.NotesUtilisateur;
            await filmsDbContext.SaveChangesAsync();
        }

        public async Task DeleteAsync(Utilisateur entity)
        {
            filmsDbContext.Utilisateurs.Remove(entity);
            await filmsDbContext.SaveChangesAsync();
        }
    }
}
