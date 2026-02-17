"""Utilities to compute XRD quantities for the (100) reflection.

This module provides:
- Scherrer crystallite size estimate from the (100) peak
- d-spacing from Bragg's law
"""

from __future__ import annotations

import argparse
import math


CU_K_ALPHA_NM = 0.15406


def degrees_to_radians(value_deg: float) -> float:
    """Convert degrees to radians."""
    return math.radians(value_deg)


def corrected_fwhm_radians(beta_measured_deg: float, beta_instrument_deg: float) -> float:
    """Return instrument-corrected FWHM in radians.

    Uses:
        beta = sqrt(beta_measured^2 - beta_instrument^2)

    Inputs are provided in degrees and converted to radians internally.
    """
    if beta_measured_deg <= beta_instrument_deg:
        raise ValueError("Measured FWHM must be greater than instrument FWHM.")

    beta_measured_rad = degrees_to_radians(beta_measured_deg)
    beta_instrument_rad = degrees_to_radians(beta_instrument_deg)
    return math.sqrt(beta_measured_rad**2 - beta_instrument_rad**2)


def crystallite_size_nm(
    two_theta_deg: float,
    beta_measured_deg: float,
    beta_instrument_deg: float,
    wavelength_nm: float = CU_K_ALPHA_NM,
    shape_factor: float = 0.9,
) -> float:
    """Compute crystallite size (nm) using the Scherrer equation.

    D = K*lambda / (beta*cos(theta))
    where theta is half of 2theta.
    """
    theta_rad = degrees_to_radians(two_theta_deg / 2.0)
    beta_rad = corrected_fwhm_radians(beta_measured_deg, beta_instrument_deg)

    cos_theta = math.cos(theta_rad)
    if cos_theta == 0:
        raise ValueError("Invalid 2θ value: cos(theta) is zero.")

    return (shape_factor * wavelength_nm) / (beta_rad * cos_theta)


def d_spacing_nm(two_theta_deg: float, wavelength_nm: float = CU_K_ALPHA_NM) -> float:
    """Compute d-spacing in nm from Bragg's law for first-order diffraction."""
    theta_rad = degrees_to_radians(two_theta_deg / 2.0)
    sin_theta = math.sin(theta_rad)
    if sin_theta == 0:
        raise ValueError("Invalid 2θ value: sin(theta) is zero.")
    return wavelength_nm / (2.0 * sin_theta)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="XRD (100) calculator")
    parser.add_argument("--two-theta", type=float, required=True, help="Peak position 2θ in degrees")
    parser.add_argument("--beta-measured", type=float, required=True, help="Measured FWHM (degrees)")
    parser.add_argument("--beta-instrument", type=float, default=0.0, help="Instrument FWHM (degrees)")
    parser.add_argument("--wavelength", type=float, default=CU_K_ALPHA_NM, help="Wavelength in nm")
    parser.add_argument("--shape-factor", type=float, default=0.9, help="Scherrer shape factor K")
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    size_nm = crystallite_size_nm(
        two_theta_deg=args.two_theta,
        beta_measured_deg=args.beta_measured,
        beta_instrument_deg=args.beta_instrument,
        wavelength_nm=args.wavelength,
        shape_factor=args.shape_factor,
    )
    d100_nm = d_spacing_nm(two_theta_deg=args.two_theta, wavelength_nm=args.wavelength)

    print(f"Crystallite size D(100): {size_nm:.4f} nm")
    print(f"d(100) spacing: {d100_nm:.4f} nm")


if __name__ == "__main__":
    main()
