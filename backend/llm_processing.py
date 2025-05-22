from langchain.llms import OpenAI

class LLMHelper:
    def __init__(self):
        self.llm = OpenAI(temperature=0)
    
    def fix_json_format(self, error_message, data):
        prompt = f"""Fix this JSON data based on the error: {error_message}
        Original data: {data}
        Return ONLY valid JSON:"""
        return self.llm(prompt)
    
    def summarize_business_description(self, description):
        prompt = f"""Summarize this business description for official forms:
        {description}
        Keep under 200 characters. Use formal language.
        Summary:"""
        return self.llm(prompt)
    