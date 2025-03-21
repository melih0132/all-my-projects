using Calculatrice;
using System;
using System.Windows;
using System.Windows.Controls;

namespace WpfCalculatrice
{
    /// <summary>
    /// main window qui gère tout
    /// </summary>
    public partial class MainWindow : Window
    {
        private Calculatrice vm;

        public MainWindow()
        {
            InitializeComponent();
            vm = new Calculatrice();
            DataContext = vm;
        }

        /// <summary>
        /// btn_add_click
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Addition_Click(object sender, RoutedEventArgs e)
        {
            //calc.Resultat = calc.Addition(calc.PremierNB, calc.SecondNB);

            vm.Resultat = Calcul.Addition(vm.PremierNB, vm.SecondNB);
        }

        /// <summary>
        /// btn_supp_click
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Soustraction_Click(object sender, RoutedEventArgs e)
        {
            //calc.Resultat = calc.Soustraction(calc.PremierNB, calc.SecondNB);

            vm.Resultat = Calcul.Soustraction(vm.PremierNB, vm.SecondNB);
        }

        /// <summary>
        /// btn_mult_click
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Multiplication_Click(object sender, RoutedEventArgs e)
        {
            //calc.Resultat = calc.Multiplication(calc.PremierNB, calc.SecondNB);

            vm.Resultat = Calcul.Multiplication(vm.PremierNB, vm.SecondNB);
        }

        /// <summary>
        /// btn_div_click
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Division_Click(object sender, RoutedEventArgs e)
        {
            //try
            //{
            //    calc.Resultat = calc.Division(calc.PremierNB, calc.SecondNB);
            //}
            //catch (DivideByZeroException ex)
            //{
            //    MessageBox.Show(ex.Message);
            //}

            try
            {
                vm.Resultat = Calcul.Division(vm.PremierNB, vm.SecondNB);
            }
            catch (DivideByZeroException ex)
            {
                MessageBox.Show(ex.Message, "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        /// <summary>
        /// bouton qui factorie la sender object aka NB1 + messbox si erreur
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Factorielle_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                vm.Resultat = Calcul.Factorielle(vm.PremierNB);
            }
            catch (ArgumentException ex)
            {
                MessageBox.Show(ex.Message, "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
    }
}