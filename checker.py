import os
import random
from time import sleep

from dotenv import load_dotenv
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

load_dotenv()

MARKS = ['0.5', '1']


def login(driver: WebDriver):
    try:
        driver.find_element(by=By.ID, value='login').send_keys(os.getenv('EMAIL'))
        driver.find_element(by=By.CLASS_NAME, value='btn-lg').click()
        driver.find_element(
            by=By.ID, value='pass'
        ).send_keys(os.getenv('PASSWORD'))
        driver.find_element(by=By.NAME, value='button').click()
    except NoSuchElementException:
        return


def rate(driver: WebDriver, home_tasks: list[WebElement]) -> None:
    for unchecked in home_tasks:
        link = unchecked.get_attribute('href')
        driver.execute_script("window.open('" + link + "');")
        driver.switch_to.window(driver.window_handles[-1])
        sleep(2)
        table = driver.find_element(by=By.ID, value='results')
        ticks = table.find_elements(by=By.XPATH, value='//a[@title="Оценка"]')

        for i in range(len(ticks)):
            sleep(1)
            table = driver.find_element(by=By.ID, value='results')
            ticks = table.find_elements(
                by=By.XPATH,
                value='//a[@title="Оценка"]'
            )
            tick = ticks[i]
            tick.click()
            sleep(1)
            form = driver.find_element(
                by=By.ID, value='evaluation-value'
            )
            form.send_keys(Keys.CONTROL + 'a')
            form.send_keys(MARKS[random.randint(0, 1)])
            driver.find_element(by=By.ID, value='evaluation-save').click()

        sleep(1)
        driver.find_element(
            by=By.ID, value='evaluation-host'
        ).find_element(
            by=By.XPATH,
            value='//*[@id="evaluation-host"]/p[2]/button'
        ).click()

        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
        sleep(1)


def check_student(
        driver: WebDriver, search_form: WebElement, students: list[str]
) -> None:

    students_table = driver.find_element(by=By.ID, value='students')

    for student in students:
        search_form.send_keys(Keys.CONTROL + 'a')
        search_form.send_keys(student)
        sleep(3)
        home_tasks = students_table.find_elements(by=By.CLASS_NAME,
                                                  value='text-red')
        rate(driver, home_tasks)
        sleep(1)


def main() -> None:
    driver = Chrome(service=Service(
        ChromeDriverManager(print_first_line=False).install()
    ))
    students = [
        'name1',
        'name2'
    ]
    driver.implicitly_wait(5)
    for page in ['MAIN_PAGE_1', 'MAIN_PAGE_2']:
        driver.get(os.getenv(page))
        login(driver)
        search_form = driver.find_element(
            by=By.XPATH,
            value='//*[@id="students_filter"]/label/input'
        )
        check_student(driver, search_form, students)


if __name__ == '__main__':
    main()
