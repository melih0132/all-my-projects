using Calculatrice;
using System;
using System.Collections.Generic;
using System.ComponentModel;
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
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace WpfCalculatriveV2
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window, INotifyPropertyChanged
    {
        public event PropertyChangedEventHandler? PropertyChanged;

        public MainWindow()
        {
            InitializeComponent();
            this.DataContext = this;
        }

        public double Nb1 { get; set; }

        public double Nb2 { get; set; }

        private Double resultat;

        public Double Resultat
        {
            get { return resultat; }
            set
            {
                resultat = value;
                OnPropertyChanged(nameof(Resultat));
            }
        }

        public ICalcul? ObjCalcul {
            get { return Calcul.Instance; }
        }

        public ICalculAvance? ObjCalculAvance
        {
            get { return CalculAvance.Instance; }
        }

        private void ButtonAddition_Click(object sender, RoutedEventArgs e)
        {
            Resultat = ObjCalcul!.Addition(Nb1, Nb2);
        }

        private void ButtonSoustraction_Click(object sender, RoutedEventArgs e)
        {
            Resultat = ObjCalcul!.Soustraction(Nb1, Nb2);
        }

        private void ButtonMultiplication_Click(object sender, RoutedEventArgs e)
        {
            Resultat = ObjCalcul!.Multiplication(Nb1, Nb2);
        }

        private void ButtonDivision_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                Resultat = ObjCalcul!.Division(Nb1, Nb2);
            }
            catch (Exception ex)
            {
                MessageBox.Show(this, ex.Message, "Erreur", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        protected void OnPropertyChanged(string name)
        {
            PropertyChangedEventHandler? handler = PropertyChanged;
            if (handler != null)
            {
                handler(this, new PropertyChangedEventArgs(name));
            }
        }

        private void ButtonFactorielle_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                Resultat = (double)ObjCalcul!.Factorielle(Nb1);
            }
            catch (Exception ex)
            {
                MessageBox.Show(this, ex.Message, "Erreur", MessageBoxButton.OK,MessageBoxImage.Error);
            }
        }

        private void ButtonMoyenne_Click(object sender, RoutedEventArgs e)
        {
            Resultat = ObjCalculAvance!.Moyenne(ObjCalcul!, Nb1, Nb2);
        }
    }
}
