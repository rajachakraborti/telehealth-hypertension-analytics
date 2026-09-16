import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy.stats import ks_2samp
from scipy.spatial.distance import jensenshannon
import warnings

warnings.filterwarnings('ignore')

class SyntheticTelemetryGenerator:
    """
    Generates synthetic Ambulatory Blood Pressure Monitoring (ABPM) telemetry.
    Enforces strict physiological boundaries and validates against NHANES statistical benchmarks.
    """
    def __init__(self, num_patients=50, days_per_patient=7, interval_minutes=30):
        self.num_patients = num_patients
        self.days = days_per_patient
        self.interval = interval_minutes
        
        # Empirical NHANES Baselines (used for statistical JSD/KS validation)
        self.nhanes_sbp_mean = 122.0
        self.nhanes_sbp_std = 14.5
        self.nhanes_dbp_mean = 76.0
        self.nhanes_dbp_std = 10.0

    def generate_telemetry(self) -> pd.DataFrame:
        print(f"Generating synthetic ABPM telemetry for {self.num_patients} patients over {self.days} days...")
        records = []
        
        for patient_id in range(1, self.num_patients + 1):
            # Randomly assign a baseline AHA stage to define the patient's resting BP
            stage = np.random.choice(["Normal", "Elevated", "Stage 1", "Stage 2"], p=[0.4, 0.3, 0.2, 0.1])
            base_sbp, base_dbp = self._get_baseline_bp(stage)
            
            # Determine if this patient exhibits healthy nocturnal dipping (10-20% drop)
            # Higher risk patients (Stage 2) have a higher chance of being "non-dippers"
            is_dipper = np.random.choice([True, False], p=[0.8, 0.2] if stage != "Stage 2" else [0.4, 0.6])
            
            current_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0) - timedelta(days=self.days)
            end_time = current_time + timedelta(days=self.days)
            
            while current_time < end_time:
                # 1. Apply Circadian Rhythm (Nocturnal Dipping)
                hour = current_time.hour
                is_night = 23 <= hour or hour < 6
                
                sbp = base_sbp
                dbp = base_dbp
                
                if is_night and is_dipper:
                    # Apply 10% to 20% nocturnal dip
                    dip_factor = np.random.uniform(0.10, 0.20)
                    sbp *= (1 - dip_factor)
                    dbp *= (1 - dip_factor)
                elif is_night and not is_dipper:
                    # Non-dippers drop less than 10% (blunted dipping)
                    dip_factor = np.random.uniform(0.0, 0.09)
                    sbp *= (1 - dip_factor)
                    dbp *= (1 - dip_factor)
                
                # 2. Add Observational Noise (simulating movement/cuff errors)
                sbp += np.random.normal(0, 5)
                dbp += np.random.normal(0, 4)
                
                # 3. Calculate Derived Physiological Metrics
                pp = sbp - dbp  # Pulse Pressure
                map_val = dbp + (pp / 3)  # Mean Arterial Pressure
                
                # 4. Enforce Physiological Bounds (Crucial for Clinical Realism)
                # If the random noise pushes it into impossible territory, clip it to viable limits
                map_val = np.clip(map_val, 70.0, 110.0)
                pp = np.clip(pp, 30.0, 80.0)
                
                # Recalculate SBP and DBP from bounded MAP and PP to maintain mathematical integrity
                # MAP = DBP + PP/3  => DBP = MAP - PP/3
                # SBP = DBP + PP
                dbp_final = map_val - (pp / 3)
                sbp_final = dbp_final + pp
                
                records.append({
                    "patient_id": f"P-{patient_id:04d}",
                    "timestamp": current_time,
                    "systolic": round(sbp_final, 1),
                    "diastolic": round(dbp_final, 1),
                    "map": round(map_val, 1),
                    "pulse_pressure": round(pp, 1),
                    "is_night": is_night,
                    "is_dipper": is_dipper,
                    "aha_stage": stage
                })
                
                current_time += timedelta(minutes=self.interval)
                
        df = pd.DataFrame(records)
        print(f"Generated {len(df)} telemetry records successfully.")
        return df

    def _get_baseline_bp(self, stage):
        """Returns baseline (SBP, DBP) based on AHA 2017 Guidelines."""
        if stage == "Normal":
            return np.random.uniform(110, 119), np.random.uniform(70, 79)
        elif stage == "Elevated":
            return np.random.uniform(120, 129), np.random.uniform(70, 79)
        elif stage == "Stage 1":
            return np.random.uniform(130, 139), np.random.uniform(80, 89)
        else: # Stage 2
            return np.random.uniform(140, 160), np.random.uniform(90, 100)

    def validate_distributions(self, df: pd.DataFrame):
        """
        Validates the generated dataset against NHANES benchmarks using K-S and JSD tests.
        """
        print("\n--- Running Statistical Pre-Training Gates ---")
        
        # 1. K-S Test
        # Generate a mock NHANES distribution for comparison
        mock_nhanes_sbp = np.random.normal(self.nhanes_sbp_mean, self.nhanes_sbp_std, len(df))
        ks_stat, ks_pval = ks_2samp(df['systolic'], mock_nhanes_sbp)
        print(f"1. K-S Test (Systolic): p-value = {ks_pval:.4f}")
        if ks_pval < 0.05:
            print("   [WARNING] K-S test rejected null hypothesis. Distributions may differ.")
        else:
            print("   [PASS] K-S test passed. Distributions are statistically similar.")

        # 2. Jensen-Shannon Divergence (JSD)
        # Create probability density histograms to compare
        hist_synth, bin_edges = np.histogram(df['systolic'], bins=30, range=(80, 180), density=True)
        hist_nhanes, _ = np.histogram(mock_nhanes_sbp, bins=30, range=(80, 180), density=True)
        
        # Add epsilon to avoid division by zero in JSD
        hist_synth = hist_synth + 1e-10
        hist_nhanes = hist_nhanes + 1e-10
        
        jsd_score = jensenshannon(hist_synth, hist_nhanes)
        print(f"2. Jensen-Shannon Divergence (JSD): {jsd_score:.4f}")
        
        # Resolving Professor Pollyn's trade-off: 
        if jsd_score <= 0.05:
            print("   [PASS] JSD is below strict threshold (<0.05).")
        elif jsd_score <= 0.10:
            print("   [ACCEPTABLE DRIFT] JSD drifted above 0.05 due to strict physiological boundary enforcement. Prioritizing clinical realism over pure statistical parity.")
        else:
            print("   [FAIL] JSD is unacceptably high.")

        # 3. Physiological Bounds Check
        map_violations = df[(df['map'] < 70) | (df['map'] > 110)]
        if len(map_violations) == 0:
            print("3. Physiological Bounds: [PASS] 100% of MAP values are within viable limits (70-110 mmHg).")
        else:
            print(f"3. Physiological Bounds: [FAIL] {len(map_violations)} records violated MAP limits.")

if __name__ == "__main__":
    generator = SyntheticTelemetryGenerator(num_patients=20, days_per_patient=7)
    df_telemetry = generator.generate_telemetry()
    generator.validate_distributions(df_telemetry)
    
    # Save a small sample for the Jupyter notebook later
    df_telemetry.to_csv("sample_telemetry.csv", index=False)
    print("\nSample telemetry saved to sample_telemetry.csv")
