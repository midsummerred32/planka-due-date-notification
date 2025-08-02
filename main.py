
from plankapy import Planka, PasswordAuth

planka = Planka("https://planka.midsummerred32.com",
                PasswordAuth("midsummerred32", "NintendoGamer08!"))

print("User info:", planka.me)
print("Projects:", planka.projects)

# List all cards with their due dates
print("\nCards with due dates:")
for project in planka.projects:
    print(f"\nProject: {project.name}")
    for board in project.boards:
        print(f"  Board: {board.name}")
        for list_item in board.lists:
            print(f"    List: {list_item.name}")
            for card in list_item.cards:
                if hasattr(card, 'dueDate') and card.dueDate:
                    print(f"      Card: {card.name} - Due: {card.dueDate}")
                else:
                    print(f"      Card: {card.name} - No due date")
