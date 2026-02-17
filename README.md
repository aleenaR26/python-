# python-

## XRD: estimating crystallite diameter from the (100) plane

If you want the **crystallite diameter/size** from the **(100) peak** in an XRD pattern, use the Scherrer equation:

\[
D_{100} = \frac{K\lambda}{\beta \cos\theta}
\]

Where:
- \(D_{100}\): crystallite size (often called diameter) from the (100) reflection
- \(K\): shape factor (commonly 0.9, often 0.89-0.94)
- \(\lambda\): X-ray wavelength (for Cu K\(\alpha\), \(\lambda = 0.15406\) nm)
- \(\beta\): FWHM of the (100) peak in **radians**, corrected for instrumental broadening
- \(\theta\): Bragg angle for (100), i.e. half of the measured 2\(\theta\)

Instrument correction:
\[
\beta = \sqrt{\beta_{\text{measured}}^2 - \beta_{\text{instrument}}^2}
\]

Notes:
- Use peak width in **radians**, not degrees.
- This gives crystallite/domain size, not necessarily particle size.
- If you meant **d-spacing** of the (100) plane instead of diameter, use Bragg's law:
\[
d_{100} = \frac{\lambda}{2\sin\theta}
\]
