class PromptManager:
    """
    Builds prompts for each tenant including agent bits.
    """

    def __init__(self, tenant):
        self.tenant = tenant

    def _agent_bits_text(self) -> str:
        """
        Convert agent bits (list of strings) into a formatted prompt block.
        """
        bits = self.tenant.config.get("agent_bits") or []
        if not bits:
            return ""

        formatted = "\n".join(f"- {bit}" for bit in bits)

        return (
            "\n\nIMPORTANT BUSINESS CONTEXT:\n"
            "The following temporary business notices MUST be considered when answering:\n"
            f"{formatted}\n"
        )

    def build_full_prompt(self, user_query, context_docs):
        style_prompt = self.tenant.config.get("style_prompt", "")
        guardrails_prompt = self.tenant.config.get("guardrails", "")
        agent_bits_prompt = self._agent_bits_text()

        context_section = "\n".join(
            doc.page_content for doc in context_docs
        )

        return f"""
SYSTEM INSTRUCTIONS:
{self.tenant.config.get("system_prompt")}

STYLE:
{style_prompt}

RULES:
{guardrails_prompt}

{agent_bits_prompt}

CONTEXT:
{context_section}

USER QUERY:
{user_query}

INSTRUCTIONS:
Use the CONTEXT to answer the USER QUERY.
Follow the STYLE and RULES strictly.
If the answer is not in the CONTEXT, say "I don't know."
""".strip()
