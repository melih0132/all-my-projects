using DortanApp.config;
using Npgsql;
using System.Collections.ObjectModel;
using System.Data;
using System.Windows;

namespace DortanApp
{
    public class ApplicationData
    {
        private static ApplicationData instance;

        private ObservableCollection<Materiel> lesMateriels;
        private ObservableCollection<Activite> lesActivites;
        private ObservableCollection<Reservation> lesReservations;

        //private NpgsqlConnection connexion;

        //public static ApplicationData Instance
        //{
        //    get
        //    {
        //        if (instance == null)
        //        {
        //            instance = new ApplicationData();
        //        }

        //        return instance;
        //    }
        //}

        public ObservableCollection<Materiel> LesMateriels
        {
            get
            {
                return lesMateriels;
            }

            set
            {
                lesMateriels = value;
            }
        }

        public ObservableCollection<Activite> LesActivites
        {
            get
            {
                return lesActivites;
            }

            set
            {
                lesActivites = value;
            }
        }

        //public NpgsqlConnection Connexion
        //{
        //    get
        //    {
        //        return connexion;
        //    }

        //    set
        //    {
        //        connexion = value;

        //    }
        //}

        public ObservableCollection<Reservation> LesReservations
        {
            get
            {
                return lesReservations;
            }

            set
            {
                lesReservations = value;
            }
        }

        public ApplicationData()
        {
            this.LesMateriels = new ObservableCollection<Materiel>();
            this.LesActivites = new ObservableCollection<Activite>();
            this.LesReservations = new ObservableCollection<Reservation>();

            ReadMateriels();
            ReadActivite();
            ReadReservations();
            GetMaxActiviteId();
        }

        private DataTable ExecuteQuery(string sql)
        {
            try
            {
                return DataAccess.Instance.GetData(sql);
            }
            catch (NpgsqlException e)
            {
                MessageBox.Show("Problème de requête : " + e.Message, "ERROR", MessageBoxButton.OK, MessageBoxImage.Error);
                return new DataTable();
            }
        }

        private int ReadReservations()
        {
            String sql = "SELECT num_reservation, num_activite, nom_activite, date_reservation, duree_reservation FROM reservation";
            try
            {
                DataTable dataTable = ExecuteQuery(sql);
                foreach (DataRow res in dataTable.Rows)
                {
                    int numReservation = Convert.ToInt32(res["num_reservation"]);
                    int numActivite = Convert.ToInt32(res["num_activite"]);
                    string nomActivite = res["nom_activite"].ToString();
                    DateTime date = Convert.ToDateTime(res["date_reservation"]);
                    int duree = Convert.ToInt32(res["duree_reservation"]);

                    Reservation nouveau = new Reservation(numReservation, new Activite(numActivite, nomActivite), date, duree); ;

                    LesReservations.Add(nouveau);
                }

                return dataTable.Rows.Count;
            }
            catch (NpgsqlException e)
            {
                Console.WriteLine("Problème de requête : " + e.Message);
                return 0;
            }
        }

        public int ReadMateriels()
        {
            String sql = "SELECT num_materiel, nom_categorie, num_site, nom_site, num_type, nom_type, nom_materiel, lien_photo, marque, description, puissance_cv, puissance_w, cout_utilisation FROM materiel";
            try
            {
                DataTable dataTable = ExecuteQuery(sql);
                foreach (DataRow res in dataTable.Rows)
                {
                    int numMateriel = Convert.ToInt32(res["num_materiel"]);
                    string nomCategorie = res["nom_categorie"].ToString();
                    int numSite = Convert.ToInt32(res["num_site"]);
                    string nomSite = res["nom_site"].ToString();
                    int numType = Convert.ToInt32(res["num_type"]);
                    string nomType = res["nom_type"].ToString();
                    string nomMateriel = res["nom_materiel"].ToString();
                    string lienPhoto = res["lien_photo"].ToString();
                    MarqueEnum marque = (MarqueEnum)Enum.Parse(typeof(MarqueEnum), res["marque"].ToString());
                    string description = res["description"].ToString();
                    int puissanceCv = Convert.ToInt32(res["puissance_cv"]);
                    int puissanceW = Convert.ToInt32(res["puissance_w"]);
                    int coutUtilisation = Convert.ToInt32(res["cout_utilisation"]);

                    Materiel nouveau = new Materiel(numMateriel, new Categorie(nomCategorie), new Site(numSite, nomSite), new TypeMateriel(numType, nomType), nomMateriel, lienPhoto, marque, description, puissanceCv, puissanceW, coutUtilisation);

                    LesMateriels.Add(nouveau);
                }

                return dataTable.Rows.Count;
            }
            catch (NpgsqlException e)
            {
                Console.WriteLine("Problème de requête : " + e.Message);
                return 0;
            }
        }

