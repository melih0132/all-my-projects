using System;

namespace DortanApp
{
    public class Employe
    {
        private int id;
        private Site site;
        private string identifiant;
        private string mdp;

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

        public string Identifiant
        {
            get
            {
                return identifiant;
            }

            set
            {
                identifiant = value;
            }
        }

        public string Mdp
        {
            get
            {
                return this.mdp;
            }

            set
            {
                this.mdp = value;
            }
        }

        public Employe(Site site, string identifiant, string mdp)
        {
            this.Site = site;
            this.Identifiant = identifiant;
            this.Mdp = mdp;
        }

        public Employe(string identifiant, string mdp)
        {
            this.Identifiant = identifiant;
            this.Mdp = mdp;
        }

        public Employe(int id, string identifiant, string mdp) : this(identifiant, mdp)
        {
            this.Id = id;
        }

        public Employe(int id, string identifiant)
        {
            this.Id = id;
            this.Identifiant = identifiant;
        }

        public Employe() { }
        
    }
}