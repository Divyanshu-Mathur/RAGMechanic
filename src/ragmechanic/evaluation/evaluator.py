from deepeval.metrics import HallucinationMetric,AnswerRelevancyMetric,FaithfulnessMetric
from deepeval.test_case import LLMTestCase

from .result import EvaluationResult
from deepeval.models import GeminiModel
from os import getenv

class Evaluator:

    def __init__(self,llm,embeddings,):
        self.llm = llm
        self.embeddings = embeddings
        
        

    def evaluate(self,question,answer,contexts,):

        # dataset = EvaluationDataset.from_list(
        #     [
        #         {
        #             "user_input": question,
        #             "response": answer,
        #             "retrieved_contexts": contexts,
        #         }
        #     ]
        # )

        # scores = evaluate(
        #     dataset,
        #     metrics=[
        #         Faithfulness(),
        #         ResponseRelevancy(),
        #     ],
        #     llm=LangchainLLMWrapper(self.llm),
        #     embeddings=LangchainEmbeddingsWrapper(self.embeddings),
        # )

        # score = scores.to_pandas().iloc[0]
        
        gemini = gemini = GeminiModel(
                model="gemini-3.5-flash-lite",
                api_key=getenv("GOOGLE_API_KEY") or getenv("GEMINI_API_KEY"),
            )
        
        hallucination_metric = HallucinationMetric(threshold=0.5,model=gemini,)
        
        answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.7,model=gemini)
        
        faithfulness_metric = FaithfulnessMetric(threshold=0.7,model=gemini)
        
        test_case = LLMTestCase(
            input=question,
            actual_output=answer,
            context=contexts,
            retrieval_context=contexts,
        )
        
        hallucination_metric.measure(test_case)
        answer_relevancy_metric.measure(test_case)
        faithfulness_metric.measure(test_case)
        

        return EvaluationResult(
            faithfulness=float(faithfulness_metric.score),
            answer_relevancy=float(answer_relevancy_metric.score),
            hallucination=float(hallucination_metric.score),
        )