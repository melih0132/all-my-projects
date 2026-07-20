"""Proprietes Windows (Shell Property Store)."""
from __future__ import annotations

import ctypes
import logging
import sys
import uuid
from ctypes import POINTER, WINFUNCTYPE, byref, c_void_p, wintypes
from pathlib import Path
from typing import List, Optional

from music_formatter.exceptions import PropertyWriteError
from music_formatter.models import MediaMetadata


class WindowsPropertyWriter:
    """Écrit propriétés Description / Média / Musique via le Shell Property Store."""

    GPS_READWRITE = 2
    VT_LPWSTR = 31
    VT_VECTOR = 0x1000

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        self._available = sys.platform == 'win32'
        self._com_ready = False
        self._enabled = False
        if self._available:
            try:
                self._init_com_apis()
            except Exception as e:
                self.logger.warning(
                    f"Propriétés Windows indisponibles : {e}. "
                    f"Les tags audio restent la source pour Explorer."
                )
                self._com_ready = False
                self._available = False

    def _init_com_apis(self) -> None:
        class GUID(ctypes.Structure):
            _fields_ = [
                ("Data1", ctypes.c_uint32),
                ("Data2", ctypes.c_uint16),
                ("Data3", ctypes.c_uint16),
                ("Data4", ctypes.c_ubyte * 8),
            ]

            def __init__(self, guid_str: Optional[str] = None):
                super().__init__()
                if guid_str:
                    u = uuid.UUID(guid_str)
                    self.Data1 = u.time_low
                    self.Data2 = u.time_mid
                    self.Data3 = u.time_hi_version
                    for i, b in enumerate(u.bytes[8:]):
                        self.Data4[i] = b

        class PROPERTYKEY(ctypes.Structure):
            _fields_ = [("fmtid", GUID), ("pid", ctypes.c_uint32)]

        class PROPVARIANT_UNION(ctypes.Union):
            _fields_ = [
                ("pwszVal", wintypes.LPWSTR),
                ("pszVal", wintypes.LPSTR),
                ("ulVal", ctypes.c_uint32),
            ]

        class PROPVARIANT(ctypes.Structure):
            _anonymous_ = ("data",)
            _fields_ = [
                ("vt", ctypes.c_ushort),
                ("wReserved1", ctypes.c_ubyte),
                ("wReserved2", ctypes.c_ubyte),
                ("wReserved3", ctypes.c_ubyte),
                ("data", PROPVARIANT_UNION),
            ]

        class IPropertyStoreVtbl(ctypes.Structure):
            _fields_ = [
                ("QueryInterface", WINFUNCTYPE(
                    ctypes.c_long, c_void_p, POINTER(GUID), POINTER(c_void_p)
                )),
                ("AddRef", WINFUNCTYPE(ctypes.c_ulong, c_void_p)),
                ("Release", WINFUNCTYPE(ctypes.c_ulong, c_void_p)),
                ("GetCount", WINFUNCTYPE(
                    ctypes.c_long, c_void_p, POINTER(ctypes.c_uint)
                )),
                ("GetAt", WINFUNCTYPE(
                    ctypes.c_long, c_void_p, ctypes.c_uint, POINTER(PROPERTYKEY)
                )),
                ("GetValue", WINFUNCTYPE(
                    ctypes.c_long, c_void_p, POINTER(PROPERTYKEY), POINTER(PROPVARIANT)
                )),
                ("SetValue", WINFUNCTYPE(
                    ctypes.c_long, c_void_p, POINTER(PROPERTYKEY), POINTER(PROPVARIANT)
                )),
                ("Commit", WINFUNCTYPE(ctypes.c_long, c_void_p)),
            ]

        class IPropertyStore(ctypes.Structure):
            _fields_ = [("lpVtbl", POINTER(IPropertyStoreVtbl))]

        self._GUID = GUID
        self._PROPERTYKEY = PROPERTYKEY
        self._PROPVARIANT = PROPVARIANT
        self._IPropertyStore = IPropertyStore
        self._IID_IPropertyStore = GUID("886D8EEB-8CF2-4446-8D02-CDBA1DBDCF99")

        self._shell32 = ctypes.WinDLL("shell32", use_last_error=True)
        self._ole32 = ctypes.WinDLL("ole32", use_last_error=True)
        self._propsys = ctypes.WinDLL("propsys", use_last_error=True)

        self._SHGetPropertyStoreFromParsingName = (
            self._shell32.SHGetPropertyStoreFromParsingName
        )
        self._SHGetPropertyStoreFromParsingName.argtypes = [
            wintypes.LPCWSTR,
            c_void_p,
            ctypes.c_uint32,
            POINTER(GUID),
            POINTER(c_void_p),
        ]
        self._SHGetPropertyStoreFromParsingName.restype = ctypes.c_long

        self._PropVariantClear = self._ole32.PropVariantClear
        self._PropVariantClear.argtypes = [POINTER(PROPVARIANT)]
        self._PropVariantClear.restype = ctypes.c_long

        self._CoInitialize = self._ole32.CoInitialize
        self._CoInitialize.argtypes = [c_void_p]
        self._CoInitialize.restype = ctypes.c_long

        self._oleaut32 = ctypes.WinDLL("oleaut32", use_last_error=True)
        self._SysAllocString = self._oleaut32.SysAllocString
        self._SysAllocString.argtypes = [wintypes.LPCWSTR]
        self._SysAllocString.restype = wintypes.LPWSTR

        self._PSGetPropertyKeyFromName = self._propsys.PSGetPropertyKeyFromName
        self._PSGetPropertyKeyFromName.argtypes = [
            wintypes.LPCWSTR, POINTER(PROPERTYKEY)
        ]
        self._PSGetPropertyKeyFromName.restype = ctypes.c_long

        self._com_ready = True

    def _ensure_com(self) -> None:
        if not self._available or not self._com_ready:
            return
        hr = self._CoInitialize(None)
        # S_OK=0, S_FALSE=1, RPC_E_CHANGED_MODE=0x80010106 : acceptables
        if hr not in (0, 1, 0x80010106):
            self.logger.debug(f"CoInitialize hr={hr:#x}")

    def write(self, file_path: Path, meta: MediaMetadata) -> None:
        """Écrit propriétés Description / Média / Audio via le Shell Property Store.

        Désactivé par défaut: l'API COM Shell provoque des plantages natifs
        (heap corruption) sur certains MP3. Les tags mutagen restent la source.
        Activer via enable() ou MUSIC_WRITE_WINDOWS_PROPS=1.
        """
        if not getattr(self, "_enabled", False):
            self.logger.debug(
                f"Propriétés Windows ignorées pour {file_path.name} (désactivées)."
            )
            return
        if not self._available:
            self.logger.debug("Propriétés Windows ignorées (plateforme non Windows).")
            return
        if not self._com_ready:
            raise PropertyWriteError("API COM propriétés Windows non initialisée.")

        path_str = str(file_path.resolve())
        self._ensure_com()

        store_ptr = c_void_p()
        hr = self._SHGetPropertyStoreFromParsingName(
            path_str,
            None,
            self.GPS_READWRITE,
            byref(self._IID_IPropertyStore),
            byref(store_ptr),
        )
        if hr != 0 or not store_ptr.value:
            raise PropertyWriteError(
                f"Impossible d'ouvrir le property store "
                f"(hr={hr & 0xFFFFFFFF:#010x}). "
                f"Format non supporté ou accès refusé."
            )

        store = ctypes.cast(store_ptr, POINTER(self._IPropertyStore))
        vtbl = store.contents.lpVtbl.contents
        errors: List[str] = []
        written = 0

        # Propriétés Description / Média / Musique (best effort)
        string_props = [
            ("System.Title", meta.title),
            ("System.Music.AlbumTitle", ""),
            ("System.Music.AlbumArtist", meta.albumartist),
            ("System.Comment", meta.description),
            ("System.FileDescription", meta.description),
            ("System.Subject", meta.title),
            ("System.Media.Subtitle", ""),
            ("System.Music.Genre", ""),
        ]

        try:
            for prop_name, value in string_props:
                if not value:
                    continue
                try:
                    self._set_string_property(store, vtbl, prop_name, value)
                    written += 1
                except PropertyWriteError as e:
                    errors.append(str(e))

            if meta.artist:
                try:
                    self._set_artist_properties(store, vtbl, meta.artist)
                    written += 1
                except PropertyWriteError as e:
                    errors.append(str(e))

            hr = vtbl.Commit(store)
            if hr != 0:
                raise PropertyWriteError(
                    f"Commit propriétés échoué (hr={hr & 0xFFFFFFFF:#010x}). "
                    f"Fichier peut-être ouvert ailleurs."
                )
            if written == 0 and errors:
                raise PropertyWriteError("; ".join(errors))
            if errors:
                self.logger.warning(
                    f"Propriétés partielles pour {file_path.name}: {'; '.join(errors)}"
                )

            self.logger.info(
                f"Propriétés Windows écrites : {file_path.name} "
                f"(title={meta.title!r}, album={meta.album!r}, artist={meta.artist!r})"
            )
        finally:
            try:
                vtbl.Release(store)
            except Exception:
                pass

    def enable(self, enabled: bool = True) -> None:
        self._enabled = bool(enabled)
    def _make_lpwstr_propvariant(self, value: str):
        """Construit un PROPVARIANT VT_LPWSTR (BSTR)."""
        pv = self._PROPVARIANT()
        pv.vt = self.VT_LPWSTR
        bstr = self._SysAllocString(value)
        if not bstr:
            raise PropertyWriteError("SysAllocString a échoué.")
        pv.pwszVal = bstr
        return pv

    def _set_string_property(self, store, vtbl, name: str, value: str) -> None:
        key = self._PROPERTYKEY()
        hr = self._PSGetPropertyKeyFromName(name, byref(key))
        if hr != 0:
            raise PropertyWriteError(f"Clé {name} introuvable (hr={hr:#x}).")

        pv = self._make_lpwstr_propvariant(value)
        try:
            hr = vtbl.SetValue(store, byref(key), byref(pv))
            if hr != 0:
                raise PropertyWriteError(
                    f"SetValue {name} échoué (hr={hr & 0xFFFFFFFF:#010x})."
                )
        finally:
            self._PropVariantClear(byref(pv))

    def _set_artist_properties(self, store, vtbl, artist: str) -> None:
        last_error = None
        for prop_name in ("System.Author", "System.Music.Artist"):
            try:
                self._set_string_property(store, vtbl, prop_name, artist)
                return
            except PropertyWriteError as e:
                last_error = e
        raise PropertyWriteError(
            f"Impossible d'écrire l'artiste : {last_error}"
        ) from last_error
