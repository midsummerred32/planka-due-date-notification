from plankapy import Planka, PasswordAuth
import requests
from datetime import datetime, timezone
import json

planka = Planka("https://planka.midsummerred32.com",
                PasswordAuth("midsummerred32", "NintendoGamer08!"))

print("User info:", planka.me)
print("Projects:", planka.projects)

# Home Assistant webhook URL
webhook_url = "https://home.midsummerred32.com/api/webhook/-N9Bcq6asoHOyUpdb8mv0w1_o"

# Get today's date
today = datetime.now(timezone.utc).date()

# List all cards with their due dates and check for today's tasks
print("\nCards with due dates:")
cards_due_today = []

for project in planka.projects:
  print(f"\nProject: {project.name}")
  for board in project.boards:
    print(f"  Board: {board.name}")
    for list_item in board.lists:
      print(f"    List: {list_item.name}")
      for card in list_item.cards:
        if hasattr(card, 'dueDate') and card.dueDate:
          # Parse the due date
          due_date = datetime.fromisoformat(card.dueDate.replace(
              'Z', '+00:00'))
          due_date_only = due_date.date()

          print(f"      Card: {card.name} - Due: {card.dueDate}")

          # Check if due date is today
          if due_date_only == today:
            # Construct card URL
            card_url = f"https://planka.midsummerred32.com/cards/{card.id}"

            # Format due date for webhook payload
            formatted_due_date = due_date.strftime("%m/%d/%Y at %I:%M %p")

            cards_due_today.append({
                "taskname": card.name,
                "due_date": formatted_due_date,
                "card_url": card_url
            })
            print(f"        *** DUE TODAY! ***")
        else:
          print(f"      Card: {card.name} - No due date")

# Send webhook for cards due today
if cards_due_today:
  print(
      f"\nFound {len(cards_due_today)} card(s) due today. Sending webhook...")

  for card_info in cards_due_today:
    payload = {
        "taskname": card_info["taskname"],
        "due_date": card_info["due_date"],
        "card_url": card_info["card_url"]
    }

    try:
      response = requests.post(webhook_url, json=payload, timeout=10)
      if response.status_code == 200:
        print(f"✅ Webhook sent successfully for: {card_info['taskname']}")
      else:
        print(
            f"❌ Webhook failed for {card_info['taskname']}: {response.status_code}"
        )
    except requests.exceptions.RequestException as e:
      print(f"❌ Error sending webhook for {card_info['taskname']}: {e}")
else:
  print("\nNo cards due today.")