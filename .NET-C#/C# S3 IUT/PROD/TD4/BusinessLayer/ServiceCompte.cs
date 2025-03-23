using DataLayer;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Data;
using System.Linq;
using System.Numerics;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;

namespace BusinessLayer
{
    public  class ServiceCompte:IServiceCompte
    {
        public DataAccess ObjDataAcces
        {
            get { return DataAccess.Instance; }
        }

      
        private static ServiceCompte _instance;
        static readonly object instanceLock = new object();

        private ServiceCompte()
        {

        }

        public static ServiceCompte Instance
        {
            get
            {
                if (_instance == null) //Les locks prennent du temps, il est préférable de vérifier d'abord la nullité de l'instance.
                {
                    lock (instanceLock)
                    {
                        if (_instance == null) //on vérifie encore, au cas où l'instance aurait été créée entretemps.
                            _instance = new ServiceCompte();
                    }
                }
                return _instance;
            }
        }


        /// <summary>
        /// Récupère la liste de tous les comptes (id et solde) de la base de données
        /// </summary>
        /// <returns>Liste des comptes bancaires</returns>
        public  List<Compte>? GetAllComptes()
        {
            try
            {
                List<Compte> comptes = new List<Compte>();
                DataTable? table = ObjDataAcces.GetData("select * from vComptes");
                foreach (DataRow res in table.Rows)
                {
                    comptes.Add(new Compte(Convert.ToInt32(res["idCompte"]), Convert.ToDouble(res["solde"])));
                }

                return comptes;
            }
            catch (Exception ex)
            {
                throw ex;

            }
        }

        public Compte GetCompte(int id)
        {
            try
            {
                DataTable? table = ObjDataAcces.GetData($"select * from vComptes where idCompte = {id}");
                Compte compte = new Compte();
                foreach (DataRow res in table.Rows)
                {
                    compte.IdCompte = Convert.ToInt32(res["idCompte"]);
                    compte.Solde = Convert.ToDouble(res["solde"]);
                }
                return compte;
            }
            catch (Exception ex)
            {
                throw ex;
            }



        }

        /// <summary>
        /// Met à jour le solde du compte passé en paramètre en fonction du montant passé en paramètre. Si  montant<0 => débit, sinon crédit.
        /// </summary>
        /// <param name="compte">Compte à débiter ou créditer</param>
        /// <param name="montant">Montant du débit (si <0) ou crédit (si >0)</param>
        /// <exception cref="Exception">Retourne une exception Problème provenant de la base</exception>
        public  void SetDebitCredit(Compte compte, double montant)
        {
            try
            {

                compte.Solde -= montant < 0 ? -montant : montant;

                ObjDataAcces.SetData($"UPDATE  vComptes SET SOLDE = {compte.Solde}  where idCompte = {compte.IdCompte}");
            }
            catch (Exception ex)
            {
                throw ex;
            }


        }

        /// <summary>
        /// Réalise un virement du compte en paramètre n°1 vers le compte en paramètre n°2 d'un montant en paramètre n°3
        /// </summary>
        /// <param name="compteDebit">Compte à débiter</param>
        /// <param name="compteCredit">Compte à créditer</param>
        /// <param name="montant">Montant du virement</param>
        /// <exception cref="Exception">Retourne une exception Problème provenant de la base</exception>
        public void Virement(Compte compteDebit, Compte compteCredit, double montant) 
        {
            try
            {
                
                Compte verifCompte = Instance.GetCompte(compteDebit.IdCompte);

                if (verifCompte.Solde - montant < 0 )
                {
                    MessageBox.Show($"Compte {compteDebit.IdCompte } Solde insuffisant ", "Erreur", MessageBoxButton.OK, MessageBoxImage.Error);
                    return;
                }
                ObjDataAcces.VirementBancaire(compteDebit.IdCompte,compteCredit.IdCompte, montant);
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }

        public void CreationCompte(int id, double solde)
        {
            try
            {
                ObjDataAcces.SetData($"insert into vComptes (idCompte, solde) values ({id}, {solde})");
            }
            catch (Exception ex)
            {
                throw ex;

            }
        }

        public List<Virement>? GetAllVirement()
        {
            try
            {
                List<Virement> virements = new List<Virement>();
                DataTable? table = ObjDataAcces.GetData("select * from virement");
                foreach (DataRow res in table.Rows)
                {
                    virements.Add(new Virement(Convert.ToInt32(res["idtransaction"]), Convert.ToInt32(res["idcomptedebit"]), Convert.ToInt32(res["idcomptecredit"]), Convert.ToDateTime(res["datetransaction"]), Convert.ToDouble(res["montant"])));
                }

                return virements;
            }
            catch (Exception ex)
            {
                throw ex;

            }
        }

        public List<Virement>? GetVirements(int idCompte, DateTime dateTransaction)
        {
            try
            {
                List<Virement> virements = new List<Virement>();
                DataTable? table = ObjDataAcces.GetData($"select * from virement where idcomptedebit = {idCompte} and datetransaction = '{dateTransaction.ToShortDateString()}'");
                foreach (DataRow res in table.Rows)
                {
                    virements.Add(new Virement(Convert.ToInt32(res["idtransaction"]), Convert.ToInt32(res["idcomptedebit"]), Convert.ToInt32(res["idcomptecredit"]), Convert.ToDateTime(res["datetransaction"]), Convert.ToDouble(res["montant"])));
                }

                return virements;
            }
            catch (Exception ex)
            {
                throw ex;

            }

        }
    }
}

