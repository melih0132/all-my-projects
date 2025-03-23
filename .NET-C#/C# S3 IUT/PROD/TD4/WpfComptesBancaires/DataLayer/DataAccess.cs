using Npgsql;
using System;
using System.Data;
using System.Reflection;

namespace DataLayer // A MODIFIER SI VOTRE PROJET A UN AUTRE NOM
{
	/// <summary>
    /// Classe de connexion à la base de données
    /// </summary>
    public class DataAccess 
    {
        public NpgsqlConnection? NpgSQLConnect { get; set; }

        /// <summary>
        /// Ouverture de la connexion à la base de données
        /// </summary>
        /// <returns> Retourne un booléen indiquant si la connexion est ouverte ou fermée</returns>
        /// <exception cref="DataBaseException">Exception levée si impossible de se connecter</exception>
        private void OpenConnection()
        {
            try
            {
                // Initialisation de la connexion à la base de données
                NpgSQLConnect = new NpgsqlConnection
                {
                    ConnectionString = "Server=srv-peda.iut-acy.local;" +
                                       "Port=5433;" +
                                       "Database=cetinkam;" +
                                       "Search Path=bd_compte_bancaire;" +
                                       "User ID=cetinkam;" +
                                       "Password=7jhqDh;"
                };

                // Ouverture de la connexion
                NpgSQLConnect.Open();
            }
            catch (Exception ex) // Précision du type d'exception capturée
            {
                string message = "Erreur de base de données : impossible d'ouvrir la connexion.";
#if DEBUG
                MethodBase? currentMethod = MethodBase.GetCurrentMethod();
                string debugInfo = $"Classe : {this.GetType().Name} / Méthode : {currentMethod?.Name}.";
                throw new DataBaseException($"{message} {debugInfo}", ex); // Ajout de l'exception d'origine
#else
        throw new DataBaseException(message, ex); // Toujours inclure l'exception d'origine
#endif
            }
        }

        /// <summary>
        /// Déconnexion de la base de données
        /// </summary>
        private void CloseConnection()
        {
            if (NpgSQLConnect!=null)
                if (NpgSQLConnect.State.Equals(System.Data.ConnectionState.Open))
                {
                    NpgSQLConnect.Close();
                }
        }

        /// <summary>
        /// Accès à des données en lecture
        /// </summary>
        /// <param name="getQuery">Requête SELECT de sélection de données</param>
        /// <returns>Retourne un DataTable contenant les lignes renvoyées par le SELECT</returns>
        /// <exception cref="DataBaseException">Exception levée si impossible de se connecter</exception>
        public DataTable? GetData(string getQuery)
        {
            try
            {
                OpenConnection();
                NpgsqlCommand npgsqlCommand = new NpgsqlCommand(getQuery, NpgSQLConnect);
                NpgsqlDataAdapter npgsqlAdapter = new NpgsqlDataAdapter
                {
                    SelectCommand = npgsqlCommand
                };
                DataTable dataTable = new DataTable();
                npgsqlAdapter.Fill(dataTable);
                CloseConnection();
                if (dataTable.Rows.Count > 0)
                    return dataTable;
                else
                    throw new Exception("La source ne renvoie pas de données.");
            }
            catch (Exception ex)
            {
                CloseConnection();
                string message = "Erreur de base de données. Impossible de récupérer les données.";
#if DEBUG
                MethodBase? m = MethodBase.GetCurrentMethod();
                    throw new DataBaseException(message + " L'erreur provient de la classe " + this.GetType().Name + " / Méthode : " + m!.Name  + ".\n"
                        + ex.Message);
#else
                throw new DataBaseException(message);
#endif
            }
        }

        /// <summary>
        /// Permet d'insérer, supprimer ou modifier des données
        /// </summary>
        /// <param name="setQuery">Requête SQL permettant d'insérer (INSERT), supprimer (DELETE) ou modifier des données (UPDATE)</param>
        /// <returns>Retourne un entier contenant le nombre de lignes ajoutées/supprimées/modifiées</returns>
        /// <exception cref="DataBaseException">Exception levée si impossible de MaJ les données</exception>
        public int SetData(string setQuery)
        {
            try
            {
                OpenConnection();
                NpgsqlCommand sqlCommand = new NpgsqlCommand(setQuery, NpgSQLConnect);
                int modifiedLines = sqlCommand.ExecuteNonQuery();
                CloseConnection();
                return modifiedLines;
            }
            catch (Exception ex)
            {
                CloseConnection();
                string message = "Erreur de base de données. Impossible de mettre à jour les données.";
#if DEBUG
                MethodBase? m = MethodBase.GetCurrentMethod();
                throw new DataBaseException(message + " L'erreur provient de la classe " + this.GetType().Name + " / Méthode : " + m!.Name + ".\n"
                    + ex.Message);
#else
                throw new DataBaseException(message);
#endif
            }
        }

        public int SetDataWithTransaction(NpgsqlTransaction transaction, string setQuery)
        {
            try
            {
                OpenConnection();
                NpgsqlCommand sqlCommand = new NpgsqlCommand(setQuery, NpgSQLConnect)
                {
                    Transaction = transaction
                };
                return sqlCommand.ExecuteNonQuery();
            }
            catch (Exception ex)
            {
                throw new DataBaseException("Erreur lors de l'exécution de la requête dans la transaction.", ex);
            }
        }
    }
}
