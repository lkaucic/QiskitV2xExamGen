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

def render_choice(choice):

    if isinstance(choice, str):
        return choice

    parts = []

    if "text" in choice:
        parts.append(choice["text"])

    if "code" in choice:
        code = choice["code"].rstrip()
        parts.append(
            "\\begin{minipage}[t]{0.92\\linewidth}\n"
            "\\ttfamily\\small\n"
            "\\obeylines\\obeyspaces\n"
            f"{code}\n"
            "\\end{minipage}"
        )

    if "image" in choice:
        parts.append(
            f"\\adjustbox{{max width=0.35\\linewidth,max height=0.12\\textheight}}{{"
            f"\\includegraphics{{{choice['image']}}}"
            f"}}"
        )

    return "\n".join(parts)


def choices_are_images(q):
    return all(
        isinstance(q["choices"][key], dict)
        and "image" in q["choices"][key]
        for key in ["A", "B", "C", "D"]
    )


def render_question(q):
    if isinstance(q["answer"], list):
        latex = f"\\item {q['question']} \\textit{{(Select all that apply)}}\n\n"
    else:
        latex = f"\\item {q['question']}\n\n"

    if "code" in q:
        latex += "\\begin{lstlisting}[language=Python]\n"
        latex += q["code"]
        latex += "\n\\end{lstlisting}\n\n"

    if "image" in q:
        latex += "\\begin{center}\n"
        latex += (
            f"\\adjustbox{{max width=0.65\\linewidth,max height=0.18\\textheight}}{{"
            f"\\includegraphics{{{q['image']}}}"
            f"}}\n"
        )
        latex += "\\end{center}\n\n"

    if choices_are_images(q):

        latex += "\\begin{center}\n"
        latex += "\\begin{tabular}{cc}\n"

        latex += f"\\textbf{{A.}} {render_choice(q['choices']['A'])} & "
        latex += f"\\textbf{{B.}} {render_choice(q['choices']['B'])} \\\\\n"

        latex += f"\\textbf{{C.}} {render_choice(q['choices']['C'])} & "
        latex += f"\\textbf{{D.}} {render_choice(q['choices']['D'])}\n"

        latex += "\\end{tabular}\n"
        latex += "\\end{center}\n\n"

    else:
        latex += "\\begin{enumerate}[label=\\Alph*.]\n"

        for key in ["A", "B", "C", "D"]:
            latex += f"\\item {render_choice(q['choices'][key])}\n"

        latex += "\\end{enumerate}\n\n"

    return latex


def render_answers(questions):
    out = "\\begin{enumerate}\n"

    for q in questions:
        ans = q["answer"]
        if isinstance(ans, list):
            ans = ", ".join(ans)
        out += f"\\item {q['id']}: {ans}\n"

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