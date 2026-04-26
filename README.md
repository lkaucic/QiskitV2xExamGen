# Qiskit v2.x Practice Exam Generator

This repository contains a simple Python-based generator for creating randomized Qiskit v2.x practice exams from a YAML question bank and exporting the result as a LaTeX/PDF quiz.

The goal is to maintain a reusable question library and generate N-question quizzes that approximately follow the IBM Certified Quantum Developer using Qiskit v2.x topic distribution.

---

## What this project does

The generator:

- Loads questions from YAML files
- Selects questions according to a section-based distribution
- Randomizes the final question order
- Supports:
  - plain multiple-choice questions
  - code snippets
  - circuit images
- Generates a LaTeX exam file
- Compiles it into a PDF using `pdflatex`
- Generates an answer key at the end of the document

---

# Recommended Project Structure

```text
qiskit-question-bank/
│
├── generate_quiz.py
├── requirements.txt
├── README.md
│
├── config/
│   ├── distribution.yaml
│   └── settings.yaml
│
├── questions/
│   ├── section1_perform_operations.yaml
│   ├── section2_visualization.yaml
│   ├── section3_create_circuits.yaml
│   ├── section4_run_circuits.yaml
│   ├── section5_sampler.yaml
│   ├── section6_estimator.yaml
│   ├── section7_results_analysis.yaml
│   └── section8_openqasm.yaml
│
├── templates/
│   ├── quiz_template.tex
│   ├── answer_key.tex
│   └── macros.tex
│
├── output/
│   ├── quiz_001.tex
│
├── assets/
│   ├── circuits/
│
└── tests/
    ├── test_001.pdf

---

## Requirements

### 1. Python

Python 3.10 or newer is recommended.

Check your Python version:

```bash
python --version
```

or:

```bash
python3 --version
```

---

### 2. Python packages

Install dependencies with:

```bash
pip install -r requirements.txt
```

Minimum `requirements.txt`:

```txt
pyyaml
```

If your script uses `adjustbox` only in LaTeX, no extra Python package is needed.

---

### 3. LaTeX distribution

To generate a PDF, you need a working LaTeX installation with `pdflatex`.

#### macOS

Recommended:

```bash
brew install --cask mactex
```

or install BasicTeX:

```bash
brew install --cask basictex
```

If using BasicTeX, you may need additional packages:

```bash
sudo tlmgr update --self
sudo tlmgr install enumitem braket listings adjustbox collectbox
```

#### Linux

On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install texlive-latex-base texlive-latex-extra texlive-fonts-recommended
```

#### Windows

Install MiKTeX or TeX Live:

- MiKTeX: https://miktex.org/
- TeX Live: https://tug.org/texlive/

After installation, make sure `pdflatex` is available from the terminal:

```bash
pdflatex --version
```

---

## How to run

From the repository root:

```bash
python generate_quiz.py
```

or:

```bash
python3 generate_quiz.py
```

Expected output:

```text
Generated LaTeX: output/output.tex
Generated PDF: tests/output.pdf
```

The final PDF should be created at:

```text
tests/output.pdf
```

The generated LaTeX file should be created at:

```text
output/output.tex
```

---

## Question distribution

For a 20-question quiz, the current minimum distribution is:

```text
Section 1: 3 questions
Section 2: 2 questions
Section 3: 4 questions
Section 4: 3 questions
Section 5: 2 questions
Section 6: 2 questions
Section 7: 2 questions
Section 8: 2 questions
```

This gives a total of 20 questions.

The section files are:

```text
section1_perform_operations.yaml
section2_visualization.yaml
section3_create_circuits.yaml
section4_run_circuits.yaml
section5_sampler.yaml
section6_estimator.yaml
section7_results_analysis.yaml
section8_openqasm.yaml
```

---

## YAML question format

Each question is stored as a YAML item.

Basic example:

```yaml
- id: S1-001
  section: 1
  question: "What does an X gate do to $\\ket{0}$?"
  choices:
    A: "Creates $\\ket{+}$"
    B: "Maps it to $\\ket{1}$"
    C: "Measures the qubit"
    D: "Adds a global phase only"
  answer: B
```

---

## Question with code

Use the `code` field for Python/Qiskit snippets.

```yaml
- id: S3-002
  section: 3
  question: "What does the following circuit prepare?"
  code: |
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
  choices:
    A: "$\\ket{00}$"
    B: "$\\ket{11}$"
    C: "$\\frac{1}{\\sqrt{2}}(\\ket{00}+\\ket{11})$"
    D: "$\\frac{1}{\\sqrt{2}}(\\ket{01}+\\ket{10})$"
  answer: C
```

Code blocks are rendered using LaTeX `lstlisting`.

---

## Question with circuit image

Place circuit images in:

```text
assets/circuits/
```

Example YAML:

