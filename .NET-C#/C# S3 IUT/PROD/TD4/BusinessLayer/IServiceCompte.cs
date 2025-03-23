using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BusinessLayer
{
    public interface IServiceCompte
    {
        public List<Compte>? GetAllComptes();
        public List<Virement>? GetAllVirement();
        public List<Virement>? GetVirements(int idCompte,DateTime dateTransaction);
        public Compte GetCompte(int id);
        public void SetDebitCredit(Compte compte, double montant);
        public void Virement(Compte compteDebit, Compte compteCredit, double montant);
        public void CreationCompte(int id, Double solde);

    }
}

