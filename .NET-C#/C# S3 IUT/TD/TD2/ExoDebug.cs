using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using System.Threading;
using Calculatrice;

namespace TD1Debug //Achanger si le nom du projet que vous avez créé n'est pas TD1Debug
{
    public class ExoDebug
    {
        #region Exercice 1 Error / Warning

        private double Exercice1_Error()
        {
            double nb;

            return Calcul.Addition(nb, nb);
        }

        private string Exercice1_Warning()
        {
            double nb;

            return "warning";
        }

        private int Exercice1_Warning(int a, int b)
        {
#warning TODO : return the calcul result
            return 0;
        }

        #endregion

        #region Exercice 2 Assertion

        /// <summary>
        /// Multiplication for positive integer
        /// </summary>
        /// <param name="a">positive integer</param>
        /// <param name="b">positive integer</param>
        /// <returns></returns>
        private int PositiveMult(int a, int b)
        {
            System.Diagnostics.Debug.Assert(a > 0 && b > 0, "A et/ou B sont négatif");
            return a * b;
        }

        public void Exercice2()
        {
            int c = PositiveMult(3, 2);
            Console.WriteLine("c = " + c);
            c = PositiveMult(3, -2);
            Console.WriteLine("c = " + c);
        }

        #endregion

        #region Exercice 3 Step By Step / BreakPoint Simple / Call Stack


        private void Exercice3Func3()
        {
            int a = 8;
            a--;
        }

        private void Exercice3Func2()
        {
            int a = 7;
            a--;
            Exercice3Func3();
        }

        private void Exercice3Func1()
        {
            for (int i = 0; i < 100; i++)
            {
                Exercice3Func2();
            }
        }

        public void Exercice3()
        {
            System.Diagnostics.Debugger.Break();
            Exercice3Func1();
            Exercice3Func1();
            Exercice3Func1();
            Exercice3Func1();
        }

        #endregion

        #region Exercice 4 Watch / BreakPoint Conditionnel

        /// <summary>
        /// Watch simple
        /// </summary>
        public void Exercice4_1()
        {
            System.Diagnostics.Debugger.Break();
            int a = 10;
            Calcul.Factorielle(a);
        }


        private int Fibonacci(int n)
        {
            if (n <= 1)
                return n;
            int result = Fibonacci(n - 1) + Fibonacci(n - 2);
            return result;
        }

        /// <summary>
        /// Conditionnal BreakPoint 1
        /// </summary>
        public void Exercice4_2()
        {
            System.Diagnostics.Debugger.Break();
            Fibonacci(40);
        }

        /// <summary>
        /// Conditionnal BreakPoint 1
        /// </summary>
        public void Exercice4_3()
        {
            System.Diagnostics.Debugger.Break();
            int a = 10;
            Calcul.Factorielle(a);
        }
        
        /// <summary>
        /// Trace point
        /// </summary>
        public void Exercice4_4()
        {
            System.Diagnostics.Debugger.Break();
            int a = 6;
            Calcul.Factorielle(a);
            double b = 5.5;
            Calcul.Factorielle(b);
        }
        

        #endregion

        #region Exercice 5 #if DEBUG

        private int IntFunc()
        {
            int a;
#if DEBUG
            a = 3;
#else
            a = 6;
#endif
            return a;
        }

        public void Exercice5()
        {
            int a = IntFunc();
            Console.WriteLine("a = " + a);
            Console.ReadKey();
        }

        #endregion
    }
}
