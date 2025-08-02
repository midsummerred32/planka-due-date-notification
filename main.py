from plankapy import Planka, PasswordAuth

planka = Planka("https://planka.midsummerred32.com",
                PasswordAuth("midsummerred32", "NintendoGamer08!"))

print(planka.me)

print(planka.projects)

