# input_utils.py

Small helpers for sanitizing and converting user input.

## Functions
- `safe_int(value: str, default: Optional[int] = None) -> Optional[int]`
  Attempt to convert the value to an integer. Returns `default` on failure.
- `safe_float(value: str, default: Optional[float] = None) -> Optional[float]`
  Attempt to convert the value to a float. Returns `default` on failure.
- `sanitize_str(value: str) -> str`
  Trim surrounding whitespace from the string, returning an empty string if
  the input is `None`.
