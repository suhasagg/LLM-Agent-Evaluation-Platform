from pydantic import BaseModel,Field
from typing import Literal
class Target(BaseModel):
    kind:Literal["responses","agent"]
    model:str
class Gate(BaseModel):
    min_score:float=Field(default=.75,ge=0,le=1)
    max_regression:float=Field(default=.05,ge=0,le=1)
class EvalRequest(BaseModel):
    dataset:str
    candidate:Target
    baseline:Target|None=None
    gate:Gate=Gate()
class JudgeScore(BaseModel):
    correctness:float=Field(ge=0,le=1)
    relevance:float=Field(ge=0,le=1)
    groundedness:float=Field(ge=0,le=1)
    reason:str
class Pairwise(BaseModel):
    winner:Literal["candidate","baseline","tie"]
    confidence:float=Field(ge=0,le=1)
    reason:str
