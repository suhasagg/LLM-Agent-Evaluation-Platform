import asyncio
from .datasets import load
from .targets import run_target
from .graders import deterministic,semantic,compare,rag_checks,agent_checks

async def evaluate(req):
    dataset=load(req.dataset)
    rows=[]
    for case in dataset["cases"]:
        candidate=await run_target(req.candidate,case)
        det=deterministic(case,candidate)
        sem=await semantic(case,candidate)
        row={"case_id":case["id"],"candidate":candidate,"deterministic":det,
             "judge":sem,"rag":rag_checks(case,candidate),
             "agent":agent_checks(case,candidate) if req.candidate.kind=="agent" else None}
        if req.baseline:
            base=await run_target(req.baseline,case)
            row["baseline"]=base
            row["pairwise"]=await compare(case,candidate,base)
        row["score"]=(det["score"]+sem["correctness"]+sem["relevance"]+sem["groundedness"])/4
        rows.append(row)
    score=sum(x["score"] for x in rows)/len(rows) if rows else 0
    baseline_losses=sum(1 for x in rows if x.get("pairwise",{}).get("winner")=="baseline")
    regression=baseline_losses/len(rows) if rows else 0
    passed=score>=req.gate.min_score and regression<=req.gate.max_regression
    return {"dataset":dataset["name"],"dataset_version":dataset["version"],"score":score,
      "regression_rate":regression,"gate_passed":passed,"cases":rows}
