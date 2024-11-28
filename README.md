## Установка

1. Клонируйте репозиторий:
git clone https://github.com/shigamm/VK_API.git

2. Установите зависимости:
pip install -r requirements.txt

## Запуск

### Пример команды:

python main.py --token {YOUR_ACCESS_TOKEN} --user_id {USER_ID} --output {result.json}

- `--token`: Ваш токен доступа к VK API (обязательно).
- `--user_id`: Идентификатор пользователя (опционально, по умолчанию используется текущий).
- `--output`: Путь к выходному JSON-файлу (опционально, по умолчанию `vk_data.json`).

### Результат

Файл `vk_data.json` будет содержать информацию о пользователе, его подписчиках, подписках и группах в формате JSON.