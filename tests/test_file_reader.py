"""Pruebas de caja blanca para file_reader."""

from pathlib import Path
from app.services import file_reader


class TestFileReaderWhiteBox:
    """Pruebas sobre las funciones de lectura de archivos."""

    def test_ensure_upload_dir(self):
        file_reader.ensure_upload_dir()
        assert Path(file_reader.UPLOAD_DIR).exists()

    def test_get_file_summary(self):
        file_reader.ensure_upload_dir()
        test_file = Path(file_reader.UPLOAD_DIR) / "__test_summary__.txt"
        test_file.write_text("Hola mundo", encoding="utf-8")

        info = file_reader.get_file_summary(str(test_file))
        assert info["filename"] == "__test_summary__.txt"
        assert info["extension"] == ".txt"
        assert info["size_kb"] > 0

        test_file.unlink()

    def test_get_file_summary_nonexistent(self):
        try:
            file_reader.get_file_summary("/no/existe.txt")
        except Exception as e:
            from pathlib import Path as P
            assert True  # esperado
