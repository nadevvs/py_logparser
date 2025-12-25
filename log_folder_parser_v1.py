from pathlib import Path

root = Path("/var/log")
keyword = "failed password"
needle = keyword.lower()

def get_ip_on_failure(line: str):
    parts = line.split()

    if "from" not in parts:
        return None
    
    idx = parts.index("from")

    if idx + 1 >= len(parts):
        return None
    
    return parts[idx + 1]

def parsefile(fpath, ndl):
    matched = 0
    counts = {}

    try:
        with open(fpath, encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f, start=1):
                cleared = line.strip()

                if not cleared:
                    continue
                if ndl not in cleared.lower():
                    continue

                ip = get_ip_on_failure(cleared)
                if ip is None:
                    continue

                counts[ip] = counts.get(ip, 0) + 1
                matched += 1

    except (PermissionError, OSError):
        return 0, 1, {}

    return matched, 0, counts

def parseall():
    total_skipped = 0
    total_match = 0
    total_scanned = 0
    total_counts = {}

    for path in root.rglob("*"):

        if not path.is_file():
            continue
        if path.suffix == ".gz":
            continue

        total_scanned += 1
        m, s, c = parsefile(path, needle)   
        
        total_skipped += s
        total_match += m
        for ip, cnt in c.items():
            total_counts[ip] = total_counts.get(ip, 0) + cnt

    print("\nTop IPs:")
    for ip, cnt in sorted(total_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{ip} -> {cnt}")

    print("Total matches:", total_match)
    print("Files scanned:", total_scanned)
    print("Files skipped:", total_skipped)


if __name__ == "__main__":
    parseall()
