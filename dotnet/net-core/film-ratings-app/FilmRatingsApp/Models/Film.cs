using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FilmRatingsApp.Models;
public class Film
{
    public int Id
    {
        get; set;
    }
    public string Titre
    {
        get; set;
    }
    public string Resume
    {
        get; set;
    }
    public DateTime DateSortie
    {
        get; set;
    }
    public string Affiche
    {
        get; set;
    }
}
