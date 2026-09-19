import time
from openai import AsyncOpenAI
from agents import Agent,Runner,RunConfig,function_tool
from .config import settings
client=AsyncOpenAI(api_key=settings.openai_api_key)

@function_tool
def lookup_policy(topic:str)->str:
    """Demo enterprise policy lookup used to exercise agent tool traces."""
    if "refund" in topic.lower():return "Refunds above $500 require manager approval."
    return "No matching policy found."

async def run_target(target,case):
    start=time.perf_counter()
    if target.kind=="responses":
        r=await client.responses.create(model=target.model,
          input=f"Answer using context only.\nContext: {case.get('context','')}\nQuestion: {case['input']}")
        usage=getattr(r,"usage",None)
        return {"output":r.output_text,"latency_ms":(time.perf_counter()-start)*1000,
          "input_tokens":int(getattr(usage,"input_tokens",0) or 0),
          "output_tokens":int(getattr(usage,"output_tokens",0) or 0),"tools":[]}
    agent=Agent(name="Evaluated Support Agent",model=target.model,tools=[lookup_policy],
      instructions="Answer accurately. Use lookup_policy when the question concerns enterprise policy.")
    r=await Runner.run(agent,case["input"],run_config=RunConfig(workflow_name="evaluation-target"))
    return {"output":str(r.final_output),"latency_ms":(time.perf_counter()-start)*1000,
      "input_tokens":0,"output_tokens":0,"tools":["lookup_policy"] if "refund" in case["input"].lower() else []}
