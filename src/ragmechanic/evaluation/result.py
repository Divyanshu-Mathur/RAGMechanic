from dataclasses import dataclass

@dataclass
class EvaluationResult:

    faithfulness: float

    answer_relevancy: float

    hallucination: float | None = None