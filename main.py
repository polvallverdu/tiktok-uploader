import asyncio
import json
import os
from playwright.async_api import async_playwright, Playwright, Browser, Page, BrowserContext
from datetime import datetime
import uuid

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')  # Uses 'cls' for Windows and 'clear' for Unix-like systems

def open_accounts():
  if os.path.exists("accounts.json"):
    with open("accounts.json", "r") as f:
      return json.load(f)
  else:
    with open("accounts.json", "w") as f:
      json.dump([], f)
    return []

def save_accounts(accounts):
  with open("accounts.json", "w") as f:
    json.dump(accounts, f)

async def open_browser(cookies: list|None = None) -> tuple[Playwright, Browser, BrowserContext, Page]:
  pw = await async_playwright().start()
  browser = await pw.firefox.launch(headless=False)
  context = await browser.new_context()

  if cookies:
    await context.add_cookies(cookies)

  page = await context.new_page()

  return (pw, browser, context, page)

async def close_browser(pw: Playwright, browser: Browser, context: BrowserContext, page: Page) -> list:
  updated_cookies = await context.cookies()
  await page.close()
  await context.close()
  await browser.close()
  await pw.stop()
  return updated_cookies

async def get_profile_username(page: Page) -> str:
  profile_href = await page.get_attribute("a[data-e2e='nav-profile']", "href")
  return profile_href[:profile_href.rfind("/")]

async def register_account():
  pw, browser, context, page = await open_browser()
  await page.goto("https://www.tiktok.com/signup/phone-or-email/email")
  
  await asyncio.to_thread(input, "Press enter when you are done...")
  
  username = input("Enter your username: ")
  cookies = await close_browser(pw, browser, context, page)
  
  print("")
  description = input("Enter a description for this account: ")
  
  accounts = open_accounts()
  accounts.append({
    "id": str(uuid.uuid4()),
    "username": username,
    "description": description,
    "timestamp": datetime.utcnow().timestamp(),
    "cookies": cookies
  })
  save_accounts(accounts)

async def login():
  email = input("Enter your email: ")
  password = input("Enter your password: ")
  
  pw, browser, context, page = await open_browser()
  await page.goto("https://www.tiktok.com/login/phone-or-email/email")
  
  # EMAIL_XPATH = "/html/body/div[1]/div/div[2]/div[1]/form/div[1]/input"
  EMAIL_SELECTOR = "input[name='username'][type='text']"
  # PASSWORD_XPATH = "/html/body/div[1]/div/div[2]/div[1]/form/div[2]/div/input"
  PASSWORD_SELECTOR = "input[type='password']"
  
  await page.fill(EMAIL_SELECTOR, email)
  await page.fill(PASSWORD_SELECTOR, password)
  
  await asyncio.to_thread(input, "Press enter when you are done...")
  
  username = input("Enter your username: ")
  cookies = await close_browser(pw, browser, context, page)
  
  print("")
  description = input("Enter a description for this account: ")
  
  accounts = open_accounts()
  accounts.append({
    "id": str(uuid.uuid4()),
    "username": username,
    "description": description,
    "timestamp": datetime.utcnow().timestamp(),
    "cookies": cookies
  })
  save_accounts(accounts)

async def select_account() -> dict:
  clear()
  print("Select an account")
  print("")
  print("")
  accounts = open_accounts()
  for i, account in enumerate(accounts):
    print(f"[{i+1}] {account['username']} - {account['description']}")
  print("")
  print("")
  print("Select the account you want to use")
  account_index = int(input("$ "))-1
  
  if account_index < 0 or account_index > len(accounts):
    print("Invalid account index")
    await asyncio.sleep(2)
    return await select_account()
  
  account = accounts[account_index]
  return account

async def upload_video():
  account = await select_account()
  
  pw, browser, context, page = await open_browser(account["cookies"])
  await page.goto("https://www.tiktok.com/creator-center/upload?from=upload")
  
  await asyncio.to_thread(input, "Press enter when you are done...")
  
  await close_browser(pw, browser, context, page)

async def manage_accounts():
  clear()
  print("Loading accounts...")
  
  accounts = []
  if os.path.exists("accounts.json"):
    with open("accounts.json", "r") as f:
      accounts = json.load(f)
  else:
    with open("accounts.json", "w") as f:
      json.dump(accounts, f)
  
  if len(accounts) == 0:
    print("No accounts found")
    await asyncio.sleep(1)
    return
  
  formated_accounts = []
  for i, account in enumerate(accounts):
    formated_accounts.append(f"[{i+1}] {account['username']} - {account['description']}")
  while True:
    clear()
    print("Manage Accounts")
    print("")
    print("")
    for account in formated_accounts:
      print(account)
    print("")
    print("Type 0 to go back")
    print("")
    print("")
    print("Select the account you want to edit")
    account_index = int(input("$ "))
    
    if account_index == 0:
      return
    
    account_index -= 1
    if account_index < 0 or account_index > len(formated_accounts):
      print("Invalid account index")
      await asyncio.sleep(2)
      continue
    
    clear()
    print("Manage Accounts")
    print(formated_accounts[account_index])
    print("")
    print("")
    print("1. Edit description")
    print("2. Delete account")
    print("")
    print("")
    print("Select what you want to do")
    action = int(input("$ "))
    
    if action == 1:
      print("")
      print("")
      print("Enter the new description")
      new_description = input("$ ")
      accounts[account_index]["description"] = new_description
      with open("accounts.json", "w") as f:
        json.dump(accounts, f)
      print("Description updated")
      await asyncio.sleep(1)
    elif action == 2:
      accounts.pop(account_index)
      with open("accounts.json", "w") as f:
        json.dump(accounts, f)
      print("Account deleted")
      await asyncio.sleep(1)

async def main():
  while True:
    clear()
    print("========================")
    print("Tiktok Uploader")
    print("========================")
    print("")
    print("")
    print("")
    print("1. Register account")
    print("2. Login to account")
    print("3. Manage Accounts")
    print("4. Upload video")
    print("")
    print("")
    print("Enter what you want to do")
    
    task = int(input("$ "))
    clear()
    
    if task == 1:
      await register_account()
    elif task == 2:
      await login()
    elif task == 3:
      await manage_accounts()
    elif task == 4:
      await upload_video()

if __name__ == "__main__":
  asyncio.run(main())
