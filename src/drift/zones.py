"""Zone classification — locked to the upstream paper's 3.0 cutoff on 1-5 Likert mean."""

from __future__ import annotations

from typing import Literal

Zone = Literal["Green Light", "Red Light", "R&D Opportunity", "Low Priority"]

CUTOFF = 3.0


def zone_of(capacity_mean: float, desire_mean: float) -> Zone:
    """Returns the upstream zone for a (capacity, desire) mean pair.

    Boundary is inclusive on the high side, matching
    `analysis/automation_viability.ipynb` in SALT-NLP/workbank.
    """
    hi_cap = capacity_mean >= CUTOFF
    hi_des = desire_mean >= CUTOFF
    if hi_cap and hi_des:
        return "Green Light"
    if hi_cap and not hi_des:
        return "Red Light"
    if not hi_cap and hi_des:
        return "R&D Opportunity"
    return "Low Priority"


def migration_label(z_old: Zone, z_new: Zone) -> str:
    short = {
        "Green Light": "Green",
        "Red Light": "Red",
        "R&D Opportunity": "R&D",
        "Low Priority": "Low",
    }
    return f"{short[z_old]}->{short[z_new]}"
