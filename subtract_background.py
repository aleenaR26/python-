import sys
from typing import List, Tuple, Iterable, Optional

try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - matplotlib may be missing
    plt = None


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


def subtract_background(sample_path: str, background_path: str) -> List[Tuple[float, float]]:
    """Return background-subtracted data."""
    sample = read_data(sample_path)
    background = read_data(background_path)

    if len(sample) != len(background):
        raise ValueError("Sample and background must have the same number of rows")

    result: List[Tuple[float, float]] = []
    for (s_pos, s_int), (b_pos, b_int) in zip(sample, background):
        if s_pos != b_pos:
            raise ValueError("Position columns do not match between sample and background")
        result.append((s_pos, s_int - b_int))

    return result


def write_xy(data: Iterable[Tuple[float, float]], path: str) -> None:
    """Write two-column data to ``path`` in ``.xy`` format."""
    with open(path, "w", encoding="utf-8") as f:
        for x, y in data:
            f.write(f"{x} {y}\n")


def plot_xy(data: Iterable[Tuple[float, float]], path: Optional[str] = None) -> None:
    """Plot ``data`` using matplotlib and save to ``path`` if provided."""
    if plt is None:
        raise RuntimeError("matplotlib is required for plotting")
    x_vals = [p[0] for p in data]
    y_vals = [p[1] for p in data]
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals)
    ax.set_xlabel("Position")
    ax.set_ylabel("Intensity (background subtracted)")
    fig.tight_layout()
    if path:
        fig.savefig(path)
    else:
        fig.show()
    plt.close(fig)


def main(args: List[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Subtract background from sample data")
    parser.add_argument("sample", help="sample .data file")
    parser.add_argument("background", help="background .data file")
    parser.add_argument("output", help="path for output .xy file")
    parser.add_argument(
        "--plot",
        metavar="PNG",
        help="optional path to save a PNG plot of the result",
    )
    ns = parser.parse_args(args)

    result = subtract_background(ns.sample, ns.background)
    write_xy(result, ns.output)
    if ns.plot:
        if plt is None:
            parser.error("matplotlib is required for --plot")
        plot_xy(result, ns.plot)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
