from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
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
    print(f"Preparing download from URL: {url}")
    print(f"Output path: {output_path}")

    try:
        print("Starting HTTP request...")
        with urlopen(url) as response, output_path.open("wb") as dst:
            content_length = response.headers.get("Content-Length")
            total = int(content_length) if content_length else None
            downloaded = 0
            print("Streaming download in 1 MB chunks...")

            while True:
                chunk = response.read(CHUNK_SIZE)
                if not chunk:
                    break

                dst.write(chunk)
                downloaded += len(chunk)

                if total:
                    pct = downloaded / total * 100
                    print(f"\rDownloaded: {downloaded:,} / {total:,} bytes ({pct:.1f}%)", end="")
                else:
                    print(f"\rDownloaded: {downloaded:,} bytes", end="")

        print()
        print(f"Saved file to: {output_path}")
    except HTTPError as exc:
        print(f"HTTP error while downloading file: {exc.code} {exc.reason}", file=sys.stderr)
        raise
    except URLError as exc:
        print(f"Network error while downloading file: {exc.reason}", file=sys.stderr)
        raise


def build_output_path(output_dir: Path, url: str) -> Path:
    filename = url.rstrip("/").split("/")[-1]
    if not filename:
        filename = "nppes_download.zip"
    return output_dir / filename


def extract_zip(zip_path: Path, extract_root: Path) -> Path:
    extract_dir = extract_root / zip_path.stem
    extract_dir.mkdir(parents=True, exist_ok=True)

    print(f"Extracting ZIP: {zip_path}")
    print(f"Extract destination: {extract_dir}")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)
        print(f"Extracted {len(zf.namelist()):,} files.")

    return extract_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download an NPPES monthly ZIP file.")
    parser.add_argument(
        "--url",
        default=build_default_url(),
        help="Direct URL to NPPES ZIP file. Defaults to current month/year.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory to save the downloaded file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = build_output_path(args.output_dir, args.url)
    download_file(args.url, output_path)
    extract_root = args.output_dir 
    extract_zip(output_path, extract_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
