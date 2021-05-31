<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: Healthsea. Detect health conditions in supplement reviews and determine the effect of the products.

This project trains a NER with the label `CONDITION` and a textcat with three exclusive classes `IMPROVED`,`WORSEN`,`NEUTRAL`. It uses the dependency parsing to extract statements made about found conditions, these statements are then classified by the textcat. For more details, see [our blog post]().

## 📋 project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. For details, see the
[spaCy projects documentation](https://spacy.io/usage/projects).

### ⏯ Commands

The following commands are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run).
Commands are only re-run if their inputs have changed.

| Command | Description |
| --- | --- |
| `install` | Install dependencies |
| `preprocess` | Convert the json annotations to spaCy's binary format |
| `train_ner` | Train a named entity recognition model |
| `train_textcat` | Train a text classification model |
| `evaluate_ner` | Evaluate the ner model and export metric |
| `evaluate_textcat` | Evaluate the textcat model and export metric |
| `package_ner` | Package the trained ner so it can be installed |
| `package_textcat` | Package the trained textcat so it can be installed |
| `visualize` | Visualize healthsea interactively using Streamlit |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `all` | `install` &rarr; `preprocess` &rarr; `train_ner` &rarr; `train_textcat` &rarr; `visualize` |
| `train` | `train_ner` &rarr; `train_textcat` |
| `evaluate` | `evaluate_ner` &rarr; `evaluate_textcat` |
| `package` | `package_ner` &rarr; `package_textcat` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| [`assets/ner_condition_training.json`](assets/ner_condition_training.json) | Local | JSON-formatted training data exported from Prodigy, annotated with `CONDITION` entities (3441 examples) |
| [`assets/ner_condition_eval.json`](assets/ner_condition_eval.json) | Local | JSON-formatted development data exported from Prodigy, annotated with `CONDITION` entities (860 examples) |
| [`assets/textcat_sentiment_training.json`](assets/textcat_sentiment_training.json) | Local | JSON-formatted training data exported from Prodigy, annotated with exclusive `IMPROVED`, `WORSEN`, `NEUTRAL` classes (1497 examples) |
| [`assets/textcat_sentiment_eval.json`](assets/textcat_sentiment_eval.json) | Local | JSON-formatted development data exported from Prodigy, annotated with exclusive `IMPROVED`, `WORSEN`, `NEUTRAL` classes (369 examples) |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->

---


