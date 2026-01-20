"""
Module de formatage de titres musicaux avec refactorisation complète.
Séparation des responsabilités et amélioration de la maintenabilité.
"""
import os
import re
import sys
import json
import logging
from pathlib import Path
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass, field
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
from datetime import datetime
import uuid

# ============================================================================
# CONSTANTES
# ============================================================================

INVALID_FILENAME_CHARS = '<>:"/\\|?*'
MAX_FILENAME_LENGTH = 255
MAX_PATH_LENGTH = 260  # Limite Windows pour les chemins longs
DEFAULT_CACHE_SIZE = 1000
DEFAULT_WORKERS = 4
PROCESSING_TIMEOUT = 30  # secondes

# Configuration par défaut
DEFAULT_CONFIG = {
    "cleanup_patterns": [
        r'\s*\(Official Audio\)',
        r'\s*\(Official Video\)',
        r'\s*\[Official Audio\]',
        r'\s*\[Official Video\]',
        r'\s*\(Official Lyrics Video\)',
        r'\s*\[Official Lyrics Video\]',
        r'\s*\(Clip Officiel\)',
        r'\s*\(Audio Officiel\)',
        r'\s*\(Lyrics?\)',
        r'\s*\[Lyrics?\]',
        r'\s*\(Paroles?\)',
        r'\s*\[Paroles?\]',
        r'\s*\(HD\)',
        r'\s*\[HD\]',
        r'\s*\(Music Video\)',
        r'\s*\[Music Video\]',
        r'\s*\(4K\)',
        r'\s*\[4K\]',
        r'\s*\(1080p?\)',
        r'\s*\[1080p?\]',
        r'\s*\(Visualizer\)',
        r'\s*\[Visualizer\]',
        r'\s*\(Remastered\)',
        r'\s*\[Remastered\]'
    ],
    "feat_patterns": [
        r'\s*\(\s*(feat\.?|featuring|ft\.?)\s+([^)]+)\)',
        r'\s*\[\s*(feat\.?|featuring|ft\.?)\s+([^\]]+)\]',
        r'\s+(feat\.?|featuring|ft\.?)\s+(.+)'
    ],
    "artist_separators": [r'\s*&\s*', r'\s*x\s*', r'\s*,\s*', r'\s*\+\s*'],
    "music_extensions": ['.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg', '.wma', '.opus'],
    "title_case_exceptions": [
        'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 
        'to', 'for', 'of', 'with', 'by'
    ]
}


# ============================================================================
# CLASSES DE DONNÉES
# ============================================================================

@dataclass(frozen=True)
class ParsedTitle:
    """Structure immuable pour stocker les informations d'un titre parsé"""
    main_artist: Optional[str]
    song_title: str
    featured_artists: Tuple[str, ...]
    original_title: str
    
    def format_title(self) -> str:
        """Formate le titre selon les règles définies"""
        featured_str = ' & '.join(self.featured_artists) if self.featured_artists else None
        
        if self.main_artist:
            base = f"{self.main_artist} - {self.song_title}"
            return f"{base} ft. {featured_str}" if featured_str else base
        return f"{self.song_title} ft. {featured_str}" if featured_str else self.song_title


@dataclass
class ProcessingStats:
    """Gère les statistiques de traitement"""
    processed: int = 0
    cache_hits: int = 0
    errors: int = 0
    
    def increment_processed(self) -> None:
        """Incrémente le compteur de fichiers traités"""
        self.processed += 1
    
    def increment_cache_hits(self) -> None:
        """Incrémente le compteur de cache hits"""
        self.cache_hits += 1
    
    def increment_errors(self) -> None:
        """Incrémente le compteur d'erreurs"""
        self.errors += 1
    
    def to_dict(self) -> Dict:
        """Convertit les statistiques en dictionnaire"""
        return {
            'processed': self.processed,
            'cache_hits': self.cache_hits,
            'errors': self.errors
        }


