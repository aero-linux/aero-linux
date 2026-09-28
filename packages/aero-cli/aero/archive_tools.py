import os
import shutil
import tarfile
import zipfile
from typing import Dict, Any


def compress_archive(src_path: str, out_archive: str = "") -> Dict[str, Any]:
    src_path = os.path.abspath(src_path)
    if not os.path.exists(src_path):
        print(f"❌ Source path does not exist: {src_path}")
        return {"status": "error", "error": "not_found"}

    if not out_archive:
        out_archive = f"{src_path}.zip"
    out_archive = os.path.abspath(out_archive)

    print(f"📦 \033[1;36mCREATING ARCHIVE\033[0m")
    print("═" * 50)
    print(f" • Source: \033[1;33m{src_path}\033[0m")
    print(f" • Output: \033[1;32m{out_archive}\033[0m")

    if out_archive.endswith(".zip"):
        with zipfile.ZipFile(out_archive, "w", zipfile.ZIP_DEFLATED) as zf:
            if os.path.isfile(src_path):
                zf.write(src_path, os.path.basename(src_path))
            else:
                for root, _, files in os.walk(src_path):
                    for file in files:
                        full_p = os.path.join(root, file)
                        rel_p = os.path.relpath(full_p, os.path.dirname(src_path))
                        zf.write(full_p, rel_p)
    elif out_archive.endswith((".tar.gz", ".tgz")):
        with tarfile.open(out_archive, "w:gz") as tf:
            tf.add(src_path, arcname=os.path.basename(src_path))
    elif out_archive.endswith((".tar.xz", ".txz")):
        with tarfile.open(out_archive, "w:xz") as tf:
            tf.add(src_path, arcname=os.path.basename(src_path))
    else:
        with tarfile.open(out_archive, "w") as tf:
            tf.add(src_path, arcname=os.path.basename(src_path))

    size_kb = round(os.path.getsize(out_archive) / 1024, 2)
    print(f"✅ Archive created successfully ({size_kb} KB).\n")
    return {"status": "created", "path": out_archive, "size_kb": size_kb}


def extract_archive(archive_path: str, dest_dir: str = "") -> Dict[str, Any]:
    archive_path = os.path.abspath(archive_path)
    if not os.path.exists(archive_path):
        print(f"❌ Archive not found: {archive_path}")
        return {"status": "error", "error": "not_found"}

    if not dest_dir:
        dest_dir = os.path.splitext(archive_path)[0]
        if dest_dir.endswith(".tar"):
            dest_dir = os.path.splitext(dest_dir)[0]
    dest_dir = os.path.abspath(dest_dir)
    os.makedirs(dest_dir, exist_ok=True)

    print(f"📂 \033[1;36mEXTRACTING ARCHIVE\033[0m")
    print("═" * 50)
    print(f" • Archive:     \033[1;33m{archive_path}\033[0m")
    print(f" • Destination: \033[1;32m{dest_dir}\033[0m")

    if zipfile.is_zipfile(archive_path):
        with zipfile.ZipFile(archive_path, "r") as zf:
            zf.extractall(dest_dir)
    elif tarfile.is_tarfile(archive_path):
        with tarfile.open(archive_path, "r:*") as tf:
            tf.extractall(dest_dir)
    else:
        print("❌ Unsupported archive format.")
        return {"status": "error", "error": "unsupported_format"}

    print(f"✅ Extracted files to: {dest_dir}\n")
    return {"status": "extracted", "destination": dest_dir}
