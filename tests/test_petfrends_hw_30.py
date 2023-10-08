import pytest
import selenium.webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:/webDrivers/chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    pytest.driver.find_element_by_id('email').send_keys('qwerty111@qwerty.qwerty')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('qwerty')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()

    page_title = pytest.driver.find_element_by_tag_name('h1')

    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-center"))
    )
    # Проверяем, что мы оказались на главной странице пользователя
    assert element.text == "PetFriends"

    yield

    pytest.driver.quit()


def test_pet_count():
    # ожидаем подгрузки самой страницы
    pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')
    total_pet_count_displayed = pytest.driver.find_elements_by_css_selector('.table tbody tr')
    pet_count = int(pytest.driver.find_element(By.CLASS_NAME, 'task3').text.split("\n")[1].split(" ")[-1])

    assert len(total_pet_count_displayed) == pet_count


def test_pet_pet_photos_les_ten_50_persent():
    # ожидаем подгрузки самой страницы
    pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')
    pet_cards = pytest.driver.find_elements_by_css_selector('.table tbody tr')
    pet_images = pytest.driver.find_elements_by_css_selector('.table tbody tr img')
    photos_count = 0
    for i in range(len(pet_cards)):
        if pet_images[i].get_attribute('src') != '':
            photos_count = photos_count + 1
    print('у 50% питомцев есть фото')
    assert photos_count >= len(pet_cards) / 2


def test_pet_information():
    pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')
    pet_cards = pytest.driver.find_elements_by_css_selector('.table tbody tr')
    pet_names = pytest.driver.find_elements_by_css_selector('.table tbody td')
    pet_type = pytest.driver.find_elements_by_css_selector('.table tbody td:nth-child(2)')
    pet_age = pytest.driver.find_elements_by_css_selector('.table tbody td:last-child')

    for i in range(len(pet_cards)):
        assert pet_names[i].text != ''
        assert pet_type[i].text !=''
        assert pet_age[i].text != ''
    print('У всех питомцев заполнены данные')