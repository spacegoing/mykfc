import zipfile
from pathlib import Path

zip_file_path = Path("data-clean", "snapshot.zip")
output_folder = Path("data-clean")

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(output_folder)
