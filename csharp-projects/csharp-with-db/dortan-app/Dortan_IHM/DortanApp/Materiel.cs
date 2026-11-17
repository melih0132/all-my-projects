using System.Windows.Controls;

namespace DortanApp
{
    public enum MarqueEnum
    {
        Peli,
        Euromast,
        Martinas,
        Menfire,
        Softshell,
        Haix,
        EuropaKimanche
    }

    public class Materiel
    {
        private int id;
        private Categorie nomCategorie;
        private Site site;
        private TypeMateriel typeMateriel;
        private string nom;
        private string lienPhoto;   
        private MarqueEnum marque;
        private string description;
        private int puissanceCV;
        private int? puissanceW;
        private int coutUtilisation;

        public Materiel(int id, Categorie nomCategorie, Site site, TypeMateriel typeMateriel, string nom, string lienPhoto, MarqueEnum marque, string description, int puissanceCV, int? puissanceW, int coutUtilisation)
        {
            this.Id = id;
            this.NomCategorie = nomCategorie;
            this.Site = site;
            this.TypeMateriel = typeMateriel;
            this.Nom = nom;
            this.LienPhoto = lienPhoto;
            this.Marque = marque;
            this.Description = description;
            this.PuissanceCV = puissanceCV;
            this.PuissanceW = puissanceW;
            this.CoutUtilisation = coutUtilisation;
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

        public Categorie NomCategorie
        {
            get
            {
                return nomCategorie;
            }

            set
            {
                nomCategorie = value;
            }
        }

        public Site Site
        {
            get
            {
                return site;
            }

            set
            {
                site = value;
            }
        }

        public TypeMateriel TypeMateriel
        {
            get
            {
                return typeMateriel;
            }

            set
            {
                typeMateriel = value;
            }
        }

        public string Nom
        {
            get
            {
                return nom;
            }

            set
            {
                nom = value;
            }
        }

        public string LienPhoto
        {
            get
            {
                return lienPhoto;
            }

            set
            {
                lienPhoto = value;
            }
        }

        public MarqueEnum Marque
        {
            get
            {
                return marque;
            }

            set
            {
                marque = value;
            }
        }

        public string Description
        {
            get
            {
                return description;
            }

            set
            {
                description = value;
            }
        }

        public int PuissanceCV
        {
            get
            {
                return puissanceCV;
            }

            set
            {
                puissanceCV = value;
            }
        }

        public int? PuissanceW
        {
            get
            {
                return puissanceW;
            }

            set
            {
                puissanceW = value;
            }
        }

        public int CoutUtilisation
        {
            get
            {
                return this.coutUtilisation;
            }

            set
            {
                this.coutUtilisation = value;
            }
        }
    }
}