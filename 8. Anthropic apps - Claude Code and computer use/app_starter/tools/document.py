from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pathlib import Path

from pydantic import Field

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    path: str = Field(description="Path to a PDF or DOCX file to convert to markdown"),
) -> str:
    """Reads a PDF or DOCX file from disk and converts its contents to markdown-formatted text.

    Given the path to a local PDF or DOCX file, this tool reads the file's binary
    content and converts it to markdown, using the file's extension to determine
    how to parse it.

    When to use:
    - When you need the text contents of a PDF or DOCX file already saved to disk
    - When you have a file path rather than raw binary document data (use
      binary_document_to_markdown instead if you already have the bytes)

    When not to use:
    - For file types other than PDF or DOCX, which are not supported

    Examples:
    >>> document_path_to_markdown("reports/quarterly_summary.pdf")
    '# Quarterly Summary\\n\\n...'
    >>> document_path_to_markdown("notes/meeting_minutes.docx")
    '# Meeting Minutes\\n\\n...'
    """
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"No such file: {file_path}")
    if file_path.is_dir():
        raise IsADirectoryError(f"Expected a file, got a directory: {file_path}")

    extension = file_path.suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file extension '{extension}'. "
            f"Supported extensions are: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    binary_data = file_path.read_bytes()
    return binary_document_to_markdown(binary_data, extension)