        public int ReadActivite()
        {
            String sql = "SELECT num_activite, nom_activite FROM activite";
            try
            {
                DataTable dataTable = ExecuteQuery(sql);
                foreach (DataRow res in dataTable.Rows)
                {
                    Activite nouveau = new Activite(int.Parse(res["num_activite"].ToString()),
                    res["nom_activite"].ToString());

                    LesActivites.Add(nouveau);
                }
                return dataTable.Rows.Count;

            }
            catch (NpgsqlException e)
            {
                Console.WriteLine("Problème de requête : " + e);
                return 0;
            }
        }

        private int GetMaxActiviteId()
        {
            string sql = "SELECT MAX(num_activite) as nb_max_id FROM activite";
            DataTable dataTable = ExecuteQuery(sql);

            int maxId = 0;

            if (dataTable.Rows.Count > 0 && dataTable.Rows[0]["nb_max_id"] != DBNull.Value)
            {
                maxId = Convert.ToInt32(dataTable.Rows[0]["nb_max_id"]);
            }

            return maxId;
        }

        private int ExecuteNonQuery(string sql)
        {
            try
            {
                return DataAccess.Instance.SetData(sql);
            }
            catch (NpgsqlException e)
            {
                MessageBox.Show("Problème de requête : " + e.Message, "ERROR", MessageBoxButton.OK, MessageBoxImage.Error);
                return 0;
            }
        }

        public int CreateActivite(Activite a)
        {
            int newId = GetMaxActiviteId() + 1;
            string sql = $"INSERT INTO activite (num_activite, nom_activite) VALUES ({newId}, '{a.Nom}')";
            return ExecuteNonQuery(sql);
        }

        //public int UpdateActivite(Activite a)
        //{
        //    string sql = $"UPDATE activite SET nom_activite = '{a.Nom}' WHERE num_activite = {a.Id}";
        //    return ExecuteNonQuery(sql);
        //}

        public int DeleteActivite(Activite a)
        {
            string sql = $"DELETE FROM activite WHERE num_activite = {a.Id}";
            return ExecuteNonQuery(sql);
        }

        private int GetMaxReservationId()
        {
            string sql = "SELECT MAX(num_reservation) as max_reservation_id FROM reservation";
            DataTable dataTable = ExecuteQuery(sql);

            int maxId = 0;

            if (dataTable.Rows.Count > 0 && dataTable.Rows[0]["max_reservation_id"] != DBNull.Value)
            {
                maxId = Convert.ToInt32(dataTable.Rows[0]["max_reservation_id"]);
            }

            return maxId;
        }

        public int CreateReservation(Reservation r)
        {
            int newId = GetMaxReservationId() + 1;
            string sql = $"INSERT INTO reservation (num_reservation, num_activite, nom_activite, date_reservation, duree_reservation) " +
                         $"VALUES ({newId}, {r.Activite.Id}, '{r.Activite.Nom}', '{r.DateReservation:yyyy-MM-dd}', {r.DureeReservation})";
            return ExecuteNonQuery(sql);
        }

        //public int UpdateReservation(Reservation r)
        //{
        //    string sql = $"UPDATE reservation SET num_activite = {r.Activite.Id}, nom_activite = '{r.Activite.Nom}', " +
        //                 $"date_reservation = '{r.DateReservation:yyyy-MM-dd}', duree_reservation = {r.DureeReservation} " +
        //                 $"WHERE num_reservation = {r.Id}";
        //    return ExecuteNonQuery(sql);
        //}

        public int DeleteReservation(Reservation r)
        {
            string sql = $"DELETE FROM reservation WHERE num_reservation = {r.Id}";
            return ExecuteNonQuery(sql);
        }
    }
}