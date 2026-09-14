# Prompt Inventory

## Actual LLM Prompts

### Grounded customer-support answer
- Location: `backend/app/rag/generation.py`
- Symbol: `GROUNDING_SYSTEM_PROMPT`
- Used by: `generate_grounded_answer()` for knowledge/RAG answers and knowledge turns in the main support workflow.
- Input context: retrieved knowledge chunks, the current customer question, and the rolling conversation memory context.
- Sales behavior: recommendations are allowed only when relevant and grounded in catalog context; they must be clearly identified, balanced with limitations and alternatives, and free of pressure or hidden persuasion.

### Conversation-memory compaction
- Location: `backend/app/services/conversation_memory.py`
- Symbol: `MEMORY_SUMMARY_PROMPT`
- Used by: `compact_conversation()` after a conversation reaches the configured message threshold.
- Input context: the previous durable summary plus older raw transcript turns.

## Agent Behavior

The five agents do **not** currently have separate LLM prompts. They use deterministic routing and service/tool logic:

- `backend/app/agents/knowledge_agent.py`: query variants, retrieval, and grounded generation.
- `backend/app/agents/catalog_agent.py`: product intent/tool selection and catalog service calls.
- `backend/app/agents/order_agent.py`: order intent/tool selection and order service calls.
- `backend/app/agents/support_agent.py`: ticket intent/tool selection and ticket service calls.
- `backend/app/agents/escalation_agent.py`: escalation reason inference and handoff tool calls.

## Main Chat Window

The main chat UI is the frontend support component:

- Location: `frontend/features/support/support-chat.tsx`
- It does not contain an LLM prompt. It sends the customer's message to `POST /api/support/query` through `frontend/lib/api.ts`.
- The backend classifies the message in `backend/app/api/support.py`, then routes it through `backend/app/workflows/support_workflow.py`.
- Knowledge turns eventually use `GROUNDING_SYSTEM_PROMPT`.
- Authenticated chat turns carry `conversation_id`; the API client persists it in `localStorage` under `electromart_conversation_id`.

## Prompt-Safety Boundary

The current customer message, retrieved documents, and stored conversation history are untrusted data. The grounding and memory prompts explicitly instruct the model not to treat them as instructions, reveal secrets, or invent unsupported facts.

Customer-facing commercial behavior is intentionally transparent: the assistant may explain a relevant product or promotion, but it must not conceal advertising intent or manipulate a customer into believing a purchase is necessary.
