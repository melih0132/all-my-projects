using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;

namespace TP3console.Models.EntityFramework;

public partial class FilmsDbContext : DbContext
{
    public FilmsDbContext()
    {
    }

    public FilmsDbContext(DbContextOptions<FilmsDbContext> options)
        : base(options)
    {
    }

    public virtual DbSet<Avi> Avis { get; set; }

    public virtual DbSet<Categorie> Categories { get; set; }

    public virtual DbSet<Film> Films { get; set; }

    public virtual DbSet<Utilisateur> Utilisateurs { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        => optionsBuilder.UseNpgsql("Server=localhost;port=5433;Database=FilmsDB;uid=postgres;password=postgres;");

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Avi>(entity =>
        {
            entity.HasKey(e => new { e.Idfilm, e.Idutilisateur }).HasName("pk_avis");

            entity.HasOne(d => d.IdfilmNavigation).WithMany(p => p.Avis)
                .OnDelete(DeleteBehavior.Restrict)
                .HasConstraintName("fk_avis_film");

            entity.HasOne(d => d.IdutilisateurNavigation).WithMany(p => p.Avis)
                .OnDelete(DeleteBehavior.Restrict)
                .HasConstraintName("fk_avis_utilisateur");
        });

        modelBuilder.Entity<Categorie>(entity =>
        {
            entity.HasKey(e => e.Idcategorie).HasName("pk_categorie");
        });

        modelBuilder.Entity<Film>(entity =>
        {
            entity.HasKey(e => e.Idfilm).HasName("pk_film");

            entity.HasOne(d => d.IdcategorieNavigation).WithMany(p => p.Films)
                .OnDelete(DeleteBehavior.Restrict)
                .HasConstraintName("fk_film_categorie");
        });

        modelBuilder.Entity<Utilisateur>(entity =>
        {
            entity.HasKey(e => e.Idutilisateur).HasName("pk_utilisateur");
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
