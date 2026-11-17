using ClientConvertisseurV2.Services;
using ClientConvertisseurV2.ViewModels;
using ClientConvertisseurV2.Views;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using System;
using Windows.ApplicationModel.Activation;

// To learn more about WinUI, the WinUI project structure,
// and more about our project templates, see: http://aka.ms/winui-project-info.

namespace ClientConvertisseurV2
{
    /// <summary>
    /// Provides application-specific behavior to supplement the default Application class.
    /// </summary>
    public partial class App : Application
    {
        public static FrameworkElement MainRoot { get; private set; }
        private Window m_window;

        public ServiceProvider Services { get; private set; }

        /// <summary>
        /// Initializes the singleton application object.  This is the first line of authored code
        /// executed, and as such is the logical equivalent of main() or WinMain().
        /// </summary>
        public App()
        {
            this.InitializeComponent();
            ConfigureServices();
        }

        private void ConfigureServices()
        {
            // Créez une collection de services
            var services = new ServiceCollection();

            // Enregistrez les services nécessaires
            services.AddTransient<ConvertisseurEuroViewModel>();
            services.AddSingleton<IService, WSService>(_ => new WSService("https://localhost:7078/api/"));

            // Construisez le fournisseur de services
            Services = services.BuildServiceProvider();
        }

        public new static App Current => (App)Application.Current;

        /// <summary>
        /// Invoked when the application is launched.
        /// </summary>
        /// <param name="args">Details about the launch request and process.</param>
        protected override void OnLaunched(Microsoft.UI.Xaml.LaunchActivatedEventArgs args)
        {
            m_window = new MainWindow();
            MainRoot = m_window.Content as FrameworkElement;

            var rootFrame = new Frame();
            m_window.Content = rootFrame;
            rootFrame.Navigate(typeof(ConvertisseurEuroPage));

            m_window.Activate();
        }
    }
}
