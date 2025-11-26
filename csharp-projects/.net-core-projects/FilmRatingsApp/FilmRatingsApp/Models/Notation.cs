using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FilmRatingsApp.Models;
public class Notation
{
    public int Id
    {
        get; set;
    }
    public int UtilisateurId
    {
        get; set;
    }
    public int FilmId
    {
        get; set;
    }
    public int Note
    {
        get; set;
    }
    public Utilisateur Utilisateur
    {
        get; set;
    }
    public Film Film
    {
        get; set;
    }
}
