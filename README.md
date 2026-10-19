# ReAct-Recovery-Controller
A research project investigating whether explicit recovery-action selection improves ReAct agent robustness under unproductive retrieval conditions.

ReAct Recovery Controller
Overview
This project investigates whether explicit recovery-action selection can improve the robustness of ReAct agents when retrieval results are unproductive, incomplete, or otherwise unhelpful.

Rather than introducing a broad observation-quality framework, this project focuses on a single research question:

Can explicit recovery-action selection improve ReAct's ability to recover from unproductive retrieval results?

The project compares a baseline ReAct agent against a modified ReAct architecture that introduces a Recovery Action Controller after retrieval steps.

Research Motivation
The ReAct framework combines reasoning and acting by interleaving thoughts, actions, and observations.

However, retrieval failures can produce trajectories where agents repeatedly issue ineffective searches, continue reasoning from weak evidence, or fail to recover from uninformative observations.

This project investigates whether explicitly selecting recovery actions can improve robustness and retrieval efficiency.

Baseline Architecture
Question ↓ Thought ↓ Action ↓ Observation ↓ Thought ↓ Finish

Proposed Architecture
Question ↓ Thought ↓ Action ↓ Observation ↓ Recovery Action Controller ↓ Continue | Retry | Reformulate | Finish

Research Questions
Can recovery-action selection improve task accuracy?
Can recovery-action selection improve recovery after unproductive retrieval?
Does the controller reduce repeated ineffective actions?
What impact does the controller have on cost, latency, and retrieval efficiency?
Dataset
Primary Benchmark:

FEVER
Potential Secondary Benchmark:

HotpotQA
Evaluation Metrics
Accuracy
Recovery Rate
Retrieval Success Rate
Tool Calls
Latency
Token Usage
Repository Structure
data/ notebooks/ src/ results/ experiments/ docs/ papers/

Project Status
Phase 1: Environment Setup

Configure GPU environment
Download FEVER subset
Select model
Implement baseline ReAct
Collect trajectories
Build Recovery Action Controller
Run experiments
Analyze results
Write final paper
