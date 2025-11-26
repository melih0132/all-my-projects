using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Mvc;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using APIfilms.Models.EntityFramework;
using APIfilms.Controllers;
using APIfilms.Models.Repository;
using APIfilms.Models.DataManager;
using Moq;
using System.Linq;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace APIfilms.Tests
{
    [TestClass]
    public class UtilisateursControllerTests
    {
        private FilmRatingsDBContext context;
        private UtilisateursController controller;
        private IDataRepository<Utilisateur> dataRepository;

        [TestInitialize]
        public void Initialize()
        {
            var options = new DbContextOptionsBuilder<FilmRatingsDBContext>()
                .UseInMemoryDatabase(databaseName: "TestDatabase")
                .Options;

            context = new FilmRatingsDBContext(options);
            dataRepository = new UtilisateurManager(context);
            controller = new UtilisateursController(dataRepository);
        }

        [TestCleanup]
        public void Cleanup()
        {
            context.Database.EnsureDeleted();
            context.Dispose();
        }

        [TestMethod]
        public async Task GetAllUtilisateurs_ReturnsAllUsers()
        {
            context.Utilisateurs.AddRange(new List<Utilisateur>
            {
                new Utilisateur { Nom = "Alice", Mail = "alice@test.com" },
                new Utilisateur { Nom = "Bob", Mail = "bob@test.com" }
            });
            await context.SaveChangesAsync();

            var result = await controller.GetUtilisateurs();
            Assert.AreEqual(2, result.Value.Count());
        }

        [TestMethod]
        public async Task GetUtilisateurById_ReturnsCorrectUser()
        {
            var user = new Utilisateur { Nom = "Test", Prenom = "User", Mail = "test@example.com" };
            context.Utilisateurs.Add(user);
            await context.SaveChangesAsync();

            var result = await controller.GetUtilisateurById(user.UtilisateurId);
            Assert.IsNotNull(result.Value);
            Assert.AreEqual(user.Mail, result.Value.Mail);
        }

        [TestMethod]
        public async Task GetUtilisateurById_ReturnsNotFound()
        {
            var result = await controller.GetUtilisateurById(999);
            Assert.IsInstanceOfType(result.Result, typeof(NotFoundResult));
        }

        [TestMethod]
        public void Postutilisateur_ModelValidated_CreationOK_AvecMoq()
        {
            var mockRepository = new Mock<IDataRepository<Utilisateur>>();
            var userController = new UtilisateursController(mockRepository.Object);

            Utilisateur user = new Utilisateur
            {
                Nom = "POISSON",
                Prenom = "Pascal",
                Mobile = "1",
                Mail = "poisson@gmail.com",
                Pwd = "Toto12345678!",
                Rue = "Chemin de Bellevue",
                CodePostal = "74940",
                Ville = "Annecy-le-Vieux",
                Pays = "France",
                Latitude = null,
                Longitude = null
            };

            var actionResult = userController.PostUtilisateur(user).Result;

            Assert.IsInstanceOfType(actionResult, typeof(ActionResult<Utilisateur>), "Pas un ActionResult<Utilisateur>");
            Assert.IsInstanceOfType(actionResult.Result, typeof(CreatedAtActionResult), "Pas un CreatedAtActionResult");

            var result = actionResult.Result as CreatedAtActionResult;
            Assert.IsInstanceOfType(result.Value, typeof(Utilisateur), "Pas un Utilisateur");

            user.UtilisateurId = ((Utilisateur)result.Value).UtilisateurId;
            Assert.AreEqual(user, (Utilisateur)result.Value, "Utilisateurs pas identiques");
        }

        [TestMethod]
        public async Task DeleteUtilisateurTest_AvecMoq()
        {
            Utilisateur user = new Utilisateur
            {
                UtilisateurId = 1,
                Nom = "Calida",
                Prenom = "Lilley",
                Mobile = "0653930778",
                Mail = "clilleymd@last.fm",
                Pwd = "Toto12345678!",
                Rue = "Impasse des bergeronnettes",
                CodePostal = "74200",
                Ville = "Allinges",
                Pays = "France",
                Latitude = 46.344795F,
                Longitude = 6.4885845F
            };

            var mockRepository = new Mock<IDataRepository<Utilisateur>>();
            mockRepository.Setup(x => x.GetByIdAsync(1).Result).Returns(user);

            var userController = new UtilisateursController(mockRepository.Object);
            var actionResult = userController.DeleteUtilisateur(1).Result;

            Assert.IsInstanceOfType(actionResult, typeof(NoContentResult), "Pas un NoContentResult");
        }
    }
}