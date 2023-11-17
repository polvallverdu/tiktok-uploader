# TikTok Uploader

This Python-based tool facilitates the uploading of TikTok videos with manual intervention. It leverages the Playwright library for web automation.

## Requirements

- `playwright`

## Usage

1. **Installation**

   Install the required dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   Install Playwright's firefox browser:

    ```bash
    playwright install firefox
    ```

2. **Getting Started**

   Run the application by executing `main.py`.

   ```bash
   python main.py
   ```

## Functions

- **Register Account:** Allows registration of a TikTok account. Requires manual input of username, description, and login credentials.

- **Login:** Log into an existing TikTok account. Provides the option to input credentials and associate them with the account.

- **Manage Accounts:** Edit or delete existing accounts' descriptions.

- **Upload Video:** Select an account to upload a video to TikTok. This function navigates to the video upload page for the chosen account.

## File Structure

- `main.py`: Contains the main application logic for registering, logging in, managing accounts, and uploading videos.

- `accounts.json`: Stores account details like username, description, timestamps, and cookies.

## Disclaimer

This tool interacts with TikTok's web interface, which may be subject to changes in the platform's structure or policies. Use this tool responsibly and be aware of TikTok's terms of service and usage guidelines.
