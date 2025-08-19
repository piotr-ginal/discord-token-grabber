import base64
import re

TOKEN_REGEX_PATTERN = r"[\w-]{24,26}\.[\w-]{6}\.[\w-]{34,38}"

def get_user_id_from_token(token: str) -> str | None:
    """Confirm that the portion of a string before the first dot can be decoded.

    Decoding from base64 offers a useful, though not infallible, method for identifying
    potential Discord tokens. This is informed by the fact that the initial
    segment of a Discord token usually encodes the user ID in base64. However,
    this test is not guaranteed to be 100% accurate in every case.

    Args:
        token (str): The potential Discord token to validate.

    Returns:
        A string representing the Discord user ID if the first part of the token
        can be successfully decoded, or None if decoding fails.
    """
    if not re.match(TOKEN_REGEX_PATTERN, token):
        return None

    try:
        discord_user_id = base64.b64decode(
            token.split(".", maxsplit=1)[0] + "=="
        ).decode("utf-8")
    except (UnicodeDecodeError, ValueError):
        return None

    return discord_user_id

def main() -> None:
    """Prompt the user to input a potential Discord token and validate it."""
    print("Enter a potential Discord token (or 'quit' to exit):")
    while True:
        token = input("> ").strip()
        if token.lower() == "quit":
            break

        if not token:
            print("Error: No token provided.")
            continue

        user_id = get_user_id_from_token(token)
        if user_id:
            print(f"Valid token format. Decoded Discord User ID: {user_id}")
        else:
            print("Invalid token format or unable to decode user ID.")

if __name__ == "__main__":
    main()
