
namespace Calculatrice
{
    /// <summary>
    /// Static class for method
    /// </summary>
    public static class Calcul
    {
        /// <summary>
        /// méthod add
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static double Addition( double a, double b )
            { return a + b; }

        /// <summary>
        /// méthod supp
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static double Soustraction( double a, double b ) 
            { return a - b; }

        /// <summary>
        /// méthod mult
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static double Multiplication( double a, double b)
            { return a * b; }

        /// <summary>
        /// méthod div
        /// </summary>
        /// <param name="premierNB"></param>
        /// <param name="secondNB"></param>
        /// <returns></returns>
        /// <exception cref="DivideByZeroException"></exception>
        public static double Division(double premierNB, double secondNB)
        {
            if (secondNB != 0)
            {
                return premierNB / secondNB;
            }
            else
            {
                throw new DivideByZeroException("division par zéro impossible");
            }
        }

        /// <summary>
        /// méthod fact
        /// </summary>
        /// <param name="a"></param>
        /// <returns></returns>
        /// <exception cref="ArgumentException"></exception>
        public static double Factorielle(double a)
        {
            if (a < 0)
            {
                throw new ArgumentException("La factorielle n'est pas définie pour les nombres négatifs");
            }
            if (a == 0 || a == 1)
            {
                return 1;
            }

            double result = 1;
            for (int i = 1; i <= a; i++)
            {
                result *= i;
            }
            return result;
        }
    }
}
