using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace TP3console.Models.EntityFramework;

[Table("utilisateur")]
public partial class Utilisateur
{
    [Key]
    [Column("idutilisateur")]
    public int Idutilisateur { get; set; }

    [Column("login")]
    [StringLength(50)]
    public string Login { get; set; } = null!;

    [Column("email")]
    [StringLength(100)]
    public string Email { get; set; } = null!;

    [Column("pwd")]
    [StringLength(64)]
    public string Pwd { get; set; } = null!;

    [InverseProperty("IdutilisateurNavigation")]
    public virtual ICollection<Avi> Avis { get; set; } = new List<Avi>();
}
