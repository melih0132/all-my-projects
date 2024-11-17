using System;
using System.Windows;

namespace DortanApp
{
    public class Reservation
    {
        private int id;
        private Activite activite;
        private DateTime dateReservation;
        private int dureeReservation;
        private List<Materiel> lesMateriels;

        public Reservation()
        {
        }

        public Reservation(Activite activite, DateTime dateReservation, int dureeReservation)
        {
            this.Activite = activite;
            this.DateReservation = dateReservation;
            this.DureeReservation = dureeReservation;
            this.LesMateriels = new List<Materiel>();
        }

        public Reservation(int id, Activite activite, DateTime dateReservation, int dureeReservation) : this(activite, dateReservation, dureeReservation)
        {
            this.Id = id;
        }

        public int Id
        {
            get
            {
                return id;
            }

            set
            {
                id = value;
            }
        }

        public Activite Activite
        {
            get
            {
                return activite;
            }

            set
            {
                activite = value;
            }
        }

        public DateTime DateReservation
        {
            get
            {
                return dateReservation;
            }

            set
            {
                if (value.Date < DateTime.Today)
                    throw new ArgumentOutOfRangeException("La date de réservation ne peut être déjà passée");

                dateReservation = value;
            }
        }

        public int DureeReservation
        {
            get
            {
                return this.dureeReservation;
            }

            set
            {
                if (value <= 0)
                {
                    throw new ArgumentException("la durée ne doit pas être nulle ou négative");
                }
                dureeReservation = value;
            }
        }

        public List<Materiel> LesMateriels
        {
            get
            {
                return this.lesMateriels;
            }

            set
            {
                this.lesMateriels = value;
            }
        }

        public void AjouterMateriel(Materiel materiel)
        {
            if (materiel != null)
            {
                LesMateriels.Add(materiel);
                MessageBox.Show("Le materiel a été ajouté");
            }
        }
    }
}