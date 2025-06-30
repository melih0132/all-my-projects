#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renommeur de fichiers MP3 intelligent avec identification musicale par IA
Version 2.0 - Traitement par batch et identification musicale
Format de sortie: "Artiste Principal - Titre ft. Artiste Secondaire.mp3"
"""

import os
import re
import json
import argparse
import unicodedata
import sys
import time
from pathlib import Path
from typing import Tuple, List, Optional, Dict, Any, Union

# Imports conditionnels
try:
    from mutagen.easyid3 import EasyID3
    from mutagen.id3 import ID3NoHeaderError
    from mutagen.mp3 import MP3
    MUTAGEN_AVAILABLE = True
except ImportError:
    print("[WARN] ATTENTION: mutagen non installé. Les tags ID3 ne seront pas lus.")
    print("   Installez avec: pip install mutagen")
    MUTAGEN_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    print("[WARN] ATTENTION: openai non installé. Le mode IA ne sera pas disponible.")
    print("   Installez avec: pip install openai")
    OPENAI_AVAILABLE = False

def load_env_file() -> None:
    """Charge les variables d'environnement depuis le fichier .env"""
    env_file = Path('.env')
    if env_file.exists():
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip().strip('"\'')
            print("[OK] Fichier .env chargé avec succès")
        except Exception as e:
            print(f"[WARN] Erreur lors du chargement du fichier .env : {e}")

def setup_openai_client() -> Optional[OpenAI]:
    """Configure et retourne le client OpenAI"""
    if not OPENAI_AVAILABLE:
        print("[ERROR] OpenAI non disponible")
        return None
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("[ERROR] OPENAI_API_KEY non trouvée dans les variables d'environnement.")
        return None
    
    try:
        client = OpenAI(api_key=api_key, timeout=60.0)
        return client
    except Exception as e:
        print(f"[ERROR] Erreur lors de la configuration OpenAI : {e}")
        return None

def extract_music_info_from_tags(filepath: str) -> Dict[str, Optional[str]]:
    """Extrait les informations musicales depuis les tags ID3"""
    if not MUTAGEN_AVAILABLE:
        return {'artist': None, 'title': None, 'album': None, 'duration': None}
    
    try:
        audio_file = MP3(str(filepath))
        tags = EasyID3(str(filepath))
        
        return {
            'artist': tags.get('artist', [None])[0],
            'title': tags.get('title', [None])[0],
            'album': tags.get('album', [None])[0],
            'duration': f"{int(audio_file.info.length // 60)}:{int(audio_file.info.length % 60):02d}" if audio_file.info.length else None
        }
    except Exception:
        return {'artist': None, 'title': None, 'album': None, 'duration': None}

def collect_all_music_files(directory: str) -> List[Dict[str, Any]]:
    """Collecte tous les fichiers MP3 avec leurs informations"""
    directory = Path(directory)
    if not directory.exists():
        return []
    
    music_files = []
    patterns = ["*.mp3", "*.MP3", "*.Mp3", "*.mP3"]
    
    for pattern in patterns:
        for mp3_file in directory.glob(pattern):
            # Extraire les informations de base
            filename_clean = clean_filename_for_analysis(mp3_file.stem)
            tags_info = extract_music_info_from_tags(mp3_file)
            
            file_info = {
                'original_path': str(mp3_file),
                'original_name': mp3_file.name,
                'filename_cleaned': filename_clean,
                'tags': tags_info,
                'file_size': mp3_file.stat().st_size if mp3_file.exists() else 0
            }
            
            music_files.append(file_info)
    
    return music_files

