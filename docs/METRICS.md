# Metrics

LLM:
- exact/contains/schema success
- semantic correctness
- relevance
- safety
- latency
- input/output tokens
- estimated cost

RAG:
- retrieval Recall@K / nDCG
- context relevance
- groundedness
- citation precision/recall
- answer correctness

Agents:
- task success
- required-tool recall
- unnecessary-tool rate
- tool argument correctness
- tool failure rate
- handoff correctness
- number of turns
- loop/runaway rate
- approval-policy compliance
- total latency/cost

Judge quality:
- agreement with human labels
- confusion matrix
- inter-judge agreement
- position/order bias
- verbosity bias
- score drift by judge-model version
