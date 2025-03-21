using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BusinessLayer
{
    public class Compte
    {
        private int idCompte;
        private double solde;

        public Compte()
        {
        }

        public Compte(int idCompte, double solde)
        {
            this.IdCompte = idCompte;
            this.Solde = solde;
        }

        public int IdCompte
        {
            get
            {
                return this.idCompte;
            }

            set
            {
                this.idCompte = value;
            }
        }

        public double Solde
        {
            get
            {
                return this.solde;
            }

            set
            {
                this.solde = value;
            }
        }

        public override bool Equals(object? obj)
        {
            return obj is Compte compte &&
                   this.IdCompte == compte.IdCompte &&
                   this.Solde == compte.Solde;
        }

        public override int GetHashCode()
        {
            return HashCode.Combine(this.IdCompte, this.Solde);
        }
    }
}
