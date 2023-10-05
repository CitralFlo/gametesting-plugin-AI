from typing import Optional
import language_tool_python
import logging

class GrammarChecker:
    def __init__(self, language: str = 'en-US'):
        self.tool = language_tool_python.LanguageTool(language)

    def check(self, text: str) -> Optional[str]:
        try:
            matches = self.tool.check(text)
            corrected_text = language_tool_python.correct(text, matches)
            return corrected_text
        except Exception as e:
            logging.error(f"Error in checking grammar: {e}")
            return None
