"""Launch only the limited C++ leaf audit; never invokes the historical census main."""
from audit_core import OUT
import subprocess
if __name__=='__main__':
    subprocess.run([str(OUT/'leaf_fiber_audit.exe')],cwd=OUT,check=True)
