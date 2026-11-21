
import spacy
from spacy.matcher import PhraseMatcher

from utils.skill_dictionary import SKILL_DICTIONARY, SKILL_ALIASES


# 1. Create NLP pipeline
nlp = spacy.blank("en")


# 2. Create PhraseMatcher
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")


# 3. Build alias lookup
alias_lookup = {}

for canonical_skill, aliases in SKILL_ALIASES.items():

    for alias in aliases:
        alias_lookup[alias.casefold()] = canonical_skill


# 4. Register canonical skills and aliases
for category, skills in SKILL_DICTIONARY.items():

    patterns = []

    for skill in skills:
        patterns.append(nlp.make_doc(skill))

    for canonical_skill, aliases in SKILL_ALIASES.items():

        if canonical_skill in skills:
            for alias in aliases:
                patterns.append(nlp.make_doc(alias))

    matcher.add(category, patterns)


# 5. Extract skills
def extract_skills(text: str) -> dict:

    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    doc = nlp(text)

    matches = matcher(doc)

    extracted_skills = {}

    for match_id, start, end in matches:

        category = nlp.vocab.strings[match_id]

        matched_text = doc[start:end].text

        # Standardize aliases
        skill = alias_lookup.get(
            matched_text.casefold(),
            next(
                (
                    item for item in SKILL_DICTIONARY[category]
                    if item.casefold() == matched_text.casefold()
                ),
                matched_text
            )
        )

        if category not in extracted_skills:
            extracted_skills[category] = []

        if skill.casefold() not in [
            existing.casefold()
            for existing in extracted_skills[category]
        ]:
            extracted_skills[category].append(skill)

    return extracted_skills
