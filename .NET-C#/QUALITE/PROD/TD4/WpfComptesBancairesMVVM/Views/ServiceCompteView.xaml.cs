using Microsoft.Extensions.DependencyInjection;
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
using WpfComptesBancairesMVVM.ViewsModels;

namespace WpfComptesBancairesMVVM.Views
{
    /// <summary>
    /// Logique d'interaction pour ServiceCompteView.xaml
    /// </summary>
    public partial class ServiceCompteView : Window
    {
        public ServiceCompteView()
        {
            InitializeComponent();
            DataContext = App.Current.Services.GetService<ServiceCompteVM>();
        }
    }
}
