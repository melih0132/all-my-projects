using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Collections.ObjectModel;
using System.Data;
using Npgsql;

namespace wpf_revisions_bindings
{
    public class ViewModel : INotifyPropertyChanged
    {
        private const string ConnectionString = "Host=localhost;Username=postgres;Password=postgres;Database=revision_wpf";

        private string _userName;
        public string UserName
        {
            get => _userName;
            set
            {
                _userName = value;
                OnPropertyChanged(nameof(UserName));
            }
        }

        // IMPORTANT : ObservableCollection
        public ObservableCollection<string> Users { get; set; } = new ObservableCollection<string>();

        // IMPORTANT : PropertyChangedEventHandler
        public event PropertyChangedEventHandler PropertyChanged;

        protected void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        public void LoadUsers()
        {
            Users.Clear();

            using var connection = new NpgsqlConnection(ConnectionString);
            connection.Open();

            using var command = new NpgsqlCommand("SELECT UserName FROM Users", connection);
            using var reader = command.ExecuteReader();

            while (reader.Read())
            {
                Users.Add(reader.GetString(0));
            }
        }

        public void SaveUser()
        {
            using var connection = new NpgsqlConnection(ConnectionString);
            connection.Open();

            using var command = new NpgsqlCommand("INSERT INTO Users (UserName) VALUES (@name)", connection);
            command.Parameters.AddWithValue("name", UserName);
            command.ExecuteNonQuery();

            LoadUsers(); // Rafraîchir la liste des utilisateurs
        }
    }
}
