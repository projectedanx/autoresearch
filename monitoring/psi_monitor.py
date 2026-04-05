# D5: monitoring/psi_monitor.py
# RULE R11 implementation — Covariate shift detection

from dataclasses import dataclass
from typing import Optional
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

PSI_THRESHOLD_WARN = 0.10   # Yellow alert
PSI_THRESHOLD_PAGE = 0.20   # PagerDuty trigger — Scar SCA-0201


@dataclass
class PSIResult:
    feature_name: str
    psi_score: float
    status: str  # "OK" | "WARN" | "ALERT"
    baseline_distribution: list
    current_distribution: list


def compute_psi(
    baseline: pd.Series,
    current: pd.Series,
    buckets: int = 10,
) -> float:
    """
    Population Stability Index.
    PSI = Σ (actual% - expected%) × ln(actual% / expected%)
    """
    baseline_pct, bin_edges = np.histogram(
        baseline, bins=buckets, density=False)
    current_pct, _ = np.histogram(current, bins=bin_edges, density=False)

    baseline_pct = np.where(
        baseline_pct == 0, 0.0001, baseline_pct / len(baseline))
    current_pct = np.where(
        current_pct == 0, 0.0001, current_pct / len(current))

    psi = np.sum(
        (current_pct - baseline_pct) * np.log(current_pct / baseline_pct))
    return float(psi)


def run_monitoring_check(
    baseline_df: pd.DataFrame,
    current_df: pd.DataFrame,
    feature_columns: list[str],
    alert_callback: Optional[callable] = None,
) -> list[PSIResult]:
    results = []

    for col in feature_columns:
        psi = compute_psi(baseline_df[col].dropna(), current_df[col].dropna())

        if psi >= PSI_THRESHOLD_PAGE:
            status = "ALERT"
            logger.error(
                f"[PSI_ALERT] Feature '{col}': PSI={psi:.4f} ≥ "
                f"{PSI_THRESHOLD_PAGE}. Covariate shift detected. "
                f"[SCA-0201 — FIPI active]"
            )
            if alert_callback:
                alert_callback(
                    feature=col, psi=psi, threshold=PSI_THRESHOLD_PAGE)
        elif psi >= PSI_THRESHOLD_WARN:
            status = "WARN"
            logger.warning(f"[PSI_WARN] Feature '{col}': PSI={psi:.4f} "
                           f"approaching threshold.")
        else:
            status = "OK"
            logger.info(f"[PSI_OK] Feature '{col}': PSI={psi:.4f}")

        results.append(PSIResult(
            feature_name=col,
            psi_score=psi,
            status=status,
            baseline_distribution=baseline_df[col].describe().to_dict(),
            current_distribution=current_df[col].describe().to_dict(),
        ))

    return results
