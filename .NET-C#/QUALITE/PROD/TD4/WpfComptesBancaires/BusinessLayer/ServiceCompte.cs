using System;
using DataLayer;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data;

namespace BusinessLayer
{
    public class ServiceCompte
    {
        static readonly DataAccess dataAccess = new DataAccess();
        /// <summary>
        /// Récupère la liste de tous les comptes (id et solde) de la base de données
        /// </summary>
        /// <returns>Liste des comptes bancaires</returns>
        public List<Compte>? GetAllComptes()
        {
            List<Compte> comptes = new List<Compte>();

            try
            {
                DataTable dt = dataAccess.GetData("select * from bd_compte_bancaire.compte");

                if (dt == null || dt.Rows.Count == 0)
                {
                    throw new Exception("Aucun compte trouvé dans la base de données.");
                }

                foreach (DataRow row in dt.Rows)
                {
                    try
                    {
                        Compte compte = new Compte();

                        if (row["idcompte"] == DBNull.Value || row["solde"] == DBNull.Value)
                        {
                            throw new Exception("Données manquantes pour un compte.");
                        }

                        compte.IdCompte = Convert.ToInt32(row["idcompte"]);
                        compte.Solde = Convert.ToDouble(row["solde"]);

                        comptes.Add(compte);
                    }
                    catch (Exception innerEx)
                    {
                        throw new Exception("Erreur lors de la création du compte à partir de la ligne de la DataTable.", innerEx);
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Erreur lors de l'accès aux comptes dans la base de données.", ex);
            }

            return comptes;
        }

        /// <summary>
        /// Met à jour le solde du compte passé en paramètre en fonction du montant passé en paramètre. Si montant<0 => débit, sinon crédit.
        /// </summary>
        /// <param name="compte">Compte à débiter ou créditer</param>
        /// <param name="montant">Montant du débit (si <0) ou crédit (si >0)</param>
        /// <exception cref="Exception">Retourne une exception Problème provenant de la base</exception>
        public void SetDebitCredit(int idCompte, double montant)
        {
            try
            {
                int modif = dataAccess.SetData($"update bd_compte_bancaire.compte set solde = solde + {montant} where idcompte = {idCompte}");
            }
            catch (Exception ex)
            {
                throw new Exception("Erreur lors de l'update sur la base.", ex);
            }
        }

        public void Virement(int idCompte1, int idCompte2, double montant)
        {
            // Ouvrir une transaction
            using (var transaction = dataAccess.NpgSQLConnect.BeginTransaction())
            {
                try
                {
                    // Débiter le premier compte
                    string debitQuery = $"UPDATE bd_compte_bancaire.compte SET solde = solde - {montant} WHERE idcompte = {idCompte1}";
                    int debitResult = dataAccess.SetDataWithTransaction(transaction, debitQuery);

                    // Vérifier si le débit a réussi (au moins une ligne modifiée)
                    if (debitResult == 0)
                    {
                        throw new Exception("Erreur de débit du premier compte.");
                    }

                    // Crédite le second compte
                    string creditQuery = $"UPDATE bd_compte_bancaire.compte SET solde = solde + {montant} WHERE idcompte = {idCompte2}";
                    int creditResult = dataAccess.SetDataWithTransaction(transaction, creditQuery);

                    // Vérifier si le crédit a réussi (au moins une ligne modifiée)
                    if (creditResult == 0)
                    {
                        throw new Exception("Erreur de crédit du second compte.");
                    }

                    // Insérer l'enregistrement de la transaction dans la table des virements
                    string insertQuery = $"INSERT INTO bd_compte_bancaire.virement (idcomptedebit, idcomptecredit, datetransaction, montant) " +
                                         $"VALUES ({idCompte1}, {idCompte2}, CURRENT_DATE, {montant})";
                    int insertResult = dataAccess.SetDataWithTransaction(transaction, insertQuery);

                    // Vérifier si l'insertion a réussi
                    if (insertResult == 0)
                    {
                        throw new Exception("Erreur lors de l'insertion de la transaction.");
                    }

                    // Si tout est réussi, valider la transaction
                    transaction.Commit();
                }
                catch (Exception ex)
                {
                    // En cas d'erreur, annuler la transaction
                    transaction.Rollback();
                    throw new Exception("Erreur lors du virement. La transaction a été annulée.", ex);
                }
            }
        }
    }
}
