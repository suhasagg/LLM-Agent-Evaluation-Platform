import json
from pathlib import Path
def load(name:str):
    safe="".join(c for c in name if c.isalnum() or c in "-_")
    candidates=[Path("/datasets")/f"{safe}.json",Path(__file__).parents[1]/"datasets"/f"{safe}.json"]
    for p in candidates:
        if p.exists():return json.loads(p.read_text())
    raise FileNotFoundError(name)
