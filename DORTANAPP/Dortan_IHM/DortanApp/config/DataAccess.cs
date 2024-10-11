using Npgsql;
using System.Data;
using System.Windows;

namespace DortanApp.config
{
    public class DataAccess
    {
        private static DataAccess instance;
        private static string strConnexion;

        private DataAccess()
        {
        }

        public static DataAccess Instance
        {
            get
            {
                if (instance == null)
                {
                    instance = new DataAccess();
                }

                return instance;
            }
        }

        public NpgsqlConnection? Connexion
        {
            get;
            set;
        }

        public void ConnexionBD(string id, string mdp)
        {
            string strConnexion = $"Host=localhost;" +
                                  $"Port=5432;" +
                                  $"Database=dortan;" +
                                  $"Username={id};" +
                                  $"Password={mdp};";

            try
            {
                Connexion = new NpgsqlConnection();
                Connexion.ConnectionString = strConnexion;
                Connexion.Open();
            }
            catch (Exception)
            {
                MessageBox.Show("ERROR : Impossinble de se connecter", "", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        public void DeconnexionBD()
        {
            try
            {
                Connexion.Close();
            }
            catch (Exception)
            {
                MessageBox.Show("ERROR : Impossible de se déconnecter", "", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        public DataTable GetData(string selectSQL)
        {
            try
            {
                NpgsqlDataAdapter dataAdapter = new NpgsqlDataAdapter(selectSQL, Connexion);
                DataTable dataTable = new DataTable();
                dataAdapter.Fill(dataTable);
                return dataTable;
            }
            catch (Exception e)
            {
                Console.WriteLine("pb avec : " + selectSQL + e.ToString());
                return null;
            }
        }

        public int SetData(string setSQL)
        {

            try
            {
                NpgsqlCommand sqlCommand = new NpgsqlCommand(setSQL, Connexion);
                int nbLines = sqlCommand.ExecuteNonQuery();
                return nbLines;
            }
            catch (Exception e)
            {
                Console.WriteLine("pb avec : " + setSQL + e.ToString());
                return 0;
            }
        }
    }
}