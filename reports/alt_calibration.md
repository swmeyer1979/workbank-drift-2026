# Alternative calibration methods - LOOCV comparison

Compare leave-one-out cross-validation MAE and binary >=3 agreement for several mappings from ensemble-raw to consensus-target.

| method | LOOCV MAE | LOOCV bin >=3 agreement |
|---|---:|---:|
| raw_identity | 0.310 | 94% |
| linear_clip | 0.401 | 94% |
| linear_round | 0.350 | 90% |
| isotonic | 0.401 | 90% |

## Reading guide

- `raw_identity`: no calibration; ensemble median used directly.
- `linear_clip`: linear regression of consensus on ensemble, clipped to [1,5].
- `linear_round`: same, then rounded to integer.
- `isotonic`: monotonic mapping, fit per `drift.calibrate`.

## Verdict

Binary >=3 agreement remains 94% for raw, linear, and rounded-linear mappings. Isotonic underperforms on the zone-relevant binary metric in leave-one-out validation.

**Decision:** ship raw ensemble median. Calibration mapping does not improve zone agreement on this calibration set.
