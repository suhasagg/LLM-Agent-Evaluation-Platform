import uuid
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from prometheus_client import Counter,Histogram,make_asgi_app
from .database import init_db,get_db
from .models import EvaluationRun
from .contracts import EvalRequest
from .engine import evaluate
from .telemetry import tracer

app=FastAPI(title="LLM / Agent Evaluation Platform",version="1.0.0")
app.mount("/metrics",make_asgi_app())
RUNS=Counter("evaluation_runs_total","Evaluation runs",["result"])
SCORE=Histogram("evaluation_score","Evaluation aggregate scores")

@app.on_event("startup")
async def startup():await init_db()

@app.get("/health")
async def health():return {"status":"ok"}

@app.post("/v1/evaluations")
async def run(req:EvalRequest,db:AsyncSession=Depends(get_db)):
    eid="eval-"+uuid.uuid4().hex[:12]
    record=EvaluationRun(id=eid,dataset=req.dataset,status="RUNNING");db.add(record);await db.commit()
    try:
        with tracer.start_as_current_span("evaluation.run") as span:
            report=await evaluate(req)
            span.set_attribute("eval.dataset",req.dataset);span.set_attribute("eval.score",report["score"])
        record.report=report;record.score=report["score"]
        record.status="PASSED" if report["gate_passed"] else "FAILED_GATE"
        RUNS.labels("pass" if report["gate_passed"] else "fail").inc();SCORE.observe(report["score"])
        await db.commit()
        return {"evaluation_id":eid,"status":record.status,"report":report}
    except Exception as e:
        record.status="ERROR";record.report={"error":str(e)[:1000]};await db.commit();raise

@app.get("/v1/evaluations/{eid}")
async def get(eid:str,db:AsyncSession=Depends(get_db)):
    x=await db.get(EvaluationRun,eid)
    if not x:raise HTTPException(404,"evaluation not found")
    return {"evaluation_id":x.id,"status":x.status,"score":x.score,"report":x.report}
