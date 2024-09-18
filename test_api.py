from dotenv import load_dotenv
import os
import requests
import logging

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Загрузка переменных окружения из .env файла
load_dotenv()

# Ваш GitHub токен
GITHUB_TOKEN = os.getenv('API_KEY')

# Имя пользователя GitHub
GITHUB_USERNAME = os.getenv('USERNAME')

# URL GitHub API для создания репозитория
url_new = "https://api.github.com/user/repos"

# URL GitHub API
url = "https://api.github.com/user/repos"

# Заголовки, включая токен аутентификации
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Имя репозитория для теста
new_repo = 'new_repo'


def new_repos():
    # Данные для создания репозитория
    data = {
        "name": new_repo,  # Название нового репозитория
        "description": "This is a test repository",  # Описание
        "private": False  # True для приватного репозитория, False для публичного
    }

    # Отправка POST-запроса для создания репозитория
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        logging.info(f"Репозиторий '{data['name']}' успешно создан!")
    else:
        logging.error(f"Ошибка при создании репозитория: {response.status_code}")
        logging.error(response.json())
    pass

def check_list_repo():
    # Отправка GET-запроса для получения списка всех репозиториев
    response = requests.get(url, headers=headers)

    # Проверка статуса ответа
    if response.status_code == 200:
        repos = response.json()

        # Список имен репозиториев
        repo_names = [repo['name'] for repo in repos]

        # Проверка наличия репозитория "new-repo"
        if new_repo in repo_names:
            logging.info("Репозиторий 'new-repo' существует.")
        else:
            logging.info("Репозиторий 'new-repo' не найден.")
    else:
        logging.error(f"Ошибка при получении списка репозиториев: {response.status_code}")
        logging.error(response.json())
    pass

def delete_new_repo():
    # URL GitHub API для удаления репозитория
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{new_repo}"
    # Отправка DELETE-запроса для удаления репозитория
    response = requests.delete(url, headers=headers)

    # Проверка статуса ответа
    if response.status_code == 204:
        logging.info(f"Репозиторий '{new_repo}' успешно удален.")
    elif response.status_code == 404:
        logging.info(f"Репозиторий '{new_repo}' не найден.")
    else:
        logging.error(f"Ошибка при удалении репозитория: {response.status_code}")
        logging.error(response.json())

if __name__ == '__main__':
    logging.info("Script started")
    new_repos()
    check_list_repo()
    delete_new_repo()
    logging.info("Script finished")