using System;
using System.Diagnostics;
using System.Windows;
using Dortan;
using DortanApp.config;

namespace DortanApp
{
    /// <summary>
    /// Logique d'interaction pour MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        ApplicationData data;
        bool connecte;
        Reservation nouvReservation;

        public MainWindow()
        {
            InitializeComponent();

            Connexion connexion = new Connexion();
            connexion.ShowDialog();
            if (connexion.DialogResult == true)
            {
                data = new ApplicationData();
                connecte = true;
                DataContext = data;
                tiReserver.Content = new UCReservation();
                tiCreer.Content = new UCCreation();
                tiVisuReservation.Content = new UCVisuReserver();
                tiMateriel.Content = new UCMateriel();
            }
            else
            {
                Application.Current.Shutdown();
            }
        }

        public void CreationActivite(string nom)
        {
            if (nom != null)
            {
                Activite nouvActivite = new Activite(nom);

                if (nouvActivite != null)
                {
                    data.LesActivites.Add(nouvActivite);
                    data.CreateActivite(nouvActivite);

                    MessageBox.Show("L'activité a été enregistré");
                }
            }
        }

        public void CreationReservation(Reservation reservation)
        {
            if (reservation != null)
            {
                nouvReservation = reservation;

                if (nouvReservation != null)
                {
                    data.LesReservations.Add(nouvReservation);
                    data.CreateReservation(nouvReservation);
                }
            }
        }

        public void SupActivite(Activite activite)
        {
            if (activite != null)
            {
                data.LesActivites.Remove(activite);
                data.DeleteActivite(activite);
            }
        }

        public void SupReservation(Reservation reservation)
        {
            if (reservation != null)
            {
                data.LesReservations.Remove(reservation);
                data.DeleteReservation(reservation);
            }
        }

        public void AjouterMaterielReservation(Materiel materiel)
        {
            if (materiel != null)
            {
                nouvReservation.AjouterMateriel(materiel);
            }
        }

        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if (connecte)
            {
                DataAccess.Instance.DeconnexionBD();
            }
        }
    }
}