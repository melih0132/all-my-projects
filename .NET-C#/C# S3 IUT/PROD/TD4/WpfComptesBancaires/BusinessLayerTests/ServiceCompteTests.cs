using Microsoft.VisualStudio.TestTools.UnitTesting;
using BusinessLayer;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using DataLayer;

namespace BusinessLayer.Tests
{
    [TestClass()]
    public class ServiceCompteTests
    {
        public void InitialisationDesTests()
        {
            DataAccess dataAccess = new DataAccess();

            dataAccess.SetData("DELETE FROM Compte");

            dataAccess.SetData("INSERT INTO Compte (Id, Solde) VALUES (1234567, 1000)");
            dataAccess.SetData("INSERT INTO Compte (Id, Solde) VALUES (2345678, 2000)");
        }

        [TestMethod()]
        public void GetAllComptesTest_Compte1()
        {
            // Arrange
            Compte attendu = new Compte(1234567, 1000);
            var service = new ServiceCompte();

            // Act
            var comptes = service.GetAllComptes();
            Compte compteRetourne = comptes.FirstOrDefault();

            // Assert
            Assert.IsNotNull(compteRetourne);
            Assert.AreEqual(attendu.IdCompte, compteRetourne.IdCompte);
            Assert.AreEqual(attendu.Solde, compteRetourne.Solde);
        }

        [TestMethod()]
        public void GetAllComptesTest_Compte2()
        {
            // Arrange
            Compte attendu = new Compte(2345678, 2000);
            var service = new ServiceCompte();

            // Act
            var comptes = service.GetAllComptes();
            Compte compteRetourne = comptes.Skip(1).FirstOrDefault(); // Le deuxième compte

            // Assert
            Assert.IsNotNull(compteRetourne);
            Assert.AreEqual(attendu.IdCompte, compteRetourne.IdCompte);
            Assert.AreEqual(attendu.Solde, compteRetourne.Solde);
        }
    }
}