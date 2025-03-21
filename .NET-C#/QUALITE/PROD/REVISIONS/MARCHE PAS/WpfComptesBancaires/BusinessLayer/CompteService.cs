using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BusinessLayer
{
    public class CompteService
    {
        private List<Compte> comptes;

        public CompteService()
        {
            comptes = DataAccess.LoadComptes();
        }

        public void AjouterCompte(int id, double solde)
        {
            if (solde < 0) throw new ArgumentException("Le solde initial ne peut pas être négatif.");
            var compte = new Compte { Id = id, Solde = solde };
            comptes.Add(compte);
            DataAccess.InsertCompte(compte);
            DataAccess.SaveComptes(comptes);
        }

        public void EffectuerVirement(int idDebit, int idCredit, double montant)
        {
            var compteDebit = comptes.Find(c => c.Id == idDebit);
            var compteCredit = comptes.Find(c => c.Id == idCredit);

            if (compteDebit == null || compteCredit == null) throw new Exception("Compte introuvable.");
            if (compteDebit.Solde < montant) throw new InvalidOperationException("Solde insuffisant.");

            compteDebit.Solde -= montant;
            compteCredit.Solde += montant;

            DataAccess.Virement(idDebit, idCredit, montant);
            DataAccess.SaveComptes(comptes);
        }
    }

}
