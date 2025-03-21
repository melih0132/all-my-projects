using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using TD3;

namespace TD3
{
    public static class Service
    {
        private static readonly string filePath = "./Data/Devises.json";

        public static List<Devise> ChargerDevises()
        {
            try
            {
                if (!File.Exists(filePath))
                    return new List<Devise>();

                string json = File.ReadAllText(filePath);
                return JsonSerializer.Deserialize<List<Devise>>(json) ?? new List<Devise>();
            }
            catch (JsonException ex)
            {
                throw new IOException("Erreur lors de la désérialisation des devises.", ex);
            }
            catch (IOException ex)
            {
                throw new IOException("Erreur lors de la lecture du fichier des devises.", ex);
            }
        }

        public static void SauvegarderDevises(List<Devise> devises)
        {
            try
            {
                if (devises == null)
                    throw new ArgumentNullException(nameof(devises), "La liste des devises ne peut pas être null.");

                string directory = Path.GetDirectoryName(filePath);
                if (!string.IsNullOrEmpty(directory))
                {
                    Directory.CreateDirectory(directory);
                }

                string json = JsonSerializer.Serialize(devises, new JsonSerializerOptions { WriteIndented = true });
                File.WriteAllText(filePath, json);
            }
            catch (IOException ex)
            {
                throw new IOException("Erreur lors de l'écriture du fichier des devises.", ex);
            }
            catch (Exception ex)
            {
                throw new Exception("Erreur inattendue lors de la sauvegarde des devises.", ex);
            }
        }
    }
}
