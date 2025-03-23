using BusinessLayer;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Configuration;
using System.Data;
using System.Windows;
using WpfComptesBancairesMVVM.ViewsModels;

namespace WpfComptesBancairesMVVM
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        public ServiceProvider Services { get; }
        public App()
        {
            ServiceCollection services = new ServiceCollection();
            services.AddSingleton<IServiceCompte, ServiceCompte>();

            services.AddTransient<ServiceCompteVM>();

            Services = services.BuildServiceProvider();
        }
        public new static App Current => (App)Application.Current;
    }

}
