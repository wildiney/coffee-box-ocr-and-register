from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from config.config import config
import sys
import platform
import time


class Dolce_gusto:
    def timer(self, timer):
        for t in range(timer):
            print("loading data - " + str(timer-t), end="\r")
            time.sleep(2)

    @staticmethod
    def write_file(content, output, mode="a"):
        print("Writing File...", end="\r")
        with open(output, mode) as f:
            f.writelines(content)

    def access(self, file):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")

        if platform.system() == 'Darwin':
            chrome_driver = r"{}/resources/chromedriver" \
                .format(config['basedir'])
        elif platform.system() == 'Windows':
            chrome_driver = r"{}/resources/chromedriver.exe" \
                .format(config['basedir'])
        else:
            sys.exit('Platform not supported')

        browser = webdriver.Chrome(options=chrome_options,
                                   executable_path=chrome_driver)
        browser.get(
            "https://www.nescafe-dolcegusto.com.br/customer/account/login/")
        self.timer(5)

        browser.find_element_by_xpath(
            """/html/body/div[4]/div/div[2]/div/section/div/form/div[1]/div[2]/div/ul/li[1]/div/input"""
        ).send_keys(config["login_dg"])
        browser.find_element_by_xpath(
            """/html/body/div[4]/div/div[2]/div/section/div/form/div[1]/div[2]/div/ul/li[2]/div/input""").send_keys(config["pass_dg"])
        browser.find_element_by_xpath(
            """/html/body/div[4]/div/div[2]/div/section/div/form/div[2]/div[2]/div/button""").click()
        self.timer(5)

        browser.get("https://www.nescafe-dolcegusto.com.br/mybonus/")
        self.timer(5)

        with open(file) as f:
            for line in f:
                if line not in ["\r", "\r\n"]:
                    code = line.replace("\n", "")
                    code = code.replace(" ", "")

                    pontos = browser.find_element_by_xpath(
                        """/html/body/div[4]/div/div[2]/div[1]/div[1]/div[4]/section/div[2]/div[3]/div/div"""
                    ).get_attribute("aria-label")
                    print(pontos)

                    browser.find_element_by_xpath(
                        """//*[@id="coupon_code"]"""
                    ).send_keys(code)
                    browser.find_element_by_xpath(
                        """//*[@id="pcm-codes-form"]/div/div[1]/div/div/button""").click()
                    self.timer(5)

                    try:
                        mes_elem = browser.find_element_by_xpath(
                            """/html/body/div[4]/div/div[2]/div[1]/div[1]/div[4]/section/div[2]/ul/li/ul"""
                        )
                        messages = mes_elem.find_elements_by_tag_name("li")
                        # for message in messages:
                        #     print(code, message.text, sep=',')
                        print(code, messages[0].text, sep=',')
                        self.write_file(
                            code + "," + messages[0].text + "\r",
                            config["file_to_save_results"]
                        )
                        self.timer(4)
                    except NoSuchElementException as e:
                        print(code, e.msg, sep=',')
                        self.write_file(
                            code + "," + e.msg + "\r",
                            config["file_to_save_results"]
                        )
                        # print(code, "ok", sep=',')
                        self.timer(4)
        browser.quit()


dg = Dolce_gusto()
dg.access("codes.csv")
