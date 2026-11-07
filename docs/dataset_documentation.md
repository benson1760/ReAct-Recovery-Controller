Dataset Documentation
Primary Dataset
FEVER v1.0

Fact Extraction and VERification Dataset

Dataset Purpose
The FEVER dataset is used to evaluate fact verification systems.

Claims are classified into:

SUPPORTS
REFUTES
NOT ENOUGH INFO
Source Data
Official FEVER development split:

shared_task_dev.jsonl

Source Statistics
Total records: 19,998

Label distribution:

SUPPORTS: 6,666
REFUTES: 6,666
NOT ENOUGH INFO: 6,666
Pilot Dataset
File:

data/samples/fever_pilot_30.json

Sampling Procedure
A balanced pilot subset was generated using:

scripts/prepare_fever_pilot.py

Random seed: 42

Pilot Composition
Total claims: 30

SUPPORTS: 10
REFUTES: 10
NOT ENOUGH INFO: 10
Evidence Coverage Analysis
The pilot contains:

20 claims with evidence references
10 claims without evidence references
42 unique evidence references
22 unique Wikipedia pages
Validation Dataset
The project also contains:

data/samples/fever_validation.json

This file contains synthetic software-validation fixtures used to test pipeline functionality.

These validation fixtures are not official FEVER benchmark examples and are not used for experimental evaluation.

Reproducibility
The pilot dataset can be regenerated using:

scripts/prepare_fever_pilot.py

Sampling metadata is stored in:

data/processed/fever/fever_pilot_30_metadata.json