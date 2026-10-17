from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_xai import ChatXAI
from langchain_anthropic import ChatAnthropic
from langchain_mistralai import ChatMistralAI


class LLMManager:

    def __init__(
        self,
        provider: str,
        model: str,
        temperature: float = 0,
        api_key: str | None = None,
    ):
        self.provider = provider.lower().strip()

        if not model or not model.strip():
            raise ValueError("Model name cannot be empty.")

        if self.provider in {"gemini", "google", "google_genai"}:
            self.provider = "gemini"

            try:
                self.llm = ChatGoogleGenerativeAI(
                    model=model,
                    temperature=temperature,
                    google_api_key=api_key,
                )
            except Exception as e:
                raise RuntimeError(
                    f"Failed to initialize Gemini model '{model}': {e}"
                ) from e

        elif self.provider in {"openai", "gpt"}:
            self.provider = "openai"

            try:
                self.llm = ChatOpenAI(
                    model=model,
                    temperature=temperature,
                    api_key=api_key,
                )
            except Exception as e:
                raise RuntimeError(
                    f"Failed to initialize OpenAI model '{model}': {e}"
                ) from e

        elif self.provider in {"grok", "xai"}:
            self.provider = "grok"

            try:
                self.llm = ChatXAI(
                    model=model,
                    temperature=temperature,
                    xai_api_key=api_key,
                )
            except Exception as e:
                raise RuntimeError(
                    f"Failed to initialize Grok model '{model}': {e}"
                ) from e

        elif self.provider in {"anthropic", "claude"}:
            self.provider = "anthropic"

            try:
                self.llm = ChatAnthropic(
                    model=model,
                    temperature=temperature,
                    anthropic_api_key=api_key,
                )
            except Exception as e:
                raise RuntimeError(
                    f"Failed to initialize Anthropic model '{model}': {e}"
                ) from e

        elif self.provider in {"mistral", "mistralai"}:
            self.provider = "mistral"

            try:
                self.llm = ChatMistralAI(
                    model=model,
                    temperature=temperature,
                    mistral_api_key=api_key,
                )
            except Exception as e:
                raise RuntimeError(
                    f"Failed to initialize Mistral model '{model}': {e}"
                ) from e

        else:
            raise ValueError(
                f"Unsupported provider: '{provider}'. "
                f"Supported providers: "
                f"openai, gemini, grok, anthropic, mistral."
            )

    def invoke(self, prompt: str):
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        try:
            return self.llm.invoke(prompt)

        except Exception as e:
            error_message = str(e).lower()

            if any(
                keyword in error_message
                for keyword in [
                    "api key",
                    "apikey",
                    "authentication",
                    "unauthorized",
                    "invalid api",
                    "invalid_api_key",
                ]
            ):
                raise RuntimeError(
                    f"{self.provider} API authentication failed. "
                    f"Please check your API key."
                ) from e

            if any(
                keyword in error_message
                for keyword in [
                    "rate limit",
                    "ratelimit",
                    "too many requests",
                    "429",
                ]
            ):
                raise RuntimeError(
                    f"{self.provider} API rate limit exceeded. "
                    f"Please try again later."
                ) from e

            if any(
                keyword in error_message
                for keyword in [
                    "timeout",
                    "timed out",
                    "connection",
                    "connecterror",
                    "network",
                ]
            ):
                raise RuntimeError(
                    f"Unable to connect to {self.provider} API. "
                    f"Please check your network connection or try again."
                ) from e

            if any(
                keyword in error_message
                for keyword in [
                    "not found",
                    "model not found",
                    "does not exist",
                    "invalid model",
                ]
            ):
                raise RuntimeError(
                    f"The model configured for {self.provider} "
                    f"could not be found or is invalid."
                ) from e

            # Generic API error
            raise RuntimeError(
                f"{self.provider} API request failed: {e}"
            ) from e

    def get_llm(self):
        return self.llm