# ============================================================================
# UTILITAIRES
# ============================================================================

class LRUCache:
    """Cache LRU simple pour remplacer le dict basique"""
    
    def __init__(self, max_size: int = DEFAULT_CACHE_SIZE):
        self.max_size = max_size
        self._cache: OrderedDict = OrderedDict()
    
    def __contains__(self, key: str) -> bool:
        return key in self._cache
    
    def __getitem__(self, key: str) -> str:
        """Récupère une valeur et la déplace à la fin (LRU)"""
        value = self._cache.pop(key)
        self._cache[key] = value
        return value
    
    def __setitem__(self, key: str, value: str) -> None:
        """Ajoute ou met à jour une valeur"""
        if key in self._cache:
            self._cache.pop(key)
        elif len(self._cache) >= self.max_size:
            self._cache.popitem(last=False)
        self._cache[key] = value


class ConfigLoader:
    """Gère le chargement et la validation de la configuration"""
    
    @staticmethod
    def load(config_file: Optional[str]) -> Dict:
        """Charge la configuration depuis un fichier ou utilise la config par défaut"""
        config = DEFAULT_CONFIG.copy()
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    if isinstance(loaded_config, dict):
                        config.update(loaded_config)
                    else:
                        logging.warning("Format de configuration invalide. Utilisation de la config par défaut.")
            except (json.JSONDecodeError, IOError) as e:
                logging.warning(f"Erreur lors du chargement de la config : {e}. Utilisation de la config par défaut.")
        
        return config


class FilenameSanitizer:
    """Gère le nettoyage et la validation des noms de fichiers"""
    
    @staticmethod
    def sanitize(filename: str) -> str:
        """Nettoie un nom de fichier des caractères invalides"""
        for char in INVALID_FILENAME_CHARS:
            filename = filename.replace(char, '_')
        
        filename = filename.rstrip('. ')
        
        if len(filename) > MAX_FILENAME_LENGTH:
            filename = filename[:MAX_FILENAME_LENGTH]
        
        return filename
    
    @staticmethod
    def is_path_too_long(file_path: Path) -> bool:
        """Vérifie si le chemin est trop long pour Windows"""
        return len(str(file_path.absolute())) > MAX_PATH_LENGTH
    
    @staticmethod
    def has_invalid_chars(filename: str) -> bool:
        """Vérifie si le nom de fichier contient des caractères invalides"""
        return any(char in filename for char in INVALID_FILENAME_CHARS)


# ============================================================================
# CLASSES PRINCIPALES
# ============================================================================

class PatternCompiler:
    """Compile et gère tous les patterns regex"""
    
    def __init__(self, config: Dict):
        self.config = config
        self._compile_all()
    
    def _compile_all(self) -> None:
        """Compile tous les patterns regex"""
        self.cleanup_patterns = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in self.config['cleanup_patterns']
        ]
        
        self.feat_patterns = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in self.config['feat_patterns']
        ]
        
        # Pattern combiné pour tous les séparateurs d'artistes
        all_separators = '|'.join(self.config['artist_separators'])
        self.combined_artist_separator = re.compile(all_separators)
        
        # Patterns pré-compilés pour le nettoyage
        self.track_number_pattern = re.compile(r'^\d{1,3}[\s\-\.]*')
        self.multiple_spaces_pattern = re.compile(r'\s+')
        self.multiple_separators_pattern = re.compile(r'[_\-]{2,}')
        
        # Structures de données optimisées
        self.music_extensions = frozenset(self.config['music_extensions'])
        self.title_case_exceptions = frozenset(self.config['title_case_exceptions'])