```yaml
- id: S3-005
  section: 3
  question: "What state does the circuit below prepare?"
  image: "assets/circuits/bell.png"
  choices:
    A: "$\\ket{00}$"
    B: "$\\ket{11}$"
    C: "$\\frac{1}{\\sqrt{2}}(\\ket{00}+\\ket{11})$"
    D: "$\\frac{1}{\\sqrt{2}}(\\ket{01}+\\ket{10})$"
  answer: C
```

Recommended image formats:

- PNG
- PDF
- SVG converted to PDF
- high-resolution PNG for circuit screenshots

For best quality, prefer vector formats where possible.

---

## LaTeX escaping rules

Because questions are rendered directly into LaTeX, some characters need care.

### Underscores

Wrong:

```yaml
question: "What does qc.measure_all() do?"
```

Correct:

```yaml
question: "What does \\texttt{qc.measure\\_all()} do?"
```

Underscore `_` has special meaning in LaTeX, so it must be escaped as `\\_`.

### Backslashes

Inside YAML strings, LaTeX commands need double backslashes.

Example:

```yaml
question: "What is $\\ket{0}$?"
```

This becomes in LaTeX:

```latex
What is $\ket{0}$?
```

---

## Useful LaTeX commands

The generated document supports:

```latex
\ket{0}
\ket{1}
\frac{1}{\sqrt{2}}
\texttt{qc.measure\_all()}
```

The template uses packages such as:

```latex
\usepackage{amsmath}
\usepackage{braket}
\usepackage{listings}
\usepackage{graphicx}
```

If image auto-sizing is used, it may also use:

```latex
\usepackage{adjustbox}
```

---

## Recommended `.gitignore`

Generated files should usually not be committed.

Recommended `.gitignore`:

```gitignore
# Python
__pycache__/
*.pyc
.venv/
venv/

# Generated LaTeX/PDF outputs
output/
tests/
*.aux
*.log
*.out
*.toc
*.fls
*.fdb_latexmk
*.synctex.gz

# OS files
.DS_Store
Thumbs.db
```

Commit the source files, question bank, and assets:

```text
generate_quiz.py
requirements.txt
README.md
questions/
assets/
```

---

## Common errors and fixes

### Error: `No such file or directory: questions`

Make sure you are running the script from the repository root:

```bash
python generate_quiz.py
```

If needed, use absolute paths in the script based on:

```python
BASE_DIR = Path(__file__).resolve().parent
```

---

### Error: `Something's wrong--perhaps a missing \item`

This usually means no questions were generated.

Check that:

- YAML files exist in `questions/`
- each YAML file contains a list of questions
- section numbers match the expected distribution
- there are enough questions for each section

---

### Error: `Missing $ inserted`

Usually caused by unescaped LaTeX characters, often `_`.

Example problem:

```yaml
question: "What does qc.measure_all() do?"
```

Fix:

```yaml
question: "What does \\texttt{qc.measure\\_all()} do?"
```

---

### PDF generated, but path looks wrong

Wrong output example:

```text
tests/test.pdf/output.pdf
```

This means `test.pdf` was accidentally used as a directory.

Correct setup should look like:

```python
OUTPUT_DIR = BASE_DIR / "tests"
OUTPUT_TEX = BASE_DIR / "output" / "output.tex"
OUTPUT_PDF = OUTPUT_DIR / "output.pdf"
```

The `-output-directory` argument must be a folder, not a PDF filename.

Correct:

```python
subprocess.run(
    [
        "pdflatex",
        "-interaction=nonstopmode",
        "-output-directory",
        str(OUTPUT_DIR),
        str(OUTPUT_TEX),
    ],
    check=True,
    cwd=BASE_DIR,
)
```

---

### Error: `pdflatex: command not found`

Install a LaTeX distribution and confirm:

```bash
pdflatex --version
```

---

### Image is too large or pixelated

Do not force very small images to expand.

Recommended LaTeX rendering:

```latex
\adjustbox{max width=0.65\linewidth,max height=0.18\textheight}{\includegraphics{assets/circuits/bell.png}}
```

This keeps images at natural size unless they are too large.

---

## Development workflow

Typical workflow:

```bash
git status
git add generate_quiz.py questions/ assets/ README.md requirements.txt
git commit -m "Add Qiskit exam generator"
git push
```

Before pushing, make sure generated files are ignored unless you intentionally want to version exam outputs.

---

## Future improvements

Possible next steps:

- add difficulty levels
- add explanations for answers
- generate separate answer-key PDF
- support command-line arguments
- support random seed for reproducible exams
- validate YAML before rendering
- add automatic LaTeX escaping
- generate multiple quiz versions at once
- export statistics about selected sections
- support question tags such as `gates`, `sampler`, `estimator`, `transpilation`

---

## License

Add your chosen license here if needed.

Example:

```text
MIT License
```
