import json,re
from agents import Agent,Runner
from .contracts import JudgeScore,Pairwise
from .config import settings

judge=Agent(name="Evaluation Judge",model=settings.judge_model,output_type=JudgeScore,
 instructions="""Score the response against question, reference and context.
correctness: matches reference facts.
relevance: directly addresses question.
groundedness: claims are supported by context.
Use 0..1. Do not reward unsupported detail.""")

pairwise=Agent(name="Blind Pairwise Judge",model=settings.judge_model,output_type=Pairwise,
 instructions="""Compare response A and B for correctness, relevance and groundedness.
A is candidate and B is baseline. Prefer tie when materially equivalent.""")

def deterministic(case,result):
    text=result["output"].lower()
    req=all(x.lower() in text for x in case.get("required_terms",[]))
    forbidden=all(x.lower() not in text for x in case.get("forbidden_terms",[]))
    return {"required_terms":req,"forbidden_terms":forbidden,
            "latency_under_30s":result["latency_ms"]<30000,
            "score":sum([req,forbidden,result["latency_ms"]<30000])/3}

async def semantic(case,result):
    prompt=json.dumps({"question":case["input"],"reference":case.get("reference",""),
      "context":case.get("context",""),"response":result["output"]})
    r=await Runner.run(judge,prompt);return r.final_output.model_dump()

async def compare(case,a,b):
    r=await Runner.run(pairwise,json.dumps({"question":case["input"],"reference":case.get("reference",""),
      "context":case.get("context",""),"A":a["output"],"B":b["output"]}))
    return r.final_output.model_dump()

def rag_checks(case,result):
    context=case.get("context","").lower()
    output=result["output"].lower()
    # Deterministic lexical support proxy; semantic groundedness comes from judge.
    terms=[x for x in re.findall(r"[a-z0-9$]+",output) if len(x)>5]
    overlap=sum(1 for x in set(terms) if x in context)
    return {"long_term_context_overlap":overlap}

def agent_checks(case,result):
    expected="lookup_policy" if "refund" in case["input"].lower() else None
    return {"required_tool":expected,"tool_used":expected in result.get("tools",[]) if expected else True}
