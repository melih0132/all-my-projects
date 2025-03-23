using Microsoft.VisualStudio.TestTools.UnitTesting;
using Calculatrice;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NSubstitute;

namespace Calculatrice.Tests
{
    [TestClass()]
    public class CalculAvanceTests
    {
        public ICalculAvance? ObjCalculAvance
        {
            get { return CalculAvance.Instance; }
        }

        [TestMethod()]
        public void MoyenneTest()
        {
            //Arrange
            Double a = 5.0;
            Double b = 6.0;
            ICalcul? calcul = Calcul.Instance;
            //Act
            Double resultat = ObjCalculAvance!.Moyenne(calcul!, a, b);
            //Assert
            Assert.AreEqual(5.5, resultat, "Test non OK. La valeur doit être égale à 5.5.");
        }

        [TestMethod]
        public void MoyenneTestAvecStub()
        {
            //Arrange
            Double a = 5.0;
            Double b = 6.0;

            var calculStub = Substitute.For<ICalcul>(); // Définition du stub sur l'interface

            // Implémentation de deux méthodes qui vont être utilisées par le calcul de la moyenne  
            calculStub.Addition(a, b).Returns(11);
            calculStub.Division(11, 2).Returns(5.5);

            //Act
            Double resultat = ObjCalculAvance!.Moyenne(calculStub, a, b); //Utilisation du stub
            //Assert
            Assert.AreEqual(5.5, resultat, "Test non OK. La valeur doit être égale à 5.5.");
        }
    }
}