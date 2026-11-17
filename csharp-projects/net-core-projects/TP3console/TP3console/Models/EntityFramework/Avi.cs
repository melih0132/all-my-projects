using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace TP3console.Models.EntityFramework;

[PrimaryKey("Idfilm", "Idutilisateur")]
[Table("avis")]
public partial class Avi
{
    [Key]
    [Column("idfilm")]
    public int Idfilm { get; set; }

    [Key]
    [Column("idutilisateur")]
    public int Idutilisateur { get; set; }

    [Column("commentaire")]
    [StringLength(1000)]
    public string? Commentaire { get; set; }

    [Column("note")]
    public decimal Note { get; set; }

    [ForeignKey("Idfilm")]
    [InverseProperty("Avis")]
    public virtual Film IdfilmNavigation { get; set; } = null!;

    [ForeignKey("Idutilisateur")]
    [InverseProperty("Avis")]
    public virtual Utilisateur IdutilisateurNavigation { get; set; } = null!;
}
