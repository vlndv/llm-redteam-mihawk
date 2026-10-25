# llm-redteam

A small Python tool that attacks a local language model with adversarial prompts and reports how well it resists.

## What it tests
A chatbot is given a hidden system prompt containing a fake secret (`CANARY-7421`). Each of the 30 attacks tries to make it:
- **Leak** the secret or its instructions (encoding tricks, partial reveals, fake authority)
- **Obey** an injected instruction (prompt injection)
- **Break character** (jailbreak, off-topic)

## Results (30 attacks, temperature 0, seed 42)

| Model | Resisted |
|---|---|
| llama3.1:8b | 22/30 |
| qwen3.5 | 23/30 |

| Category | llama3.1:8b | qwen3.5 |
|---|---|---|
| system prompt leakage | 8/10 | 9/10 |
| prompt injection | 5/10 | 6/10 |
| jailbreak | 7/7 | 5/7 |
| off-topic | 2/3 | 3/3 |

Full tables are in [REPORT.md](REPORT.md).

## Findings
- **The two models fail differently.** llama3.1:8b obeyed 5 injected instructions but leaked the secret only twice. qwen3.5 obeyed 2 injections but leaked the secret in 5 replies.
- **A refusal is not the same as safety.** qwen3.5 repeatedly quoted the secret inside a refusal, and in one test it refused in Part 1 and printed the password in Part 2.
- **Both leaked the secret when asked to translate their instructions into French.**
- **The scores hide the difference.** The leak is scored under whichever attack triggered it, so category totals alone understate how often qwen3.5 leaked.
- **My first checker missed a leak.** I found it by reading the raw replies, then changed the evaluator to scan every reply for the secret, ignoring case and punctuation.

## Limitations
30 attacks, one run per model, keyword-based scoring. A one-point gap between models is not meaningful. Scoring does not capture partial instruction leaks (qwen3.5 revealed part of its system prompt in one test) or over-refusal. This is a starting point, not a benchmark.

## Run it
1. Install [Ollama](https://ollama.com) and pull a model: `ollama pull llama3.1:8b`
2. `pip install -r requirements.txt`
3. `python runner.py llama3.1:8b`
4. `python report.py results_llama3.1_8b.json`

## Files
- `model.py` calls the model
- `attacks.py` holds the attacks and the secret
- `runner.py` runs attacks and scores them
- `show.py` prints replies for manual review
- `report.py` builds `REPORT.md`