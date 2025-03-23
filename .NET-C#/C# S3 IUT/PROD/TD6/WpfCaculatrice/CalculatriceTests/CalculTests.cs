using Microsoft.VisualStudio.TestTools.UnitTesting;
using Calculatrice;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Calculatrice.Tests
{
    [TestClass()]
    public class CalculTests
    {
        public ICalcul? ObjCalcul
        {
            get { return Calcul.Instance; }
        }

        [TestMethod()]
        public void AdditionTest_AvecValeur_1_2_Retourne3()
        {
            //Arrange
            Double a = 1.0;
            Double b = 2.0;

            //Act
            Double resultat = ObjCalcul!.Addition(a, b);

            //Assert
            Assert.AreEqual(3.0, resultat, "Test non OK. La valeur doit être égale à 3.");
        }

        [TestMethod()]
        public void AdditionTest_AvecValeur_0_0_Retourne0()
        {
            //Arrange
            Double a = 0.0;
            Double b = 0.0;

            //Act
            Double resultat = ObjCalcul!.Addition(a, b);

            //Assert
            Assert.AreEqual(0.0, resultat, "Test non OK. La valeur doit être égale à 0.");
        }

        [TestMethod()]
        public void AdditionTest_AvecValeur_1_moins2_RetourneMoins1()
        {
            //Arrange
            Double a = 1.0;
            Double b = -2.0;

            //Act
            Double resultat = ObjCalcul!.Addition(a, b);

            //Assert
            Assert.AreEqual(-1.0, resultat, "Test non OK. La valeur doit être égale à -1.0.");
        }

        [TestMethod()]
        public void AdditionTest_AvecValeur_moins1_moins2_RetourneMoins3()
        {
            //Arrange
            Double a = -1.0;
            Double b = -2.0;

            //Act
            Double resultat = ObjCalcul!.Addition(a, b);

            //Assert
            Assert.AreEqual(-3.0, resultat, "Test non OK. La valeur doit être égale à -3.0.");
        }

        [TestMethod()]
        public void DivisionTest_AvecValeur_1_2_Retourne0dot5()
        {
            //Arrange
            Double a = 1.0;
            Double b = 2.0;

            //Act
            Double resultat = ObjCalcul!.Division(a, b);

            //Assert
            Assert.AreEqual(0.5, resultat, "Test non OK. La valeur doit être égale à 0.5.");
        }

        [TestMethod()]
        public void DivisionTest_AvecValeur_1_Moins2_RetourneMoins0dot5()
        {
            //Arrange
            Double a = 1.0;
            Double b = -2.0;

            //Act
            Double resultat = ObjCalcul!.Division(a, b);

            //Assert
            Assert.AreEqual(-0.5, resultat, "Test non OK. La valeur doit être égale à -0.5.");
        }

        [TestMethod()]
        public void DivisionTest_AvecValeur_0_1_Retourne0()
        {
            //Arrange
            Double a = 0.0;
            Double b = 1.0;

            //Act
            Double resultat = ObjCalcul!.Division(a, b);

            //Assert
            Assert.AreEqual(0, resultat, "Test non OK. La valeur doit être égale à 0.");
        }

        [TestMethod()]
        [ExpectedException(typeof(DivideByZeroException))]
        public void DivisionTest_AvecValeur_1_0_RetourneDivideByZeroExceptionSansAssert()
        {
            //Arrange
            Double a = 1.0;
            Double b = 0.0;

            //Act
            Double resultat = ObjCalcul!.Division(a, b);
        }

        [TestMethod()]
        public void DivisionTest_AvecValeur_1_0_RetourneDivideByZeroExceptionAvecAssert()
        {
            //Arrange
            Double a = 1.0;
            Double b = 0.0;
            DivideByZeroException? expectedException = null;

            // Act
            try
            {
                Double resultat = ObjCalcul!.Division(a, b);
            }
            catch (DivideByZeroException ex)
            {
                expectedException = ex;
            }

            // Assert
            Assert.IsNotNull(expectedException, "Test non OK. Erreur exception.");
        }
    }
}