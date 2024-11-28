import requests
import json
import argparse
import os

VK_API_VERSION = "5.131"
BASE_URL = "https://api.vk.com/method"

def fetch_vk_data(token, user_id=572062014):
    try:
        user_info = requests.get(
            f"{BASE_URL}/users.get",
            params={
                "user_ids": user_id,
                "access_token": token,
                "v": VK_API_VERSION,
            }
        ).json()

        followers_ids = requests.get(
            f"{BASE_URL}/friends.get",
            params={
                "user_id": user_id,
                "access_token": token,
                "v": VK_API_VERSION,
            }
        ).json().get("response", {}).get("items", [])

        followers = []
        if followers_ids:
            followers = requests.get(
                f"{BASE_URL}/users.get",
                params={
                    "user_ids": ",".join(map(str, followers_ids)),
                    "access_token": token,
                    "v": VK_API_VERSION,
                }
            ).json().get("response", [])

        subscriptions_info = requests.get(
            f"{BASE_URL}/users.getSubscriptions",
            params={
                "user_id": user_id,
                "access_token": token,
                "v": VK_API_VERSION,
            }
        ).json().get("response", {})

        group_ids = subscriptions_info.get("groups", {}).get("items", [])
        groups = []
        if group_ids:
            groups = requests.get(
                f"{BASE_URL}/groups.getById",
                params={
                    "group_ids": ",".join(map(str, group_ids)),
                    "access_token": token,
                    "v": VK_API_VERSION,
                }
            ).json().get("response", [])

        return {
            "user": user_info.get("response", []),
            "followers": followers,
            "subscriptions": {
                "users": subscriptions_info.get("users", {}).get("items", []),
                "groups": groups,
            },
        }
    except Exception as e:
        print(f"Ошибка при запросе данных: {e}")
        return {}

def save_to_json(data, output_file):
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Данные сохранены в файл: {output_file}")
    except Exception as e:
        print(f"Ошибка сохранения файла: {e}")

def main():
    parser = argparse.ArgumentParser(description="VK_API")
    parser.add_argument("--token", required=True)
    parser.add_argument("--user_id", default=None)
    parser.add_argument("--output", default="vk_data.json")

    args = parser.parse_args()

    user_id = args.user_id
    token = args.token
    output_file = args.output

    if not os.path.exists(os.path.dirname(output_file)) and os.path.dirname(output_file):
        print(f"Некорректный путь для файла: {output_file}")
        return

    vk_data = fetch_vk_data(token, user_id)
    if vk_data:
        save_to_json(vk_data, output_file)

if __name__ == "__main__":
    main()