def clean_filename_for_analysis(filename: str) -> str:
    """Nettoie le nom de fichier pour l'analyse par l'IA"""
    # Supprimer les parasites courants
    parasites_patterns = [
        r'\(official\s*video\)', r'\(clip\s*officiel\)', r'\(audio\)', r'\(visualizer\)',
        r'\(paroles\)', r'\(lyrics\)', r'\(audio\s*officiel\)', r'\(lyric\s*video\)',
        r'\[[^\]]*\]', r'\([0-9]+\)', r'\(.*?video.*?\)', r'\(.*?audio.*?\)', 
        r'official\s*video', r'lyrics?', r'music\s*video', r'\bmv\b', r'video',
        r'\bHD\b', r'\bHQ\b', r'\b4K\b', r'\baudio\b', r'visualizer',
        r'topic', r'vevo', r'records?', r'entertainment', r'download',
        r'remix(?!\s*\w)', r'edit(?!\s*\w)', r'version(?!\s*\w)', r'remaster(?!\s*\w)'
    ]
    
    cleaned = filename
    for pattern in parasites_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # Nettoyer les espaces multiples et caractères indésirables
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    cleaned = re.sub(r'[_\-\s]+', ' ', cleaned).strip()
    
    return cleaned

def identify_music_batch_with_ai(music_files: List[Dict[str, Any]], client: OpenAI, batch_size: int = 20) -> Dict[str, Dict[str, Any]]:
    """Identifie les morceaux par petits lots pour respecter les limites de tokens"""
    if not client or not music_files:
        return {}
    
    all_identifications = {}
    total_files = len(music_files)
    
    # Traitement par batches
    for batch_start in range(0, total_files, batch_size):
        batch_end = min(batch_start + batch_size, total_files)
        batch_files = music_files[batch_start:batch_end]
        
        print(f"[AI] Traitement du lot {batch_start//batch_size + 1}/{(total_files + batch_size - 1)//batch_size} ({batch_end - batch_start} fichiers)")
        
        # Préparer la liste des morceaux pour ce batch
        files_for_analysis = []
        for i, file_info in enumerate(batch_files):
            global_id = batch_start + i
            entry = {
                'id': global_id,
                'filename': file_info['filename_cleaned'],
                'original_name': file_info['original_name']
            }
            
            # Ajouter les tags si disponibles
            if file_info['tags']['artist'] or file_info['tags']['title']:
                entry['existing_tags'] = {
                    'artist': file_info['tags']['artist'],
                    'title': file_info['tags']['title'],
                    'album': file_info['tags']['album']
                }
            
            files_for_analysis.append(entry)
        
        # Créer le prompt pour ce batch
        prompt = f"""
Tu es un expert musical avec une connaissance approfondie de la musique internationale (pop, rap, rock, électronique, world music, etc.).

MISSION: Identifier et standardiser {len(files_for_analysis)} morceaux de musique.

RÈGLES D'IDENTIFICATION:
1. Utilise ta base de connaissances musicales pour identifier chaque morceau
2. Si le nom est ambigu, fais de ton mieux pour identifier l'artiste et le titre corrects
3. Ignore les parasites techniques (Official Video, Lyrics, etc.)
4. Détecte les collaborations: ft, feat, featuring, avec, &, x, X
5. Respecte l'orthographe officielle des artistes et titres
6. Pour les featuring: sépare l'artiste principal des artistes secondaires
7. Si tu ne peux pas identifier un morceau, utilise les informations disponibles

MORCEAUX À IDENTIFIER:
{json.dumps(files_for_analysis, ensure_ascii=False, indent=1)}

RÉPONSE REQUISE - JSON VALIDE UNIQUEMENT:
{{
  "identifications": {{
    "{files_for_analysis[0]['id']}": {{
      "artiste_principal": "Nom officiel de l'artiste principal",
      "titre": "Titre officiel du morceau", 
      "featuring": "Artiste(s) secondaire(s) OU null si aucun",
      "confiance": "high/medium/low",
      "source": "knowledge_base/filename/tags"
    }}
  }}
}}

IMPORTANT: 
- Réponds UNIQUEMENT en JSON valide
- Utilise tes connaissances musicales pour identifier les vrais noms d'artistes
- Si incertain, indique "confiance": "low"
"""

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Utiliser GPT-3.5 pour économiser les tokens
                messages=[
                    {"role": "system", "content": "Tu es un expert musical. Tu réponds TOUJOURS en JSON valide uniquement, sans texte supplémentaire."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000,
                timeout=60
            )
            
            result = response.choices[0].message.content.strip()
            
            # Nettoyer le JSON
            if result.startswith('```json'):
                result = result[7:]
            if result.endswith('```'):
                result = result[:-3]
            result = result.strip()
            
            parsed_result = json.loads(result)
            
            if 'identifications' in parsed_result:
                # Ajouter les identifications de ce batch
                all_identifications.update(parsed_result['identifications'])
                print(f"[OK] Lot traité avec succès ({len(parsed_result['identifications'])} identifications)")
            else:
                print("[WARN] Format de réponse IA inattendu pour ce lot")
                # Créer des identifications de fallback pour ce batch
                for file_info in files_for_analysis:
                    file_id = str(file_info['id'])
                    all_identifications[file_id] = create_fallback_identification(file_info)
                
        except json.JSONDecodeError as e:
            print(f"[WARN] Erreur JSON pour le lot {batch_start//batch_size + 1}: {e}")
            # Créer des identifications de fallback pour ce batch
            for file_info in files_for_analysis:
                file_id = str(file_info['id'])
                all_identifications[file_id] = create_fallback_identification(file_info)
                
        except Exception as e:
            print(f"[WARN] Erreur API pour le lot {batch_start//batch_size + 1}: {e}")
            # Créer des identifications de fallback pour ce batch
            for file_info in files_for_analysis:
                file_id = str(file_info['id'])
                all_identifications[file_id] = create_fallback_identification(file_info)
        
        # Délai entre les batches pour éviter le rate limiting
        if batch_end < total_files:
            time.sleep(1)
    
    print(f"[AI] Identification terminée: {len(all_identifications)} morceaux traités")
    return all_identifications

def create_fallback_identification(file_info: Dict[str, Any]) -> Dict[str, Any]:
    """Crée une identification de fallback quand l'IA échoue"""
    filename = file_info.get('filename', '')
    
    # Essayer d'extraire des informations basiques
    if ' - ' in filename:
        parts = filename.split(' - ', 1)
        artist = parts[0].strip()
        title = parts[1].strip()
        
        # Chercher un featuring
        featuring = None
        feat_patterns = [r' ft\.?\s+(.+)', r' feat\.?\s+(.+)', r' featuring\s+(.+)', r' avec\s+(.+)']
        for pattern in feat_patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                featuring = match.group(1).strip()
                title = re.sub(pattern, '', title, flags=re.IGNORECASE).strip()
                break
        
        return {
            'artiste_principal': artist,
            'titre': title,
            'featuring': featuring,
            'confiance': 'low',
            'source': 'fallback'
        }
    
    return {
        'artiste_principal': filename or 'Artiste Inconnu',
        'titre': 'Titre Inconnu',
        'featuring': None,
        'confiance': 'low',
        'source': 'fallback'
    }

def smart_title_case(text: str) -> str:
    """Met en forme le texte avec une capitalisation intelligente"""
    if not text:
        return ""
    
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Mots à ne pas capitaliser
    lowercase_words = {
        'a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'if', 'in', 'is',
        'it', 'of', 'on', 'or', 'to', 'up', 'via', 'with', 'the',
        'le', 'la', 'les', 'de', 'du', 'des', 'et', 'ou', 'avec', 'dans',
        'sur', 'pour', 'par', 'un', 'une', 'ce', 'cette', 'ces',
        've', 'ile', 'bir', 'bu', 'şu', 'o', 'da', 'de', 'ta', 'te',
        'ft', 'feat', 'featuring', 'avec'
    }
    
    words = text.split()
    result = []
    
    for i, word in enumerate(words):
        if any(char in word for char in "''`"):
            result.append(word)
        elif i == 0:
            result.append(word.capitalize())
        elif word.lower() in lowercase_words:
            result.append(word.lower())
        else:
            result.append(word.capitalize())
    
    return ' '.join(result)

def sanitize_filename(filename: str) -> str:
    """Nettoie un nom de fichier pour qu'il soit compatible"""
    if not filename:
        return "fichier_sans_nom"
    
    # Caractères interdits
    invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
    filename = re.sub(invalid_chars, '', filename)
    
    # Supprimer les points en fin
    filename = filename.rstrip('.')
    
    # Limiter la longueur
    if len(filename) > 200:
        half = 97
        filename = filename[:half] + "..." + filename[-half:]
    
    return filename.strip() or "fichier_nettoye"

def build_new_filename(identification: Dict[str, Any]) -> str:
    """Construit le nouveau nom de fichier selon le format standard"""
    artist = identification.get('artiste_principal', '').strip()
    title = identification.get('titre', '').strip()
    featuring = identification.get('featuring', '') or ''
    
    # Gérer le cas où featuring peut être une liste
    if isinstance(featuring, list):
        featuring = ', '.join(featuring) if featuring else ''
    else:
        featuring = featuring.strip() if featuring else ''
    
    if not artist or not title:
        return None
    
    # Formater
    artist = smart_title_case(artist)
    title = smart_title_case(title)
    
    # Construire le nom
    if featuring and featuring.lower() not in ['null', 'none', '']:
        featuring = smart_title_case(featuring)
        filename = f"{artist} - {title} ft. {featuring}.mp3"
    else:
        filename = f"{artist} - {title}.mp3"
    
    return sanitize_filename(filename)

def get_safe_target_path(directory: Path, target_name: str) -> Path:
    """Génère un chemin sûr en évitant les conflits"""
    target_path = directory / target_name
    
    if not target_path.exists():
        return target_path
    
    base = target_path.stem
    ext = target_path.suffix
    
    for i in range(1, 101):
        new_name = f"{base} ({i}){ext}"
        new_path = directory / new_name
        if not new_path.exists():
            return new_path
    
    # Fallback avec timestamp
    import time
    timestamp = int(time.time())
    return directory / f"{base}_{timestamp}{ext}"

def process_music_directory(directory: str, dry_run: bool = False, verbose: bool = False, 
                          limit: Optional[int] = None, batch_size: int = 20) -> None:
    """Traite un répertoire complet de fichiers musicaux"""
    
    load_env_file()
    
    directory_path = Path(directory)
    if not directory_path.exists():
        print(f"[ERROR] Le répertoire '{directory}' n'existe pas.")
        return
    
    # Configuration OpenAI
    client = setup_openai_client()
    if not client:
        print("[ERROR] Impossible de configurer OpenAI.")
        return
    
    # Collecter tous les fichiers musicaux
    print(f"[INFO] Analyse du répertoire '{directory}'...")
    music_files = collect_all_music_files(directory)
    
    if not music_files:
        print("[ERROR] Aucun fichier MP3 trouvé.")
        return
    
    # Limiter par défaut à 400 fichiers si aucune limite n'est spécifiée
    if limit is None:
        limit = 400
    
    if limit and limit > 0:
        music_files = music_files[:limit]
    
    print(f"[INFO] {len(music_files)} fichier(s) MP3 trouvé(s) (limite: {limit})")
    
    # Identification par batch avec l'IA
    identifications = identify_music_batch_with_ai(music_files, client, batch_size)
    
    if not identifications:
        print("[ERROR] Échec de l'identification IA")
        return
    
    # Statistiques
    stats = {
        'total': len(music_files),
        'renamed': 0,
        'skipped': 0,
        'errors': 0,
        'high_confidence': 0,
        'medium_confidence': 0,
        'low_confidence': 0
    }
    
    # Traitement des renommages
    print(f"\n[INFO] Traitement des renommages...")
    
    for i, file_info in enumerate(music_files):
        file_id = str(i)
        original_path = Path(file_info['original_path'])
        
        if file_id not in identifications:
            print(f"[WARN] Pas d'identification pour {original_path.name}")
            stats['errors'] += 1
            continue
        
        identification = identifications[file_id]
        confidence = identification.get('confiance', 'unknown')
        
        # Compter les niveaux de confiance
        if confidence == 'high':
            stats['high_confidence'] += 1
        elif confidence == 'medium':
            stats['medium_confidence'] += 1
        elif confidence == 'low':
            stats['low_confidence'] += 1
        
        # Construire le nouveau nom
        new_filename = build_new_filename(identification)
        
        if not new_filename:
            print(f"[ERROR] Impossible de construire le nom pour {original_path.name}")
            stats['errors'] += 1
            continue
        
        # Vérifier si le renommage est nécessaire
        if new_filename == original_path.name:
            if verbose:
                print(f"[SKIP] Déjà correct: {original_path.name}")
            stats['skipped'] += 1
            continue
        
        # Préparer le nouveau chemin
        target_path = get_safe_target_path(directory_path, new_filename)
        
        # Affichage
        feat_info = f" ft. {identification.get('featuring', '')}" if identification.get('featuring') and identification.get('featuring').lower() not in ['null', 'none'] else ""
        confidence_indicator = f"[{confidence.upper()}]" if confidence != 'unknown' else ""
        
        print(f"\n[{i+1:3d}/{len(music_files)}] {confidence_indicator}")
        print(f"  From: {original_path.name}")
        print(f"  To  : {target_path.name}")
        
        if verbose:
            print(f"  Artist: {identification.get('artiste_principal', 'N/A')}")
            print(f"  Title : {identification.get('titre', 'N/A')}")
            if feat_info:
                print(f"  Feat  : {identification.get('featuring', 'N/A')}")
        
        # Renommage
        if dry_run:
            print(f"  [DRY-RUN] Renommage simulé")
        else:
            try:
                original_path.rename(target_path)
                print(f"  [OK] Renommé avec succès")
                stats['renamed'] += 1
            except Exception as e:
                print(f"  [ERROR] Erreur de renommage: {e}")
                stats['errors'] += 1
    
    # Résultats finaux
    print(f"\n{'='*50}")
    print(f"RÉSULTATS DU TRAITEMENT")
    print(f"{'='*50}")
    print(f"Fichiers traités     : {stats['total']}")
    print(f"Fichiers renommés    : {stats['renamed']}")
    print(f"Fichiers ignorés     : {stats['skipped']}")
    print(f"Erreurs              : {stats['errors']}")
    print(f"\nNIVEAUX DE CONFIANCE:")
    print(f"Haute confiance      : {stats['high_confidence']}")
    print(f"Confiance moyenne    : {stats['medium_confidence']}")
    print(f"Faible confiance     : {stats['low_confidence']}")
    
    if dry_run:
        print(f"\n[DRY-RUN] Mode simulation - Aucun fichier modifié")

def main():
    """Fonction principale"""
    
    parser = argparse.ArgumentParser(
        description='Renommeur MP3 intelligent avec identification musicale par IA v2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  %(prog)s --dry-run              # Tester sans modifier
  %(prog)s --verbose              # Affichage détaillé  
  %(prog)s --limit 10             # Limiter à 10 fichiers
  %(prog)s /path/to/music         # Répertoire spécifique

Nouveautés v2.0:
  - Identification musicale par IA en batch
  - Meilleure précision grâce à la base de connaissances musicales
  - Niveaux de confiance pour chaque identification
  - Traitement optimisé (moins de tokens utilisés)

Prérequis:
  - Fichier .env avec OPENAI_API_KEY=votre_clé
  - pip install openai mutagen
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
    parser.add_argument(
        '--limit', 
        type=int, 
        help='Limite le nombre de fichiers à traiter (pour tester)'
    )
    parser.add_argument(
        '--batch-size', 
        type=int, 
        default=20,
        help='Nombre de fichiers à traiter par lot IA (défaut: 20)'
    )
    
    args = parser.parse_args()
    
    try:
        process_music_directory(
            directory=args.directory,
            dry_run=args.dry_run,
            verbose=args.verbose,
            limit=args.limit,
            batch_size=args.batch_size
        )
    except KeyboardInterrupt:
        print("\n[STOP] Opération interrompue par l'utilisateur")
    except Exception as e:
        print(f"[FATAL] Erreur fatale : {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()