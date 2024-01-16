import os

from didyoumean.service.spell_checker_service import SpellCheckerService


class SpellCheckerEngine:
    def __init__(self):
        self.spell_checker_service = SpellCheckerService()

    def correct(self, text: str) -> str:
        return self.spell_checker_service.return_word(text)
