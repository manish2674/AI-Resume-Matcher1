
from core.text_cleaner import clean_text


sample_text = """
    PYTHON   DEVELOPER


Skills : Python,   Pandas, NumPy
Machine-Learning  |  Deep Learning
C++  |  C#  |  Node.js
Experience: 2 years
"""

cleaned_text = clean_text(sample_text)

print("ORIGINAL TEXT:")
print(sample_text)

print("\nCLEANED TEXT:")
print(cleaned_text)

print("\nOriginal characters:", len(sample_text))
print("Cleaned characters:", len(cleaned_text))
