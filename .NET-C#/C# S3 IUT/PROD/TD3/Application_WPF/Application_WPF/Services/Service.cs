using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Text;
using System.Threading.Tasks;

namespace Application_WPF.Services
{
    public static class Service
    {
        public static List<GEstionDevises> LoadDevises()
        {
            string jsonFilePath = "Data/Devises.json"; 

            try
            {
                if (File.Exists(jsonFilePath))
                {
                    string jsonString = File.ReadAllText(jsonFilePath);

                    return JsonSerializer.Deserialize<List<GEstionDevises>>(jsonString);
                }
                else
                {
                    Console.WriteLine("Le fichier service.json n'existe pas.");
                    return new List<GEstionDevises>();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Erreur lors du chargement des devises : " + ex.Message);
                return new List<GEstionDevises>();
            }
        }
        public static void SaveDevises(List<GEstionDevises> devises)
        {
            string jsonFilePath = "Data/service.json"; // Chemin relatif au fichier JSON
            try
            {
                // Sérialisation des objets C# en JSON
                string jsonString = JsonSerializer.Serialize(devises);

                // Écriture dans le fichier JSON
                File.WriteAllText(jsonFilePath, jsonString);
                Console.WriteLine("Les devises ont été sauvegardées avec succès.");
            }
            catch (Exception ex)
            {
                Console.WriteLine("Erreur lors de la sérialisation : " + ex.Message);
            }
        }
    }
}
