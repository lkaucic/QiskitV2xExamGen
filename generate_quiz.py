# generate_quiz.py
# Simple starter version:
# - loads YAML questions
# - picks random questions by section
# - renders LaTeX
# - saves quiz.tex

import yaml
import random
from pathlib import Path
import subprocess

# =========================
# CONFIG
# =========================

QUIZ_SIZE = 20

# Example section distribution (counts for 20-question exam)
SECTION_COUNTS = {
    1: 3,
    2: 2,
    3: 4,
    4: 3,
    5: 2,
    6: 2,
    7: 2,
    8: 2
}

QUESTIONS_DIR = Path("questions")
OUTPUT_DIR_TEX = Path("output")
OUTPUT_DIR_PDF = Path("tests")
OUTPUT_FILE = OUTPUT_DIR_TEX / "output.tex"
OUTPUT_PDF = OUTPUT_DIR_PDF


# =========================
# LOAD QUESTIONS
# =========================

def load_questions():
    all_questions = []

    for file in QUESTIONS_DIR.glob("*.yaml"):
        with open(file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            all_questions.extend(data)

    return all_questions


# =========================
# PICK QUESTIONS
# =========================

def select_questions(question_bank):
    selected = []
    used_ids = set()

    for section, count in SECTION_COUNTS.items():

        # questions from requested section
        pool = [
            q for q in question_bank
            if q["section"] == section and q["id"] not in used_ids
        ]

        chosen = []

        if len(pool) >= count:
            chosen = random.sample(pool, count)

        else:
            chosen = pool.copy()

            missing = count - len(chosen)

            # fallback: any unused questions
            fallback_pool = [
                q for q in question_bank
                if q["id"] not in used_ids
                and q["id"] not in [x["id"] for x in chosen]
            ]

            if len(fallback_pool) >= missing:
                chosen += random.sample(fallback_pool, missing)
            else:
                chosen += fallback_pool

        for q in chosen:
            used_ids.add(q["id"])

        selected.extend(chosen)

    random.shuffle(selected)
    return selected

# =========================
# LATEX HELPERS
# =========================

def render_question(q):
    latex = f"\\item {q['question']}\n\n"

    if "code" in q:
        latex += "\\begin{lstlisting}[language=Python]\n"
        latex += q["code"]
        latex += "\n\\end{lstlisting}\n\n"

    if "image" in q:
        latex += "\\begin{center}\n"
        latex += f"\\adjustbox{{max width=0.8\\linewidth,max height=0.22\\textheight}}{{\\includegraphics{{{q['image']}}}}}\n"
        latex += "\\end{center}\n\n"

    latex += "\\begin{enumerate}[label=\\Alph*.]\n"

    for key in ["A", "B", "C", "D"]:
        latex += f"\\item {q['choices'][key]}\n"

    latex += "\\end{enumerate}\n\n"

    return latex


def render_answers(questions):
    out = "\\begin{enumerate}\n"

    for q in questions:
        out += f"\\item {q['id']}: {q['answer']}\n"

    out += "\\end{enumerate}\n"

    return out


def render_document(questions):
    body = ""

    for q in questions:
        body += render_question(q)

    answers = render_answers(questions)

    return rf"""
\documentclass[11pt,a4paper]{{article}}

\usepackage[margin=1in]{{geometry}}
\usepackage{{enumitem}}
\usepackage{{amsmath}}
\usepackage{{braket}}
\usepackage{{listings}}
\usepackage{{graphicx}}
\usepackage{{adjustbox}}
\title{{Qiskit v2.x Practice Quiz}}
\date{{}}

\begin{{document}}

\maketitle

\section*{{Questions}}

\begin{{enumerate}}
{body}
\end{{enumerate}}

\newpage

\section*{{Answer Key}}

{answers}

\end{{document}}
"""


# =========================
# MAIN
# =========================

def main():
    OUTPUT_PDF.mkdir(exist_ok=True)

    bank = load_questions()
    quiz = select_questions(bank)

    latex = render_document(quiz)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(latex)

    print("Generated LaTeX:", OUTPUT_FILE)

    try:
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(OUTPUT_DIR_PDF), str(OUTPUT_FILE)],
            check=True
        )
        print("Generated PDF:", OUTPUT_PDF)

    except FileNotFoundError:
        print("pdflatex not found. LaTeX file was generated, but PDF was not compiled.")

    except subprocess.CalledProcessError:
        print("PDF compilation failed. Check the .log file in tests/.")


if __name__ == "__main__":
    main()