import io
import codecs
from collections.abc import Iterator

from src.text_processing import detect_encoding, repair_text

ENCODING_SAMPLE_SIZE = 65536
STREAM_READ_CHUNK_SIZE = 65536


def iter_decoded_lines(binary_stream) -> Iterator[str]:
    """Декодирует бинарный поток и возвращает его построчно"""
    sample = binary_stream.read(ENCODING_SAMPLE_SIZE)
    encoding = detect_encoding(sample)

    if _is_seekable(binary_stream):
        yield from _iter_seekable_text_lines(binary_stream, encoding)
        return

    yield from _iter_non_seekable_text_lines(binary_stream, sample, encoding)


def _iter_seekable_text_lines(binary_stream, encoding: str) -> Iterator[str]:
    """Читает построчно поток, который поддерживает перемотку"""
    binary_stream.seek(0)
    with io.TextIOWrapper(binary_stream, encoding=encoding, errors="replace", newline="") as text_file:
        for line in text_file:
            yield from _normalize_text_line(line)


def _iter_non_seekable_text_lines(binary_stream, sample: bytes, encoding: str) -> Iterator[str]:
    """Читает и декодирует поток без поддержки перемотки"""
    decoder = codecs.getincrementaldecoder(encoding)(errors="replace")
    pending = ""

    for chunk in _iter_binary_chunks(binary_stream, sample):
        text = decoder.decode(chunk)
        pending += text
        lines, pending = _split_complete_lines(pending)
        for line in lines:
            yield from _normalize_text_line(line)

    pending += decoder.decode(b"", final=True)
    lines, _ = _split_complete_lines(pending, final=True)
    for line in lines:
        yield from _normalize_text_line(line)


def _iter_binary_chunks(binary_stream, sample: bytes) -> Iterator[bytes]:
    """Возвращает поток порциями"""
    if sample:
        yield sample

    while True:
        chunk = binary_stream.read(STREAM_READ_CHUNK_SIZE)
        if not chunk:
            break
        yield chunk


def _split_complete_lines(text: str, final: bool = False) -> tuple[list[str], str]:
    """Разделяет буфер на завершённые строки и оставшийся хвост"""
    text = text.replace("\r\n", "\n")
    parts = text.split("\n")
    if final:
        return parts[:-1] if text.endswith("\n") else parts, ""

    return parts[:-1], parts[-1]


def _normalize_text_line(line: str) -> Iterator[str]:
    """Исправляет кодировку строки и нормализует её переводы строк"""
    repaired_line = repair_text(line)
    normalized_line = repaired_line.replace("\\r\\n", "\n").replace("\\n", "\n")
    yield from normalized_line.splitlines()


def _is_seekable(binary_stream) -> bool:
    """Проверяет, можно ли перемещаться по потоку"""
    seekable = getattr(binary_stream, "seekable", None)
    if callable(seekable):
        return bool(seekable())

    return False
