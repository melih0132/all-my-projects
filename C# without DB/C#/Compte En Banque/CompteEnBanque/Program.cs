namespace CompteEnBanque
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Text;

    class Program
    {
        static void Main(string[] args)
        {
            Console.OutputEncoding = Encoding.UTF8;

            CompteCourant compteCourant = new CompteCourant("Melih Cetinkaya", "CC123");
            CompteEpargne compteEpargne = new CompteEpargne("Melih Cetinkaya", "CE456");

            string option = "";

            do
            {
                Console.WriteLine("Appuyez sur Entrée pour afficher le menu.");
                Console.ReadLine();

                Console.WriteLine("Veuillez sélectionner une option ci-dessous :");
                Console.WriteLine("[I] Voir les informations sur le titulaire du compte");
                Console.WriteLine("[CS] Compte courant - Consulter le solde");
                Console.WriteLine("[CD] Compte courant - Déposer des fonds");
                Console.WriteLine("[CR] Compte courant - Retirer des fonds");
                Console.WriteLine("[ES] Compte épargne - Consulter le solde");
                Console.WriteLine("[ED] Compte épargne - Déposer des fonds");
                Console.WriteLine("[ER] Compte épargne - Retirer des fonds");
                Console.WriteLine("[X] Quitter");
                option = Console.ReadLine().ToUpper();

                switch (option)
                {
                    case "I":
                        AfficherInformations(compteCourant);
                        break;
                    case "CS":
                        Console.WriteLine($"Solde du compte courant : {compteCourant.Solde}€");
                        break;
                    case "CD":
                        GererDepot(compteCourant);
                        break;
                    case "CR":
                        GererRetrait(compteCourant);
                        break;
                    case "ES":
                        Console.WriteLine($"Solde du compte épargne : {compteEpargne.Solde}€");
                        break;
                    case "ED":
                        GererDepot(compteEpargne);
                        break;
                    case "ER":
                        GererRetrait(compteEpargne);
                        break;
                    case "X":
                        Console.WriteLine("Application fermée.");
                        break;
                    default:
                        Console.WriteLine("Option invalide.");
                        break;
                }
            }
            while (option != "X");

            // Écriture des transactions dans des fichiers distincts
            compteCourant.EcrireTransactionsDansFichier("transactions_compte_courant.txt");
            compteEpargne.EcrireTransactionsDansFichier("transactions_compte_epargne.txt");
        }

        static void AfficherInformations(Compte compte)
        {
            Console.WriteLine($"Titulaire: {compte.Titulaire}");
            Console.WriteLine($"Numéro de compte: {compte.NumeroCompte}");
        }

        static void GererDepot(Compte compte)
        {
            Console.WriteLine("Quel montant souhaitez-vous déposer ?");
            if (decimal.TryParse(Console.ReadLine(), out decimal montant))
            {
                compte.Deposer(montant);
                Console.WriteLine($"Vous avez déposé : {montant}€.");
            }
            else
            {
                Console.WriteLine("Montant invalide.");
            }
        }

        static void GererRetrait(Compte compte)
        {
            Console.WriteLine("Quel montant souhaitez-vous retirer ?");
            if (decimal.TryParse(Console.ReadLine(), out decimal montant))
            {
                compte.Retirer(montant);
                Console.WriteLine($"Vous avez retiré : {montant}€.");
            }
            else
            {
                Console.WriteLine("Montant invalide.");
            }
        }
    }

    // Classe de base Compte
    public abstract class Compte
    {
        public string Titulaire { get; set; }
        public string NumeroCompte { get; set; }
        public decimal Solde { get; protected set; }
        private List<Transaction> transactions;

        public Compte(string titulaire, string numeroCompte)
        {
            Titulaire = titulaire;
            NumeroCompte = numeroCompte;
            Solde = 0;
            transactions = new List<Transaction>();
        }

        public abstract void Deposer(decimal montant);
        public abstract void Retirer(decimal montant);

        public void EnregistrerTransaction(string type, decimal montant)
        {
            transactions.Add(new Transaction(DateTime.Now, type, montant));
        }

        // Méthode pour écrire les transactions dans un fichier
        public void EcrireTransactionsDansFichier(string cheminFichier)
        {
            using (StreamWriter sw = new StreamWriter(cheminFichier))
            {
                foreach (var transaction in transactions)
                {
                    sw.WriteLine($"{transaction.Date} - {transaction.Type} - {transaction.Montant}€");
                }
            }
        }
    }

    // Exemple de classe dérivée, CompteCourant
    public class CompteCourant : Compte
    {
        public CompteCourant(string titulaire, string numeroCompte) : base(titulaire, numeroCompte) { }

        public override void Deposer(decimal montant)
        {
            Solde += montant;
            EnregistrerTransaction("Dépôt", montant);
        }

        public override void Retirer(decimal montant)
        {
            if (Solde >= montant)
            {
                Solde -= montant;
                EnregistrerTransaction("Retrait", montant);
            }
            else
            {
                Console.WriteLine("Fonds insuffisants pour le retrait.");
            }
        }
    }

    // Exemple de classe dérivée, CompteEpargne
    public class CompteEpargne : Compte
    {
        public CompteEpargne(string titulaire, string numeroCompte) : base(titulaire, numeroCompte) { }

        public override void Deposer(decimal montant)
        {
            Solde += montant;
            EnregistrerTransaction("Dépôt", montant);
        }

        public override void Retirer(decimal montant)
        {
            if (Solde >= montant)
            {
                Solde -= montant;
                EnregistrerTransaction("Retrait", montant);
            }
            else
            {
                Console.WriteLine("Fonds insuffisants pour le retrait.");
            }
        }
    }

    // Classe Transaction
    public class Transaction
    {
        public DateTime Date { get; set; }
        public string Type { get; set; }
        public decimal Montant { get; set; }

        public Transaction(DateTime date, string type, decimal montant)
        {
            Date = date;
            Type = type;
            Montant = montant;
        }
    }

}
