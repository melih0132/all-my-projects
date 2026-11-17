using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace TP3console.Models.EntityFramework;

[Table("film")]
public partial class Film
{
    [Key]
    [Column("idfilm")]
    public int Idfilm { get; set; }

    [Column("nom")]
    [StringLength(50)]
    public string Nom { get; set; } = null!;

    [Column("description")]
    public string? Description { get; set; }

    [Column("idcategorie")]
    public int Idcategorie { get; set; }

    [InverseProperty("IdfilmNavigation")]
    public virtual ICollection<Avi> Avis { get; set; } = new List<Avi>();

    [ForeignKey("Idcategorie")]
    [InverseProperty("Films")]
    public virtual Categorie IdcategorieNavigation { get; set; } = null!;
}
