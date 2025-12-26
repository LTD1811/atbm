"""Parse markdown quiz file to extract questions with 4 options."""
import re
from pathlib import Path


def parse_quiz_markdown(filepath: str) -> list[dict]:
    """
    Parse markdown file and extract all questions.
    Questions with 4 options are 'quiz' type, others are 'flashcard' type.
    
    Returns list of dicts with: id, question, type, options/answer, correct
    """
    content = Path(filepath).read_text(encoding="utf-8")
    questions = []
    
    # Split by question headers: # **number\. Question text (ends at newline)
    pattern = r'^# \*\*(\d+)\\?\.\s*(.+)$'
    matches = list(re.finditer(pattern, content, re.MULTILINE))
    
    for i, match in enumerate(matches):
        q_num = int(match.group(1))
        q_text = match.group(2).strip()
        
        # Get content between this question and next (or end of file)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        answer_block = content[start:end]
        
        # Extract options A, B, C, D
        options = {}
        correct = None
        
        for option_letter in ['A', 'B', 'C', 'D']:
            # Pattern: *A. text OR A. text (with * marking correct answer)
            opt_pattern = rf'(\*?)({option_letter})\.\s*(.+?)(?=\n\n|\n[*A-D]\.|\Z)'
            opt_match = re.search(opt_pattern, answer_block, re.DOTALL)
            
            if opt_match:
                is_correct = opt_match.group(1) == '*'
                text = opt_match.group(3).strip()
                # Clean up the text
                text = re.sub(r'\s+', ' ', text)
                options[option_letter] = text
                if is_correct:
                    correct = option_letter
        
        # Questions with 4 options -> quiz type
        if len(options) == 4 and correct:
            questions.append({
                'id': q_num,
                'question': q_text,
                'type': 'quiz',
                'options': options,
                'correct': correct
            })
        else:
            # Extract flashcard answer (text after * *)
            flashcard_pattern = r'\*\s*\*(.+?)(?=\n\n|#|\Z)'
            flashcard_match = re.search(flashcard_pattern, answer_block, re.DOTALL)
            
            if flashcard_match:
                answer_text = flashcard_match.group(1).strip()
                answer_text = re.sub(r'\s+', ' ', answer_text)
                questions.append({
                    'id': q_num,
                    'question': q_text,
                    'type': 'flashcard',
                    'answer': answer_text,
                    'options': {},
                    'correct': None
                })
    
    return questions


if __name__ == "__main__":
    # Test parsing
    import json
    filepath = Path(__file__).parent.parent / "docs" / "300 câu ATBM dành cho HS tiểu học.md"
    questions = parse_quiz_markdown(str(filepath))
    print(f"Found {len(questions)} questions with 4 options")
    if questions:
        print(json.dumps(questions[0], ensure_ascii=False, indent=2))
