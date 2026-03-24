---
name: AI Code Masker
description: A privacy-first developer tool that allows you to safely mask identifiers in source code before sharing with AI, and restore them afterwards.
---

# AI Code Masker

This skill allows you to safely process source code with AI by masking sensitive identifiers (like variable names, class names, method names) before sharing the code. It replaces them with generic names and stores the mapping locally.

**Supported Languages:**
- Java
- Python
- JavaScript / React

## Usage

The primary tool for this skill is a Python CLI script located at `scripts/masker.py`.
You can use it via the `run_command` tool.

### Masking Code
```bash
python .agents/skills/ai-code-masker/scripts/masker.py mask <path_to_file>
```
This will:
1. Parse the source file and identify non-keyword identifiers.
2. Replace identifiers with generic sequences (e.g., `var_1`, `class_1`, `method_1`).
3. Generate a `<path_to_file>.masked` file containing the safe code.
4. Save the mappings to a `<path_to_file>.map.json` file in the same directory.

### Unmasking Code
```bash
python .agents/skills/ai-code-masker/scripts/masker.py unmask <path_to_masked_file>
```
This will:
1. Load the corresponding `<path_to_file>.map.json` file.
2. Replace all generic identifiers in the masked code with their original names.
3. Generate a `<path_to_file>.unmasked` file (which should match the original).

## When to use this skill
- When the user asks to share code with an AI (or with you, the agent) but wants to hide sensitive identifiers.
- When you are writing code that contains sensitive business logic names and the user requests you to mask them before displaying or saving them.

## Notes
- The masker tries its best to distinguish variables, methods, and classes by checking adjacent characters (e.g., a trailing `(` often means a method), but this is a heuristic.
- The execution is fully local and does not require internet access.
