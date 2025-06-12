import sys
from typing import List, Tuple


def read_data(path: str) -> List[Tuple[float, float]]:
    """Read a two-column data file."""
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            data.append((float(parts[0]), float(parts[1])))
    return data


def subtract_background(sample_path: str, background_path: str, output_path: str) -> None:
    """Subtract background data from sample data and write the result."""
    sample = read_data(sample_path)
    background = read_data(background_path)

    if len(sample) != len(background):
        raise ValueError("Sample and background must have the same number of rows")

    result_lines = []
    for (s_pos, s_int), (b_pos, b_int) in zip(sample, background):
        if s_pos != b_pos:
            raise ValueError("Position columns do not match between sample and background")
        result_lines.append(f"{s_pos} {s_int - b_int}\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(result_lines)


def main(args: List[str]) -> int:
    if len(args) != 3:
        print(
            "Usage: python subtract_background.py <sample.data> <background.data> <output.data>",
            file=sys.stderr,
        )
        return 1
    sample_path, background_path, output_path = args
    subtract_background(sample_path, background_path, output_path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
