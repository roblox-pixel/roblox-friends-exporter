import requests
import os
import time

user_id = input("Entre l'ID Roblox : ")

friends = []
cursor = None

print("Récupération des amis...")

# 🔹 Pagination automatique
while True:
    url = f"https://friends.roblox.com/v1/users/{user_id}/friends?limit=200"
    if cursor:
        url += f"&cursor={cursor}"

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    friends.extend(data.get("data", []))

    cursor = data.get("nextPageCursor")
    if not cursor:
        break

    time.sleep(0.3)  # petit délai pour éviter le rate limit

print(f"{len(friends)} amis trouvés.")

if not friends:
    print("Aucun ami trouvé.")
    exit()

# 🔹 Récupération des IDs
friend_ids = [friend["id"] for friend in friends]

print("Récupération des noms d'utilisateur...")

users_url = "https://users.roblox.com/v1/users"
all_users = []

# Roblox limite à 100 IDs par requête → on découpe en blocs
for i in range(0, len(friend_ids), 100):
    batch = friend_ids[i:i+100]
    response = requests.post(users_url, json={"userIds": batch})
    response.raise_for_status()
    all_users.extend(response.json().get("data", []))
    time.sleep(0.3)

# 🔹 Sauvegarde
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop, "amis_complets.txt")

with open(file_path, "w", encoding="utf-8") as f:
    for user in all_users:
        f.write(f"{user['id']} | {user['name']} | {user['displayName']}\n")

print("Fichier créé ici :", file_path)
print("Mission terminée 🚀")
