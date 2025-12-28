from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait as FluentWait
import time

# === Настройка WebDriver ===
service = Service('../driver/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# === Implicit Wait ===
driver.implicitly_wait(10)

# === Тест-отчет ===
test_report = []

start_time = time.time()

try:
    # === Шаг 1: Открываем DEMOQA Dropdown page для Select Class ===
    driver.get("https://demoqa.com/select-menu")
    test_report.append(("Open Select Menu Page", "PASS"))

    # === Шаг 2: Выбираем Old Select Menu для смены цвета и меняем по индексу ===
    color_dropdown = Select(WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "oldSelectMenu"))
    ))
    color_dropdown.select_by_visible_text("Red")  # visible text
    assert color_dropdown.first_selected_option.text == "Red"
    color_dropdown.select_by_index(3)  # index
    test_report.append(("Dropdown select", "PASS"))

    # === Шаг 3: Переходим на DEMOQA Buttons Page для Actions Class ===
    driver.get("https://demoqa.com/buttons")
    test_report.append(("Open Buttons Page", "PASS"))

    actions = ActionChains(driver)

    # Hover + Click
    double_click_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "doubleClickBtn"))
    )
    actions.double_click(double_click_btn).perform()
    test_report.append(("Double Click", "PASS"))

    # Right Click
    right_click_btn = driver.find_element(By.ID, "rightClickBtn")
    actions.context_click(right_click_btn).perform()
    test_report.append(("Right Click", "PASS"))

    # Click Me button (hover + click)
    click_me_btn = driver.find_element(By.XPATH, "//button[text()='Click Me']")
    actions.move_to_element(click_me_btn).click().perform()
    test_report.append(("Click Me button", "PASS"))

    # === Fluent Wait Example ===
    from selenium.webdriver.support.ui import WebDriverWait as FW
    from selenium.webdriver.support import expected_conditions as EC

    fluent_wait = FW(driver, timeout=15, poll_frequency=0.5, ignored_exceptions=[NoSuchElementException])
    message = fluent_wait.until(EC.visibility_of_element_located((By.ID, "rightClickMessage")))
    test_report.append(("Fluent Wait check", "PASS"))

except Exception as e:
    test_report.append(("Test Failed", f"FAIL - {e}"))

finally:
    end_time = time.time()
    driver.quit()
    print("\n=== TEST REPORT ===")
    for step, status in test_report:
        print(f"{step}: {status}")
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
