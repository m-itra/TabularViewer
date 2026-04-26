from ftfy import fix_encoding
from charset_normalizer import from_bytes


def detect_encoding(sample: bytes) -> str:
    """Определяет наиболее вероятную кодировку текстового фрагмента"""
    best_match = from_bytes(sample).best()
    if best_match is None:
        return "utf-8"

    if best_match.encoding == "utf_8" and best_match.bom:
        return "utf_8_sig"

    return best_match.encoding


def repair_text(text: str) -> str:
    """Исправляет ошибки кодировки в тексте"""
    return fix_encoding(text)
