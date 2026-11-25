"""
Model-based FEVER baseline agent.
"""

import json
import re
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)


LABELS = {
    "SUPPORTS",
    "REFUTES",
    "NOT ENOUGH INFO"
}


class ModelReActAgent:

    def __init__(
        self,
        model_name="microsoft/Phi-3-mini-4k-instruct",
        device=None
    ):

        self.device = (
            device
            if device is not None
            else (
                "cuda"
                if torch.cuda.is_available()
                else "cpu"
            )
        )

        print("Loading model:", model_name)

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name
        )

        self.model = (
            AutoModelForCausalLM
            .from_pretrained(model_name)
            .to(self.device)
        )

        prompt_path = (
            "src/prompts/react_prompt.txt"
        )

        with open(
            prompt_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.prompt_template = file.read()

    def build_prompt(
        self,
        claim,
        evidence_text
    ):

        return self.prompt_template.format(
            claim=claim,
            evidence=evidence_text
        )

    import re


    def extract_label(
         self,
         text
):

        matches = re.findall(
        r"\b(SUPPORTS|REFUTES|NOT ENOUGH INFO)\b",
        text.upper()
    )

        if matches:
            return matches[-1]

        return "NOT ENOUGH INFO"

    def predict(
        self,
        claim,
        evidence_text,
        max_new_tokens=32
    ):

        prompt = self.build_prompt(
            claim,
            evidence_text
        )

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        ).to(self.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False
        )

        response = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        label = self.extract_label(
            response
        )

        return {
            "prediction": label,
            "response": response
        }