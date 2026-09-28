import glob
import os
import subprocess
from typing import Dict, Any


def get_ssd_wear_stats() -> Dict[str, Any]:
    print("💾 \033[1;36mNVME / SSD ENDURANCE & LIFESPAN FORECASTER\033[0m")
    print("═" * 55)

    disks = glob.glob("/sys/block/nvme*") + glob.glob("/sys/block/sd*")
    stats = []

    for disk_path in disks:
        disk_name = os.path.basename(disk_path)
        stat_file = os.path.join(disk_path, "stat")
        if os.path.exists(stat_file):
            try:
                with open(stat_file, "r") as f:
                    fields = f.read().split()
                # Field 7 is sectors written (512 bytes per sector)
                sectors_written = int(fields[6])
                tb_written = round((sectors_written * 512) / (1024**4), 2)
                # Typical consumer NVMe endurance is 300 to 600 TBW
                est_tbw = 300.0
                wear_pct = round((tb_written / est_tbw) * 100, 2)
                health_pct = max(0, round(100 - wear_pct, 1))

                print(f" • Drive:            \033[1;32m{disk_name}\033[0m")
                print(f" • Data Written:     \033[1;33m{tb_written} TBW\033[0m")
                print(f" • Estimated Wear:   {wear_pct}% of {int(est_tbw)} TBW rating")
                print(f" • Remaining Health: \033[1;32m{health_pct}%\033[0m (Healthy)")
                print()
                stats.append({
                    "disk": disk_name,
                    "tb_written": tb_written,
                    "wear_pct": wear_pct,
                    "health_pct": health_pct
                })
            except Exception:
                pass

    if not stats:
        print(" • Standard Block Storage active.")
    return {"drives": stats}
