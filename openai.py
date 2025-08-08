"""Minimal stub of the :mod:`openai` package for testing purposes.

The real OpenAI Python client is not installed in the execution environment
used for the tests.  Only a very small subset of its interface is required and
even that is patched by the unit tests.  Providing this stub allows ``import
openai`` to succeed without pulling in the actual dependency.
"""

api_key = ""
__dummy__ = True


class OpenAI:  # pragma: no cover - simple lightweight stand‑in
    def __init__(self, api_key: str | None = None, **_kwargs):
        self.api_key = api_key

    class _Chat:
        class _Completions:
            def create(self, *args, **kwargs):  # noqa: D401 - mimics real method
                """Placeholder method used only when mocked in tests."""
                raise NotImplementedError(
                    "This is a stub used for testing and should be mocked"
                )

        completions = _Completions()

    chat = _Chat()