class TitleCleaner:
    """Gère le nettoyage des titres"""
    
    def __init__(self, patterns: PatternCompiler):
        self.patterns = patterns
    
    def clean(self, title: str) -> str:
        """Nettoie le titre des mentions indésirables"""
        if not title:
            return ""
        
        cleaned = title.strip()
        if not cleaned:
            return ""
        
        cleaned = self.patterns.track_number_pattern.sub('', cleaned).strip()
        if not cleaned:
            return ""
        
        for pattern in self.patterns.cleanup_patterns:
            cleaned = pattern.sub('', cleaned)
            if not cleaned:
                return ""
        
        cleaned = self.patterns.multiple_spaces_pattern.sub(' ', cleaned).strip()
        cleaned = self.patterns.multiple_separators_pattern.sub(' ', cleaned)
        
        return cleaned


class ArtistExtractor:
    """Gère l'extraction et le traitement des artistes"""
    
    def __init__(self, patterns: PatternCompiler):
        self.patterns = patterns
    
    def extract_featured(self, title: str) -> Tuple[str, List[str]]:
        """Extrait les artistes en featuring du titre"""
        if not title:
            return "", []
        
        for pattern in self.patterns.feat_patterns:
            match = pattern.search(title)
            if match:
                main_title = title[:match.start()].strip()
                feat_part = match.group(2).strip()
                
                if feat_part:
                    artists = self.split_artists(feat_part)
                    return main_title, artists
                return main_title, []
        
        return title, []
    
    def split_artists(self, artist_string: str) -> List[str]:
        """Divise une chaîne d'artistes en liste"""
        if not artist_string:
            return []
        
        parts = self.patterns.combined_artist_separator.split(artist_string.strip())
        artists = [part.strip() for part in parts if part.strip()]
        
        if not artists:
            return []
        
        # Déduplication en préservant l'ordre
        seen = set()
        unique_artists = []
        for artist in artists:
            artist_lower = artist.lower()
            if artist and artist_lower not in seen:
                seen.add(artist_lower)
                unique_artists.append(self._capitalize(artist))
        
        return unique_artists
    
    def _capitalize(self, text: str) -> str:
        """Capitalisation intelligente respectant les règles de titre"""
        if not text:
            return text
        
        text = text.strip()
        if not text:
            return text
        
        if text.isupper() and len(text) <= 5:
            return text
        
        words = text.split()
        if not words:
            return text
        
        result = []
        for i, word in enumerate(words):
            word_lower = word.lower()
            if i == 0 or word_lower not in self.patterns.title_case_exceptions:
                if word:
                    result.append(word[0].upper() + word_lower[1:])
            else:
                result.append(word_lower)
        
        return ' '.join(result)


class TitleParser:
    """Parse la structure complète d'un titre"""
    
    def __init__(self, cleaner: TitleCleaner, extractor: ArtistExtractor):
        self.cleaner = cleaner
        self.extractor = extractor
    
    def parse(self, title: str) -> ParsedTitle:
        """Parse la structure complète du titre"""
        if not title:
            return ParsedTitle(None, "", (), "")
        
        original_title = title
        cleaned = self.cleaner.clean(title)
        
        if not cleaned:
            return ParsedTitle(None, original_title, (), original_title)
        
        if ' - ' in cleaned:
            return self._parse_with_separator(cleaned, original_title)
        else:
            return self._parse_simple(cleaned, original_title)
    
    def _parse_with_separator(self, cleaned: str, original_title: str) -> ParsedTitle:
        """Parse un titre avec séparateur artiste-titre"""
        parts = cleaned.split(' - ', 1)
        artist_part = parts[0].strip()
        song_part = parts[1].strip()
        
        if not artist_part or not song_part:
            return self._parse_simple(cleaned, original_title)
        
        song_title, song_featured = self.extractor.extract_featured(song_part)
        main_artist, artist_featured = self._parse_artist_part(artist_part)
        
        all_featured = tuple(artist_featured + song_featured)
        
        return ParsedTitle(
            main_artist if main_artist else None,
            self.extractor._capitalize(song_title) if song_title else original_title,
            all_featured,
            original_title
        )
    
    def _parse_simple(self, cleaned: str, original_title: str) -> ParsedTitle:
        """Parse un titre simple sans séparateur"""
        song_title, featured = self.extractor.extract_featured(cleaned)
        return ParsedTitle(
            None,
            self.extractor._capitalize(song_title) if song_title else original_title,
            tuple(featured),
            original_title
        )
    
    def _parse_artist_part(self, artist_string: str) -> Tuple[str, List[str]]:
        """Parse la partie artiste pour identifier principal et collaborateurs"""
        if not artist_string:
            return "", []
        
        main_part, featured = self.extractor.extract_featured(artist_string)
        main_artists = self.extractor.split_artists(main_part)
        
        if len(main_artists) > 1:
            return main_artists[0], main_artists[1:] + featured
        return main_artists[0] if main_artists else "", featured


