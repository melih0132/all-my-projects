namespace DortanApp
{
    public class Activite
    {
        private int id;
        private string nom;

        public Activite(int id)
        {
            this.Id = id;
        }

        public Activite(int id, string nom) : this(id)
        {
            this.Nom = nom;
        }

        public Activite(string nom)
        {
            this.Nom = nom;
        }

        public int Id
        {
            get
            {
                return id;
            }

            set
            {
                id = value;
            }
        }

        public string Nom
        {
            get
            {
                return this.nom;
            }

            set
            {
                this.nom = value;
            }
        }

        public override string? ToString()
        {
            return Nom;
        }
    }
}