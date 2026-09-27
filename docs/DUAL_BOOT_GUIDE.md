# 🪟 Aero Linux — Dual-Boot & Partition Safety Guide

Aero Linux's Calamares installer is explicitly configured for **fail-safe dual-booting alongside Windows 10/11**.

---

## 1. Safety Principles Built Into the Installer

1. **Active EFI System Partition (ESP) Preservation:**
   - Aero Linux detects existing Windows EFI bootloaders (`/EFI/Microsoft/Boot/bootmgfw.efi`) and mounts the existing EFI partition without reformatting it.
2. **NTFS / BitLocker Partition Protection:**
   - The installer does not modify NTFS data partitions unless explicitly requested in manual partitioning.
3. **Zero-Swap Disk Configuration:**
   - Aero Linux does not carve out a 8GB–16GB disk swap partition, leaving all disk space for root `/` while leveraging dynamic in-memory **zRAM ZSTD**.

---

## 2. Recommended Dual-Boot Steps

1. **Shrink Windows Partition in Disk Management:**
   - In Windows, open `diskmgmt.msc` and shrink your main `C:` drive by **30GB to 100GB** to create "Unallocated Space".
2. **Boot Aero Linux Live USB:**
   - In BIOS/UEFI, disable Secure Boot if using proprietary NVIDIA drivers.
   - Select the USB drive in the boot menu.
3. **Run Calamares Installer (`aero-welcome` or Desktop Icon):**
   - In the **Partitioning** step, choose **"Install alongside Windows"** or choose **"Manual Partitioning"** and assign the Unallocated Space to mount as `/` with `ext4` or `btrfs`.
4. **Finish & Reboot:**
   - Systemd-boot / GRUB will automatically detect both Windows Boot Manager and Aero Linux.