class MusicTitleFormatter:
    """Classe principale pour reformater les titres musicaux"""
    
    def __init__(self, config_file: Optional[str] = None):
        config = ConfigLoader.load(config_file)
        patterns = PatternCompiler(config)
        
        self.cleaner = TitleCleaner(patterns)
        self.extractor = ArtistExtractor(patterns)
        self.parser = TitleParser(self.cleaner, self.extractor)
        self.patterns = patterns
        
        self._format_cache = LRUCache(max_size=DEFAULT_CACHE_SIZE)
        self.stats = ProcessingStats()
    
    def format_title(self, title: str) -> str:
        """Méthode principale de formatage avec gestion d'erreurs et cache LRU"""
        if not title:
            return ""
        
        try:
            if title in self._format_cache:
                self.stats.increment_cache_hits()
                return self._format_cache[title]
            
            self.stats.increment_processed()
            parsed = self.parser.parse(title)
            result = parsed.format_title()
            
            self._format_cache[title] = result
            return result
            
        except (AttributeError, IndexError, KeyError) as e:
            self.stats.increment_errors()
            logging.error(f"Erreur lors du formatage de '{title}': {e}", exc_info=True)
            return title
        except Exception as e:
            self.stats.increment_errors()
            logging.error(f"Erreur inattendue lors du formatage de '{title}': {e}", exc_info=True)
            return title
    
    def get_stats(self) -> Dict:
        """Retourne les statistiques de traitement"""
        return self.stats.to_dict()


class FileSystemHandler:
    """Gère les opérations sur le système de fichiers"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.sanitizer = FilenameSanitizer()
    
    def get_music_files(self, folder_path: str, extensions: frozenset, 
                       recursive: bool = False) -> List[Tuple[Path, str, str]]:
        """Récupère tous les fichiers musicaux"""
        folder = Path(folder_path)
        
        if not folder.exists():
            raise FileNotFoundError(f"Le dossier '{folder_path}' n'existe pas.")
        
        if not folder.is_dir():
            raise NotADirectoryError(f"'{folder_path}' n'est pas un dossier.")
        
        pattern = "**/*" if recursive else "*"
        music_files = []
        
        try:
            for file_path in folder.glob(pattern):
                if file_path.is_file() and file_path.suffix.lower() in extensions:
                    music_files.append((file_path, file_path.stem, file_path.suffix))
        except PermissionError as e:
            self.logger.error(f"Permission refusée pour accéder à '{folder_path}': {e}")
            raise
        except Exception as e:
            self.logger.error(f"Erreur lors de la lecture du dossier : {e}", exc_info=True)
            raise
        
        return sorted(music_files, key=lambda x: x[0].name.lower())
    
    def rename_file(self, file_path: Path, new_name: str) -> bool:
        """Renomme un fichier avec gestion d'erreurs améliorée"""
        sanitized_name = self.sanitizer.sanitize(new_name)
        new_path = file_path.parent / sanitized_name
        
        # Vérifications préalables
        if self.sanitizer.is_path_too_long(new_path):
            self.logger.warning(f"Chemin trop long pour '{sanitized_name}'. Ignoré.")
            return False
        
        if self.sanitizer.has_invalid_chars(sanitized_name):
            self.logger.error(f"Nom de fichier invalide : '{sanitized_name}'")
            return False
        
        # Gestion du renommage
        try:
            if file_path.name.lower() == sanitized_name.lower() and file_path.name != sanitized_name:
                return self._fix_case(file_path, sanitized_name, new_path)
            
            if new_path.exists() and new_path != file_path:
                self.logger.warning(f"Le fichier '{sanitized_name}' existe déjà. Ignoré.")
                return False
            
            file_path.rename(new_path)
            self.logger.info(f"Renommé : {file_path.name} -> {sanitized_name}")
            return True
            
        except PermissionError as e:
            self.logger.error(f"Permission refusée lors du renommage : {e}")
            return False
        except OSError as e:
            self.logger.error(f"Erreur système lors du renommage : {e}")
            return False
        except Exception as e:
            self.logger.error(f"Erreur inattendue lors du renommage : {e}", exc_info=True)
            return False
    
    def _fix_case(self, file_path: Path, sanitized_name: str, new_path: Path) -> bool:
        """Corrige uniquement la casse du nom de fichier"""
        temp_name = f"temp_{uuid.uuid4().hex[:8]}_{sanitized_name}"
        temp_path = file_path.parent / temp_name
        
        try:
            file_path.rename(temp_path)
            temp_path.rename(new_path)
            self.logger.info(f"Casse corrigée : {file_path.name} -> {sanitized_name}")
            return True
        except Exception as e:
            self.logger.error(f"Erreur lors de la correction de casse : {e}")
            return False


