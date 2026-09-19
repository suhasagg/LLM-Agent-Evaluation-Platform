# Architecture

## Separate target execution from grading
Targets generate outputs. Graders consume immutable captured outputs. This permits re-grading without paying to rerun the target.

## Multi-dimensional evaluation
Keep correctness, relevance, groundedness, tool behavior, latency and cost separate. Aggregate scores are useful for gates but should never erase raw dimensions.

## Deterministic before probabilistic
Exact constraints, JSON schema, required tools, forbidden strings, latency and token budgets should use deterministic code. Use LLM judges for semantic properties.

## Baselines
A candidate should be compared against a pinned baseline on the same dataset. Pairwise judging reduces some absolute-score calibration problems.

## Agent evaluation
Evaluate the trajectory, not only final text: tool selection, arguments, tool errors, handoffs, approvals, loops and cost.

## Trace integration
OpenAI Agents SDK traces generations, tools, handoffs and guardrails. A production ingestion adapter can correlate those traces with experiment/run ids.
