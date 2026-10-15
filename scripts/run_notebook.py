"""Execute a notebook in place from the command line (works where the `jupyter` command is not on PATH).

    python scripts/run_notebook.py Topic_6_Advanced_Analysis_and_Model_Refinement.ipynb

Run from the repository root; takes about 10 minutes for the capstone notebook (nested cross-validation).
"""
import sys, time, nbformat
from nbconvert.preprocessors import ExecutePreprocessor
P = sys.argv[1]
nb = nbformat.read(P, as_version=4)
t0 = time.time()
ep = ExecutePreprocessor(timeout=7200, kernel_name="python3")
try:
    ep.preprocess(nb, {"metadata": {"path": "."}})
    status = "OK"
except Exception as e:
    status = "FAILED: " + str(e)[:3000]
nbformat.write(nb, P)
print(status, f"{time.time()-t0:.0f}s")
sys.exit(0 if status == "OK" else 1)
