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
using WpfVirementMVVM.ViewsModels;

namespace WpfVirementMVVM.Views
{
    /// <summary>
    /// Logique d'interaction pour VirementView.xaml
    /// </summary>
    public partial class VirementView : Window
    {
        public VirementView()
        {
            InitializeComponent();
            DataContext = App.Current.Services.GetService<VirementVM>();
        }
    }
}
