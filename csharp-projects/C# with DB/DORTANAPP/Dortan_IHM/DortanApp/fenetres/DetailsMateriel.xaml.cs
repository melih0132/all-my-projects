using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace DortanApp
{
    /// <summary>
    /// Logique d'interaction pour DetailsMateriel.xaml
    /// </summary>
    public partial class DetailsMateriel : Window
    {
        public DetailsMateriel()
        {
            InitializeComponent();
        }

        public void AfficherDetails(DortanApp.Materiel materiel)
        {
            if (materiel != null)
            {
                lbNomCategorie.Content = "Nom de la categorie : " + materiel.NomCategorie.ToString();
                lbSite.Content = "Site : " + materiel.Site.Nom;
                lbType.Content = "Type du materiel : " + materiel.TypeMateriel.Nom;
                lbNom.Content = "Nom du materiel : " + materiel.Nom;
                lbMarque.Content = "Nom de la marque : " + materiel.Marque;
                lbDescription.Content = "Description : " + materiel.Description;
                lbPuissanceCV.Content = "Puissance en CV : " + materiel.PuissanceCV;
                lbPuissanceW.Content = "Puissance en W : " + materiel.PuissanceW;
                lbCoutUtilisation.Content = "Cout de l'utilisation : " + materiel.CoutUtilisation;
            }
        }

        private void btOK_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
        }
    }
}