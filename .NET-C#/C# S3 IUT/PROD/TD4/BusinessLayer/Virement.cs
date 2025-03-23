using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BusinessLayer
{
    public class Virement
    {
        private int idTransacation;
        private int  idCompteDebit;
        private int idCompteCredit;
        private DateTime dateTransacation;
        private double montant;

        public Virement(int idTransacation, int idCompteDebit, int idCompteCredit, DateTime dateTransacation, double montant)
        {
            this.IdTransacation = idTransacation;
            this.IdCompteDebit = idCompteDebit;
            this.IdCompteCredit = idCompteCredit;
            this.DateTransacation = dateTransacation;
            this.Montant = montant;
        }

        public int IdTransacation
        {
            get
            {
                return this.idTransacation;
            }

            set
            {
                this.idTransacation = value;
            }
        }

        public int IdCompteDebit
        {
            get
            {
                return this.idCompteDebit;
            }

            set
            {
                this.idCompteDebit = value;
            }
        }

        public int IdCompteCredit
        {
            get
            {
                return this.idCompteCredit;
            }

            set
            {
                this.idCompteCredit = value;
            }
        }

        public DateTime DateTransacation
        {
            get
            {
                return this.dateTransacation;
            }

            set
            {
                this.dateTransacation = value;
            }
        }

        public double Montant
        {
            get
            {
                return this.montant;
            }

            set
            {
                this.montant = value;
            }
        }

        public override bool Equals(object? obj)
        {
            return obj is Virement virement &&
                   this.IdTransacation == virement.IdTransacation &&
                   this.IdCompteDebit == virement.IdCompteDebit &&
                   this.IdCompteCredit == virement.IdCompteCredit &&
                   this.DateTransacation == virement.DateTransacation &&
                   this.Montant == virement.Montant;
        }

        public override int GetHashCode()
        {
            return HashCode.Combine(this.IdTransacation, this.IdCompteDebit, this.IdCompteCredit, this.DateTransacation, this.Montant);
        }
    }
}
