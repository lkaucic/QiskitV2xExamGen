# Project Structure

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
│   ├── quiz_001.pdf
│   ├── quiz_001_answers.pdf
│   └── archive/
│
├── assets/
│   ├── logo.png
│   └── images/
│
└── tests/
    ├── test_loader.py
    ├── test_distribution.py
    └── test_latex_render.py