# python-

This repository contains a utility for subtracting background data from
BEMALINE `.data` files using pure Python (no external dependencies).

## Usage

```bash
python subtract_background.py sample.data background.data output.data
```

Both input files must have the same first column (e.g. the position or `r`
values). The result is written to `output.data` with the background intensity
removed.
