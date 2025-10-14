# Improvement Opportunities Overview

This document summarizes high-impact improvements identified during a quick review of the MJ Microstock Prompter Pro codebase.

## 1. Security & Secrets Handling
- The `/api/config` endpoint returns raw Gemini and OpenAI API keys to any caller, which is a critical secret management vulnerability. Remove the endpoint or expose only capability flags through a server-controlled proxy instead of the actual keys. 【F:app.py†L22-L28】
- `app.secret_key` falls back to `None` when the environment variable is absent, leaving session data unsigned. Provide a safe default or fail fast during startup. 【F:app.py†L19-L21】

## 2. Reliability & API Error Handling
- Prompt generation loops call third-party APIs sequentially and block the entire request with `time.sleep(2)` after every prompt. Replace the fixed delay with provider-aware rate limiting or background job processing so the UI stays responsive. 【F:app.py†L88-L119】【F:app.py†L155-L194】
- A single provider error aborts the whole batch and returns HTTP 500. Collect per-prompt failures, surface them in the response, and continue processing the remaining prompts for a better user experience. 【F:app.py†L120-L123】【F:app.py†L195-L198】

## 3. Request Validation & Sanitization
- Endpoints assume `request.json` is populated and trust numerous string fields. Add schema validation (e.g., `pydantic` or `marshmallow`) and normalize fields before using them to build prompts or write files. 【F:app.py†L63-L123】【F:app.py†L128-L198】
- Uploaded filenames are only wrapped in `secure_filename` during download preparation. Enforce allowed extensions and path safety at upload time and centralize the validation logic. 【F:app.py†L291-L371】

## 4. Code Quality & Maintainability
- The Midjourney and FLUX prompt routes duplicate nearly identical batching logic. Extract shared helpers for iteration, metadata assembly, and error handling to reduce drift between the flows. 【F:app.py†L63-L198】
- Multiple modules call `logging.basicConfig`, which can clobber global logging configuration when imported. Configure logging once in the entry point instead. 【F:controller.py†L28-L32】【F:image_metadata_extractor.py†L20-L21】

## 5. Data Robustness
- `ImageMetadataExtractor` blindly parses model output with `json.loads`; unexpected responses will raise and only be caught by the outer handler. Add validation or a fallback parser to avoid losing metadata results when the AI returns natural language. 【F:image_metadata_extractor.py†L129-L198】
- Metadata analysis depends on `PrompterGenerator` even for simple keyword scoring. Consider decoupling optimizer routines so offline metadata extraction remains available without AI credentials. 【F:image_metadata_extractor.py†L26-L67】

## 6. Testing & Tooling
- Existing tests focus solely on the controller class and use heavy mocking. Add Flask integration tests that cover request validation, response schemas, and file processing to prevent regressions in the web layer. 【F:tests/test_prompter.py†L1-L108】
- No automated static analysis or type checking is configured. Introducing tools like `ruff`, `mypy`, or `bandit` would catch style issues and security pitfalls (e.g., the exposed API keys) earlier.

## 7. Documentation & Operations
- Document environment setup for required upload directories and expected rate limits. The current README mentions `.env` keys but omits operational safeguards like rotating credentials and handling failed background jobs. 【F:README.md†L56-L108】
- Provide deployment guidance (e.g., production WSGI server, HTTPS, secret storage) to help users run the app securely.

---
Addressing the points above will substantially improve the security posture, resilience, and maintainability of the application while giving contributors clearer guidance for extending the project.
