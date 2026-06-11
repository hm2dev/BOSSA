#!/usr/bin/env python3

# run as python split_hex.py input.hex [alignment, default 0x1000] [min-gap, default 0]

import sys
import os
import math

from intelhex import IntelHex

import math

def format_bytes(size_bytes):
    """
    Convert bytes to a human-readable string.
    Automatically chooses binary (KiB, MiB) for sizes >= 1 KiB,
    and decimal (KB, MB) for smaller sizes.
    
    :param size_bytes: int or float, number of bytes (must be >= 0)
    :return: str, formatted size
    """
    if not isinstance(size_bytes, (int, float)):
        raise TypeError("size_bytes must be an integer or float")
    if size_bytes < 0:
        raise ValueError("size_bytes must be non-negative")
    if size_bytes == 0:
        return "0 B"

    # Auto-select: binary for >= 1 KiB
    binary = size_bytes >= 1024
    base = 1024 if binary else 1000
    units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"] if binary else ["B", "KB", "MB", "GB", "TB", "PB"]

    index = int(math.log(size_bytes, base))
    index = min(index, len(units) - 1)

    return f"{size_bytes / base**index:.2f} {units[index]}"

def align_down(addr, align):
    return addr & ~(align - 1)

def align_up(addr, align):
    return (addr + align - 1) & ~(align - 1)

def split_hex_file(filename, alignment=0x1000, merge_gap=0):
    ih = IntelHex(filename)

    addresses = sorted(ih.addresses())

    if not addresses:
        print("No data found in HEX file.")
        return

    sections = []
    current_section = [addresses[0]]
    last_addr = addresses[0]

    # Detect sections with optional gap merging
    for addr in addresses[1:]:
        if addr <= last_addr + 1 + merge_gap:
            current_section.append(addr)
        else:
            sections.append(current_section)
            current_section = [addr]
        last_addr = addr

    sections.append(current_section)

    base_name = os.path.splitext(os.path.basename(filename))[0]

    # Write aligned sections
    for section in sections:
        start = section[0]
        end = section[-1]

        # Align addresses
        aligned_start = align_down(start, alignment)
        aligned_end = align_up(end + 1, alignment)  # +1 important for correct end

        size = aligned_end - aligned_start
        size_unpaddded=end-start;
        print(f"Padding start: {start-aligned_start}")
        print(f"Padding end:   {aligned_end-end}")
        print(f"Unpadded size: {size_unpaddded}")
        print(f"Padded size:   {size}")

        # Efficient extraction (no slow loops)
        ih.padding = 0xFF
        data = ih.tobinarray(start=aligned_start, size=size)

        out_filename = (
            f"{base_name}_0x{aligned_start:08X}-0x{aligned_end-1:08X}.bin"
        )

        with open(out_filename, "wb") as f:
            data.tofile(f)

        print(
            f"{out_filename}: "
            f"orig=0x{start:08X}-0x{end:08X}, "
            f"aligned=0x{aligned_start:08X}-0x{aligned_end-1:08X}, "
            f"size={size} (0x{size:X}) bytes "
        )


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input.hex> [alignment_hex, default 0x1000 bytes (64kiB)] [merge_gap, default 0 bytes]")
        print("Example:")
        print(f"  {sys.argv[0]} firmware.hex 0x1000 16")
        sys.exit(1)

    input_file = sys.argv[1]

    alignment = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0x1000
    merge_gap = int(sys.argv[3], 0) if len(sys.argv) > 3 else 0

    if not os.path.isfile(input_file):
        print(f"Error: file '{input_file}' not found.")
        sys.exit(1)

    print(f"Input file  : {input_file}")
    print(f"Alignment   : {alignment} bytes (0x{alignment:X}, {format_bytes(alignment)})")
    print(f"Merge gap   : {merge_gap} bytes (0x{merge_gap:X}, {format_bytes(merge_gap)})\n")

    split_hex_file(input_file, alignment, merge_gap)

if __name__ == "__main__":
    main()
