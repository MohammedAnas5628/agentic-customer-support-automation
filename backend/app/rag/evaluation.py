import asyncio
import logging

from backend.app.agents.knowledge_agent import run_knowledge_agent


EVALUATION_CASES = (
    ("What is the return policy for products?", "returns_and_refunds.md"),
    ("How long is the product warranty?", "warranty.md"),
    ("How can I cancel my order?", "cancellation_and_replacement.md"),
    ("What payment methods does ElectroMart support?", "payments.md"),
    ("How do I secure or update my account?", "account_and_security.md"),
    ("What is the weather in Mumbai today?", None),
    ("Can you recommend a restaurant near me?", None),
    ("Who won the latest cricket match?", None),
)


async def run_evaluation() -> None:
    for question, expected_source in EVALUATION_CASES:
        result = await run_knowledge_agent(question)
        sources = ", ".join(source["source"] for source in result.sources) or "none"
        expected = expected_source or "no ElectroMart source expected"
        print(f"Question: {question}")
        print(f"Status: {result.status}; sources: {sources}; expected: {expected}")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    asyncio.run(run_evaluation())


if __name__ == "__main__":
    main()