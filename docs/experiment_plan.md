# ReAct Recovery Experiment Plan

## Working Title

Diagnosing and Improving ReAct Recovery After Unproductive Searches

## Observed Problem

A ReAct agent may encounter an unproductive search result, recognize that the result does not provide the required evidence, but still select an ineffective next action.

## Research Question

Can explicit query reformulation improve ReAct's recovery from unproductive searches without interfering with cases where standard ReAct would recover naturally?

## Primary Hypothesis

Some ReAct failures after unproductive observations result from inconsistent recovery-action selection. The agent may recognize insufficient progress but fail to produce a meaningfully different search query.

## Alternative Hypothesis

The failures may primarily result from limitations in the retrieval environment. If useful evidence is unavailable, query reformulation may not improve performance.

## Experimental Conditions

### Condition A: Standard ReAct

The agent receives the observation and chooses its next action without intervention.

### Condition B: Detection Only

The agent is informed that the previous result did not satisfy the current evidence need, but independently chooses the next action.

### Condition C: Enforced Reformulation

The agent is informed that the previous result was unproductive and must issue a meaningfully different search query.

## Initial Dataset

A small FEVER pilot containing:

- SUPPORTS cases
- REFUTES cases
- NOT ENOUGH INFO cases

## Validation Size

Three cases, one from each FEVER category.

## Pilot Size

Twenty to thirty cases after pipeline validation.

## Initial Metrics

- Final-answer accuracy
- Task-completion rate
- Successful-recovery rate
- Repeated-query rate
- Effective-reformulation rate
- Premature-stopping rate
- Unsupported-answer rate
- Average tool calls
- Average trajectory length
- Runtime

## Initial Scope Limitations

The first experiment will not implement:

- Contradiction suppression
- Broad evidence-quality scoring
- Cross-check control
- Adaptive token budgeting
- Full hypothesis revision
- Multiple recovery decisions
- Model fine-tuning
