#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nettoyeur de noms de fichiers MP3 - Supprime les " (1)" à la fin
Version 1.0 - Suppression des suffixes numériques
"""

import os
import re
import argparse
from pathlib import Path
from typing import List

def find_mp3_files(directory: str) -> List[Path]:
    """Trouve tous les fichiers MP3 dans le répertoire"""
    directory_path = Path(directory)
    if not directory_path.exists():
        return []
    
    mp3_files = []
    patterns = ["*.mp3", "*.MP3", "*.Mp3", "*.mP3"]
    
    for pattern in patterns:
        for mp3_file in directory_path.glob(pattern):
            mp3_files.append(mp3_file)
    
    return mp3_files

def clean_filename(filename: str) -> str:
    """Nettoie le nom de fichier en supprimant les suffixes numériques"""
    # Pattern pour matcher " (1)", " (2)", etc. à la fin du nom
    pattern = r'\s*\(\d+\)(?=\.[^.]+$|$)'
    
    # Supprimer le pattern du nom de fichier
    cleaned = re.sub(pattern, '', filename)
    
    return cleaned

def process_directory(directory: str, dry_run: bool = False, verbose: bool = False) -> None:
    """Traite un répertoire pour nettoyer les noms de fichiers"""
    
    directory_path = Path(directory)
    if not directory_path.exists():
        print(f"[ERROR] Le répertoire '{directory}' n'existe pas.")
        return
    
    # Trouver tous les fichiers MP3
    print(f"[INFO] Recherche de fichiers MP3 dans '{directory}'...")
    mp3_files = find_mp3_files(directory)
    
    if not mp3_files:
        print("[INFO] Aucun fichier MP3 trouvé.")
        return
    
    print(f"[INFO] {len(mp3_files)} fichier(s) MP3 trouvé(s)")
    
    # Statistiques
    stats = {
        'total': len(mp3_files),
        'renamed': 0,
        'skipped': 0,
        'errors': 0
    }
    
    # Traitement des fichiers
    print(f"\n[INFO] Traitement des renommages...")
    
    for i, mp3_file in enumerate(mp3_files):
        original_name = mp3_file.name
        cleaned_name = clean_filename(original_name)
        
        # Vérifier si le nettoyage est nécessaire
        if cleaned_name == original_name:
            if verbose:
                print(f"[SKIP] Déjà correct: {original_name}")
            stats['skipped'] += 1
            continue
        
        # Préparer le nouveau chemin
        new_path = mp3_file.parent / cleaned_name
        
        # Vérifier s'il y a un conflit
        if new_path.exists() and new_path != mp3_file:
            print(f"[WARN] Conflit détecté pour {cleaned_name} - fichier ignoré")
            stats['errors'] += 1
            continue
        
        # Affichage
        print(f"\n[{i+1:3d}/{len(mp3_files)}]")
        print(f"  From: {original_name}")
        print(f"  To  : {cleaned_name}")
        
        # Renommage
        if dry_run:
            print(f"  [DRY-RUN] Renommage simulé")
        else:
            try:
                mp3_file.rename(new_path)
                print(f"  [OK] Renommé avec succès")
                stats['renamed'] += 1
            except Exception as e:
                print(f"  [ERROR] Erreur de renommage: {e}")
                stats['errors'] += 1
    
    # Résultats finaux
    print(f"\n{'='*50}")
    print(f"RÉSULTATS DU NETTOYAGE")
    print(f"{'='*50}")
    print(f"Fichiers traités     : {stats['total']}")
    print(f"Fichiers renommés    : {stats['renamed']}")
    print(f"Fichiers ignorés     : {stats['skipped']}")
    print(f"Erreurs              : {stats['errors']}")
    
    if dry_run:
        print(f"\n[DRY-RUN] Mode simulation - Aucun fichier modifié")

def main():
    """Fonction principale"""
    
    parser = argparse.ArgumentParser(
        description='Nettoyeur de noms de fichiers MP3 - Supprime les " (1)" à la fin',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  %(prog)s --dry-run              # Tester sans modifier
  %(prog)s --verbose              # Affichage détaillé  
  %(prog)s /path/to/music         # Répertoire spécifique

Fonctionnalités:
  - Supprime les suffixes numériques comme " (1)", " (2)", etc.
  - Évite les conflits de noms
  - Mode simulation disponible
        """
    )
    
    parser.add_argument(
        'directory', 
        nargs='?', 
        default='.', 
        help='Répertoire contenant les MP3 (défaut: répertoire courant)'
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true', 
        help='Mode simulation - affiche les changements sans les appliquer'
    )
    parser.add_argument(
        '--verbose', '-v', 
        action='store_true', 
        help='Affichage détaillé des informations'
    )
    
    args = parser.parse_args()
    
    try:
        process_directory(
            directory=args.directory,
            dry_run=args.dry_run,
            verbose=args.verbose
        )
    except KeyboardInterrupt:
        print("\n[STOP] Opération interrompue par l'utilisateur")
    except Exception as e:
        print(f"[FATAL] Erreur fatale : {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main() 