class ResultDisplay:
    """Gère l'affichage des résultats"""
    
    @staticmethod
    def display_file_result(original_name: str, formatted_title: str, 
                           needs_rename: bool, new_name: Optional[str] = None) -> None:
        """Affiche le résultat pour un fichier"""
        print(f"\nAnalyse : {original_name}")
        print(f"   Titre formaté : '{formatted_title}'")
        
        if needs_rename and new_name:
            print(f"   CHANGEMENT DÉTECTÉ")
            print(f"   Original : {original_name}")
            print(f"   Nouveau  : {new_name}")
        else:
            print(f"   Aucun changement nécessaire")
    
    @staticmethod
    def display_stats(stats: Dict, dry_run: bool) -> None:
        """Affiche les statistiques finales"""
        print(f"\n=== STATISTIQUES ===")
        print(f"Fichiers trouvés : {stats['total']}")
        print(f"Fichiers traités : {stats['processed']}")
        print(f"Fichiers {'à renommer' if dry_run else 'renommés'} : {stats['renamed']}")
        print(f"Erreurs : {stats['errors']}")
        
        if 'formatter_stats' in stats:
            fmt_stats = stats['formatter_stats']
            print(f"Cache hits : {fmt_stats['cache_hits']}")
            print(f"Erreurs de formatage : {fmt_stats['errors']}")


