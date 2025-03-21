using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BusinessLayer
{

    public class Compte
    {

        private int idCompte;

		public int IdCompte
		{
			get { return idCompte; }
			set { idCompte = value; }
		}

        private double solde;

        public double Solde
        {
            get { return solde; }
            set { solde = value; }
        }

        public Compte(int idCompte, double solde)
        {
            this.IdCompte = idCompte;
            this.Solde = solde;
        }

        public Compte() 
        {
        }

        public override string? ToString()
        {
            return this.IdCompte.ToString();
        }
    }
}
