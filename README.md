# python-

This repository contains a utility for subtracting background data from
BEMALINE `.data` files. The result can be saved in `.xy` format, and an
optional plot can be generated with `matplotlib` (install separately).

## Usage

```bash
python subtract_background.py sample.data background.data result.xy --plot result.png
```

Both input files must have the same first column (e.g. the position or `r`
values). The result is written to `result.xy` with the background intensity
removed. If `--plot` is provided, a PNG image of the subtracted data is saved.
