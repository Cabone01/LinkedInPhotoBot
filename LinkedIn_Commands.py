import os
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from bot_token import user, password
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

def get_Message_Contact_Names():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.get('https://www.linkedin.com/')

    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.ID, 'session_key')))

    id_box = driver.find_element('name', 'session_key')
    id_box.send_keys(user)
    id_box = driver.find_element('name', 'session_password')
    id_box.send_keys(password)

    login_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-primary')
    login_button.click()

    # Go to message contacts
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'global-nav__primary-items')))
    icon_list = driver.find_element(By.CLASS_NAME, 'global-nav__primary-items')
    icons = icon_list.find_elements(By.TAG_NAME, "li")
    icons[3].click()

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'msg-conversation-listitem__participant-names')))
    msg_boxs = driver.find_element(By.CLASS_NAME, 'msg-conversations-container--inbox-shortcuts')
    msg_list = msg_boxs.find_elements(By.TAG_NAME, "li")

    msg_names = []
    for msg in msg_list:
        try:
            msg_names.append(msg.find_element(By.CLASS_NAME, 'msg-conversation-card__participant-names').text)
            time.sleep(1)
        except NoSuchElementException:
            pass
    driver.quit()
    return msg_names

def send_Image(name):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.get('https://www.linkedin.com/')

    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.ID, 'session_key')))

    id_box = driver.find_element('name', 'session_key')
    id_box.send_keys(user)
    id_box = driver.find_element('name', 'session_password')
    id_box.send_keys(password)

    login_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-primary')
    login_button.click()

    # Go to message contacts
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'global-nav__primary-items')))
    icon_list = driver.find_element(By.CLASS_NAME, 'global-nav__primary-items')
    icons = icon_list.find_elements(By.TAG_NAME, "li")
    icons[3].click()

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'msg-conversations-container__conversations-list')))
    msg_boxs = driver.find_element(By.CLASS_NAME, 'msg-conversations-container__conversations-list')
    certain_msg = msg_boxs.find_element(By.XPATH, f"//li/div/a/div[2]/div/div[1]/h3[text()='{name}']")
    certain_msg.click()

    drop_box = driver.find_element(By.CLASS_NAME, 'msg-form__attachment-drag-and-drop-content')
    drag_and_drop_file(drop_box, os.getcwd() + f'\\LinkedInPhotoBot\\Images\\image.jpg')
    time.sleep(20)
    driver.find_element(By.CLASS_NAME, 'msg-form__send-button').click()
    time.sleep(3)

    driver.quit()


JS_DROP_FILE = """
    var target = arguments[0],
        offsetX = arguments[1],
        offsetY = arguments[2],
        document = target.ownerDocument || document,
        window = document.defaultView || window;

    var input = document.createElement('INPUT');
    input.type = 'file';
    input.onchange = function () {
      var rect = target.getBoundingClientRect(),
          x = rect.left + (offsetX || (rect.width >> 1)),
          y = rect.top + (offsetY || (rect.height >> 1)),
          dataTransfer = { files: this.files };

      ['dragenter', 'dragover', 'drop'].forEach(function (name) {
        var evt = document.createEvent('MouseEvent');
        evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
        evt.dataTransfer = dataTransfer;
        target.dispatchEvent(evt);
      });

      setTimeout(function () { document.body.removeChild(input); }, 25);
    };
    document.body.appendChild(input);
    return input;
"""

def drag_and_drop_file(drop_target, path):
    driver = drop_target.parent
    file_input = driver.execute_script(JS_DROP_FILE, drop_target, 0, 0)
    file_input.send_keys(path)