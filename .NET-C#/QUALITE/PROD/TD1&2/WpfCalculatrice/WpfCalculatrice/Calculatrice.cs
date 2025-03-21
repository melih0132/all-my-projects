using System;
using System.ComponentModel;

namespace WpfCalculatrice
{
    /// <summary>
    /// class calculatrice non static
    /// </summary>
    public class Calculatrice : INotifyPropertyChanged
    {
        private double premierNB;
        private double secondNB;
        private double resultat;

        public event PropertyChangedEventHandler PropertyChanged;

        protected void OnPropertyChanged(string name)
        {
            PropertyChangedEventHandler handler = PropertyChanged;
            if (handler != null)
            {
                handler(this, new PropertyChangedEventArgs(name));
            }
        }

        public double PremierNB
        {
            get 
            { 
                return this.premierNB; 
            }
            set
            {
                this.premierNB = value;
                OnPropertyChanged(nameof(PremierNB));
            }
        }

        public double SecondNB
        {
            get 
            { 
                return this.secondNB; 
            }
            set
            {
                this.secondNB = value;
                OnPropertyChanged(nameof(SecondNB));
            }
        }

        public double Resultat
        {
            get 
            { 
                return this.resultat; 
            }
            set
            {
                this.resultat = value;
                OnPropertyChanged(nameof(Resultat));
            }
        }

        //public double Addition(double premierNB, double secondNB)
        //{
        //    return premierNB + secondNB;
        //}

        //public double Soustraction(double premierNB, double secondNB)
        //{
        //    return premierNB - secondNB;
        //}

        //public double Multiplication(double premierNB, double secondNB)
        //{
        //    return premierNB * secondNB;
        //}

        //public double Division(double premierNB, double secondNB)
        //{
        //    if (secondNB != 0)
        //    {
        //        return premierNB / secondNB;
        //    }
        //    else
        //    {
        //        throw new DivideByZeroException("division par zéro impossible");
        //    }
        //}
    }
}