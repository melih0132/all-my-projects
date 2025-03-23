using Application_WPF_Av_Eval.UserControls;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.IO;
using Application_WPF_Av_Eval.Models;

namespace Application_WPF_Av_Eval.Services
{
    class Service
    {
        private static readonly string filePath = "./Data/Devises.json";

        public static List<Devise> ChargerDevises()
        {
            try
            {
                if (File.Exists(filePath))
                {
                    string json = File.ReadAllText(filePath);
                    return JsonSerializer.Deserialize<List<Devise>>(json);
                }
                return new List<Devise>();
            }
            catch (Exception ex)
            {
                throw new Exception("Erreur lors du chargement des devises : " + ex.Message);
            }
        }

        public static void SauvegarderDevises(List<Devise> devises)
        {
            try
            {
                string json = JsonSerializer.Serialize(devises);
                File.WriteAllText(filePath, json);
            }
            catch (Exception ex)
            {
                throw new Exception("Erreur lors de la sauvegarde des devises : " + ex.Message);
            }
        }
    }
}
