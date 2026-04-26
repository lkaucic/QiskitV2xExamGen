qiskit-question-bank/
│
├── generate_quiz.py              # Main script: loads YAML, selects questions, builds LaTeX
├── requirements.txt             # pyyaml, jinja2 (optional)
├── README.md                    # How to use project
│
├── config/
│   ├── distribution.yaml        # Section percentages / quiz rules
│   └── settings.yaml            # Default quiz size, seed, options
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
│   ├── quiz_template.tex        # Main LaTeX template
│   ├── answer_key.tex           # Optional separate answer key layout
│   └── macros.tex               # Optional custom commands (\ket{}, etc.)
│
├── output/
│   ├── quiz_001.tex
│   ├── quiz_001.pdf
│   ├── quiz_001_answers.pdf
│   └── archive/
│
├── assets/
│   ├── logo.png                 # Optional IBM / personal logo
│   └── images/                 # Circuit images if ever needed
│
└── tests/
    ├── test_loader.py
    ├── test_distribution.py
    └── test_latex_render.py