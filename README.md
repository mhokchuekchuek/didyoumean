# didyoumean

Thai Word Spell Correction by using [Peter's Norvig algorithm](https://norvig.com/spell-correct.html) and word frequency corpus from [ttc corpus](https://pythainlp.github.io/docs/2.0/api/corpus.html).

### Didyoumean Case's Support

- Forget to change Eng to TH

    - If can be change Eng to TH\
    `9hoqi5gxHowi` => ต้นรถเป็นไร

    - If cannot be change Eng to TH\
    `sasdfsjofjdios` => sasdfsjofjdios

- A little bit misspelled\
    `กฏหมาย` => กฎหมาย

### installation

```
pip install git+https://github.com/mhokchuekchuek/didyoumean.git
```

### How to Use

```python
from didyoumean.usecases.spell_correction import SpellCheckerEngine

spell_checker = SpellCheckerEngine()
spell_checker.correct("กฏหมาย")

## response
'กฎหมาย'
```