class MusicFileProcessor:
    """Classe principale pour traiter les fichiers musicaux dans un dossier"""
    
    def __init__(self, config_file: Optional[str] = None, max_workers: int = DEFAULT_WORKERS):
        self.formatter = MusicTitleFormatter(config_file)
        self.max_workers = max_workers
        self.logger = self._setup_logging()
        self.fs_handler = FileSystemHandler(self.logger)
        self.display = ResultDisplay()
    
    @staticmethod
    def _setup_logging() -> logging.Logger:
        """Configure le logging"""
        if not logging.getLogger().handlers:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler('music_formatter.log', encoding='utf-8'),
                    logging.StreamHandler()
                ]
            )
        return logging.getLogger(__name__)
    
    def process_single_file(self, file_info: Tuple[Path, str, str]) -> Optional[Tuple[Path, str, str, bool]]:
        """Traite un seul fichier"""
        file_path, name_without_ext, extension = file_info
        
        try:
            formatted_name = self.formatter.format_title(name_without_ext)
            new_filename = formatted_name + extension
            needs_rename = file_path.name != new_filename
            
            return (file_path, file_path.name, new_filename, needs_rename)
        except Exception as e:
            self.logger.error(f"Erreur lors du traitement de {file_path}: {e}", exc_info=True)
            return None
    
    def _process_files_parallel(self, music_files: List[Tuple[Path, str, str]]) -> Tuple[List, int]:
        """Traite les fichiers en parallèle"""
        results = []
        errors = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.process_single_file, file_info): file_info
                for file_info in music_files
            }
            
            for future in as_completed(futures):
                try:
                    result = future.result(timeout=PROCESSING_TIMEOUT)
                    if result:
                        results.append(result)
                    else:
                        errors += 1
                except Exception as e:
                    file_info = futures[future]
                    self.logger.error(f"Erreur dans le traitement parallèle pour {file_info[0]}: {e}", exc_info=True)
                    errors += 1
        
        return results, errors
    
    def _process_files_sequential(self, music_files: List[Tuple[Path, str, str]]) -> Tuple[List, int]:
        """Traite les fichiers séquentiellement"""
        results = []
        errors = 0
        
        for file_info in music_files:
            result = self.process_single_file(file_info)
            if result:
                results.append(result)
            else:
                errors += 1
        
        return results, errors
    
    def _process_results(self, results: List, dry_run: bool) -> int:
        """Traite les résultats et effectue les renommages si nécessaire"""
        renamed_count = 0
        
        for file_path, original_name, new_name, needs_rename in results:
            formatted_title = self.formatter.format_title(file_path.stem)
            self.display.display_file_result(original_name, formatted_title, needs_rename, new_name)
            
            if needs_rename:
                if not dry_run:
                    if self.fs_handler.rename_file(file_path, new_name):
                        renamed_count += 1
                else:
                    renamed_count += 1
        
        return renamed_count
    
    def process_folder(self, folder_path: str, dry_run: bool = True, 
                      recursive: bool = False, parallel: bool = True) -> Dict:
        """Traite tous les fichiers d'un dossier"""
        music_files = self.fs_handler.get_music_files(
            folder_path, 
            self.formatter.patterns.music_extensions, 
            recursive
        )
        
        if not music_files:
            self.logger.info("Aucun fichier musical trouvé dans le dossier.")
            return {'total': 0, 'processed': 0, 'renamed': 0, 'errors': 0}
        
        self.logger.info(f"Fichiers musicaux trouvés : {len(music_files)}")
        
        # Traitement parallèle ou séquentiel
        if parallel and len(music_files) > 1:
            results, errors = self._process_files_parallel(music_files)
        else:
            results, errors = self._process_files_sequential(music_files)
        
        # Traitement des résultats
        renamed_count = self._process_results(results, dry_run)
        
        return {
            'total': len(music_files),
            'processed': len(results),
            'renamed': renamed_count,
            'errors': errors,
            'formatter_stats': self.formatter.get_stats()
        }
    
    def create_backup_list(self, folder_path: str, output_file: str = "backup_list.json") -> None:
        """Crée une liste de sauvegarde des noms de fichiers"""
        try:
            music_files = self.fs_handler.get_music_files(
                folder_path, 
                self.formatter.patterns.music_extensions
            )
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'folder': folder_path,
                'files': [{'original': str(f[0]), 'name': f[1], 'ext': f[2]} for f in music_files]
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Liste de sauvegarde créée : {output_file}")
        except (IOError, PermissionError) as e:
            self.logger.error(f"Erreur lors de la création de la sauvegarde : {e}")
        except Exception as e:
            self.logger.error(f"Erreur inattendue lors de la création de la sauvegarde : {e}", exc_info=True)


# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def create_sample_config() -> None:
    """Crée un fichier de configuration d'exemple"""
    config = {
        "cleanup_patterns": [
            "\\s*\\(Official Audio\\)",
            "\\s*\\(Official Video\\)",
            "\\s*\\[Official Audio\\]",
            "\\s*\\[Official Video\\]"
        ],
        "feat_patterns": [
            "\\s*\\(\\s*(feat\\.?|featuring|ft\\.?)\\s+([^)]+)\\)",
            "\\s*\\[\\s*(feat\\.?|featuring|ft\\.?)\\s+([^\\]]+)\\]"
        ],
        "artist_separators": ["\\s*&\\s*", "\\s*x\\s*", "\\s*,\\s*"],
        "music_extensions": [".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg", ".wma"],
        "title_case_exceptions": [
            "a", "an", "the", "and", "or", "but", "in", "on", "at", 
            "to", "for", "of", "with", "by"
        ]
    }
    
    try:
        with open("music_formatter_config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print("Fichier de configuration d'exemple créé : music_formatter_config.json")
    except IOError as e:
        print(f"Erreur lors de la création du fichier de configuration : {e}")


def create_argument_parser() -> argparse.ArgumentParser:
    """Crée et configure le parser d'arguments"""
    parser = argparse.ArgumentParser(
        description="Reformateur de titres musicaux optimisé",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python music_formatter.py                    # Applique les changements
  python music_formatter.py --verbose           # Mode simulation
  python music_formatter.py --recursive        # Traitement récursif
  python music_formatter.py --create-config    # Créer un fichier de config
        """
    )
    
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Mode simulation (affiche les changements sans les appliquer)')
    parser.add_argument('--recursive', '-r', action='store_true',
                       help='Traitement récursif des sous-dossiers')
    parser.add_argument('--config', help='Fichier de configuration JSON')
    parser.add_argument('--parallel', action='store_true', default=True,
                       help='Traitement parallèle (par défaut)')
    parser.add_argument('--no-parallel', dest='parallel', action='store_false',
                       help='Désactiver le traitement parallèle')
    parser.add_argument('--workers', type=int, default=DEFAULT_WORKERS,
                       help=f'Nombre de workers pour le traitement parallèle (défaut: {DEFAULT_WORKERS})')
    parser.add_argument('--create-config', action='store_true',
                       help='Créer un fichier de configuration d\'exemple')
    parser.add_argument('--backup', action='store_true',
                       help='Créer une sauvegarde des noms de fichiers')
    
    return parser


def display_startup_info(args: argparse.Namespace, dry_run: bool, folder_path: str) -> None:
    """Affiche les informations de démarrage"""
    print("=== REFORMATEUR DE TITRES MUSICAUX (Version Optimisée) ===")
    print(f"Dossier : {folder_path}")
    print(f"Mode : {'SIMULATION' if dry_run else 'APPLICATION'}")
    print(f"Récursif : {'OUI' if args.recursive else 'NON'}")
    print(f"Parallèle : {'OUI' if args.parallel else 'NON'}")
    if args.parallel:
        print(f"Workers : {args.workers}")
    if args.config:
        print(f"Config : {args.config}")
    print()


def get_script_directory() -> str:
    """Retourne le chemin du dossier contenant le script Python"""
    return str(Path(__file__).parent.absolute())


def main() -> None:
    """Fonction principale avec interface en ligne de commande"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    if args.create_config:
        create_sample_config()
        return
    
    # Utiliser automatiquement le dossier du script
    folder_path = get_script_directory()
    # Par défaut, on applique les changements. --verbose active le mode simulation
    dry_run = args.verbose
    display_startup_info(args, dry_run, folder_path)
    
    try:
        processor = MusicFileProcessor(args.config, args.workers)
        
        if args.backup:
            processor.create_backup_list(folder_path)
        
        stats = processor.process_folder(
            folder_path, 
            dry_run=dry_run, 
            recursive=args.recursive,
            parallel=args.parallel
        )
        
        processor.display.display_stats(stats, dry_run)
        
    except KeyboardInterrupt:
        print("\nInterruption par l'utilisateur.")
        sys.exit(130)
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"Erreur : {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        logging.exception("Erreur détaillée :")
        sys.exit(1)


if __name__ == "__main__":
    main()
