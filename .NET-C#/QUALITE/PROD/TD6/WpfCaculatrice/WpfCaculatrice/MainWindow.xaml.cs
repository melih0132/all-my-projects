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

namespace WpfCaculatrice
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

        private void ButtonAddition_Click(object sender, RoutedEventArgs e)
        {
            Resultat = Nb1 + Nb2;
        }

        private void ButtonSoustraction_Click(object sender, RoutedEventArgs e)
        {
            Resultat = Nb1 - Nb2;
        }

        private void ButtonMultiplication_Click(object sender, RoutedEventArgs e)
        {
            Resultat = Nb1 * Nb2;
        }

        private void ButtonDivision_Click(object sender, RoutedEventArgs e)
        {
            Resultat = Nb1 / Nb2;
        }

        protected void OnPropertyChanged(string name)
        {
            PropertyChangedEventHandler? handler = PropertyChanged;
            if (handler != null)
            {
                handler(this, new PropertyChangedEventArgs(name));
            }
        }
    }
}
