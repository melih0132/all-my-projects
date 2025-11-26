using System.ComponentModel.DataAnnotations;

namespace WSConvertisseur.Models
{
    public class Devise
    {
		private int id;
		/// <summary>
		/// Id de la devise
		/// </summary>
		public int Id
		{
			get { return id; }
			set { id = value; }
		}

		private string? nomDevise;

        /// <summary>
        /// Nom de la devise
        /// </summary>
        [Required]
        public string? NomDevise
		{
			get { return nomDevise; }
			set { nomDevise = value; }
		}

		private double taux;

        /// <summary>
        /// Taux de la devise
        /// </summary>public int Taux
        public double Taux
		{
            get { return taux; }
			set { taux = value; }
		}

        public Devise() {}

        public Devise(int id, string? nomDevise, double taux)
        {
            Id = id;
            NomDevise = nomDevise;
            Taux = taux;
        }

        public override bool Equals(object? obj)
        {
            return obj is Devise devise &&
                   Id == devise.Id &&
                   NomDevise == devise.NomDevise &&
                   Taux == devise.Taux;
        }

        public override int GetHashCode()
        {
            return HashCode.Combine(Id, NomDevise, Taux);
        }
    }
}
