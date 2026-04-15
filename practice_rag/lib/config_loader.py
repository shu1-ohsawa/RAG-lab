import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

import yaml

def load_config(config_path="config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    # HF_HOMEなどの環境変数をここでセット
    os.environ["HF_HOME"] = config["paths"]["hf_cache"]
    return config