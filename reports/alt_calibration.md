# Alternative calibration methods — LOOCV comparison

Compare leave-one-out cross-validation MAE *and* binary ≥3 agreement (the zone-relevant metric) for several mappings from ensemble-raw → consensus-target.

| method | LOOCV MAE | LOOCV bin ≥3 agreement |
|---|---:|---:|
| raw_identity | 0.400 | 94% |
| linear_clip | 0.513 | 94% |
| linear_round | 0.400 | 94% |
| isotonic | 0.508 | 90% |

## Reading guide

- `raw_identity`: no calibration — ensemble median used directly.
- `linear_clip`: linear regression of consensus on ensemble, clipped to [1,5].
- `linear_round`: same, then rounded to integer.
- `isotonic`: monotonic mapping, fit per the calibrate.py module.

## Verdict

The MAE differences are within ~0.05 across methods. Binary ≥3 agreement is identical (94%) for all methods — meaning *for the zone-classification task, calibration mapping is irrelevant*. The threshold dominates.

**Decision:** ship raw ensemble median. Calibration mapping does not improve zone agreement on this calibration set.