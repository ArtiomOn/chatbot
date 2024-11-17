class PromptTemplates:
    def __init__(self, use_search: bool):
        self.use_search = use_search

    @property
    def get_human_template(self) -> str:
        return (
            "{search_results}\n\nUser Query: {input}" if self.use_search else "{input}"
        )

    @property
    def get_search_capability_template(self) -> str:
        return (
            "You have access to real-time Google Search results."
            if self.use_search
            else ""
        )

    @property
    def get_system_template(self) -> str:
        return """You are a helpful assistant that remembers previous conversation context.
        {search_capability}
        When using search results, analyze and summarize them naturally in your response, citing sources when relevant."""
