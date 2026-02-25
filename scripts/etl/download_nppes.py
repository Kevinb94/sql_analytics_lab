from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
import shutil
import zipfile
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "NPI_Files"
CHUNK_SIZE = 1024 * 1024  # 1 MB


def build_default_url(now: datetime | None = None) -> str:
    dt = now or datetime.now()
    if dt.day >= 15:
        target = dt
    else:
        if dt.month == 1:
            target = dt.replace(year=dt.year - 1, month=12)
        else:
            target = dt.replace(month=dt.month - 1)

    month_year = target.strftime("%B_%Y")
    return f"https://download.cms.gov/nppes/NPPES_Data_Dissemination_{month_year}.zip"


def download_file(url: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Downloading: {url}")
    try:
        with urlopen(url) as response, output_path.open("wb") as dst:
            while True:
                chunk = response.read(CHUNK_SIZE)
                if not chunk:
                    break
                dst.write(chunk)

        print(f"Saved ZIP to: {output_path}")
    except HTTPError as exc:
        print(f"HTTP error: {exc.code} {exc.reason}", file=sys.stderr)
        raise
    except URLError as exc:
        print(f"Network error: {exc.reason}", file=sys.stderr)
        raise


def build_output_path(output_dir: Path, url: str) -> Path:
    filename = url.rstrip("/").split("/")[-1] or "nppes_download.zip"
    return output_dir / filename


def extract_zip(zip_path: Path, extract_root: Path) -> Path:
    extract_dir = extract_root / zip_path.stem
    extract_dir.mkdir(parents=True, exist_ok=True)

    print(f"Extracting to: {extract_dir}")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)

    return extract_dir


def organize_extracted_files(extract_dir: Path, base_dir: Path) -> None:
    """
    Move CSVs into canonical folders under base_dir.
    """

    prefix_map: dict[str, str] = {
        "endpoint_pfile_": "endpoint_pfile",
        "npidata_pfile_": "npidata_pfile",
        "othername_pfile_": "othername_pfile",
        "pl_pfile_": "pl_pfile",
    }

    for p in extract_dir.iterdir():
        if not p.is_file():
            continue

        if p.suffix.lower() != ".csv":
            continue

        dest_subfolder = None
        for prefix, folder in prefix_map.items():
            if p.name.startswith(prefix):
                dest_subfolder = folder
                break

        if not dest_subfolder:
            continue  # skip unknown CSV types

        dest_dir = base_dir / dest_subfolder
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_path = dest_dir / p.name

        if dest_path.exists():
            dest_path.unlink()

        shutil.move(str(p), str(dest_path))
        print(f"Moved {p.name} -> {dest_dir.name}/")


def main() -> int:
    parser = argparse.ArgumentParser(description="Download and organize NPPES monthly ZIP.")
    parser.add_argument(
        "--url",
        default=build_default_url(),
        help="Direct URL to NPPES ZIP file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory to save the downloaded file.",
    )

    args = parser.parse_args()

    output_path = build_output_path(args.output_dir, args.url)
    download_file(args.url, output_path)

    extract_dir = extract_zip(output_path, args.output_dir)

    organize_extracted_files(extract_dir, args.output_dir)

    # ✅ Always delete the extracted monthly folder
    shutil.rmtree(extract_dir)
    print(f"Deleted temporary folder: {extract_dir}")

    # Optional: also delete the ZIP to keep only canonical folders
    output_path.unlink(missing_ok=True)
    print(f"Deleted ZIP file: {output_path}")

    print("NPPES data successfully organized into canonical folders.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())