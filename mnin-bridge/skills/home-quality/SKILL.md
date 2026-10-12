---
name: mnin-home-quality
description: Audit the official MNIN NBDA Home reference, assets and genuine responsive browser screenshots without regeneration or WordPress modifications.
---

# MNIN NBDA Home quality workflow

**Official source of truth:** the last user-approved Home V1.0 PNG as an immutable binary.
Do not treat a generated picture, an upscale or a text reconstruction as pixel-identical.

## Stages

1. Confirm original asset file path, bytes, width/height and SHA-256 in a private location.
2. Enumerate original logo, Amine, mission parchment, 1AC/2AC/3AC cards, icons and sunset asset sources.
3. Calculate intrinsic raster sizes; flag logo/icon sources that cannot render crisply at the required CSS pixel size and device pixel ratio. Prefer original vectors for vector art; do not claim upscaled raster becomes native 8K.
4. Compare static HTML/CSS composition with the official reference. Record discrepancies without rewriting approved illustration.
5. Render full page and viewport captures in a **real browser** on agreed desktop, laptop, tablet and smartphone sizes.
6. Check overflow, broken images, layout clipping, heading and CTA visibility, keyboard, reduced motion, FR/AR RTL.
7. Check performance separately from screenshots. Never declare LCP/INP/CLS PASS without measurements.
8. Produce a mission report with SHA-256, viewport, actual screenshots, exceptions, evidence, and owner sign-off.
9. Only after static Home PASS plan opt-in 3D Amine / line-of-progress prototype, reversible and visually faithful at rest.

No WordPress staging/production change, no deployment, no paid APIs without explicit approval.
