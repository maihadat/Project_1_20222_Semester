import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
import mysql.connector
from Sorter import Sorter
from Cloud_Service import CloudService
from Utilities import *


class Crawler:
    def __init__(self):
        self.sources = ["https://www.getapp.com/collaboration-software/cloud-storage/?sort=reviews",
                        "https://www.getapp.com/collaboration-software/cloud-storage/?sort=reviews&page=2"]
        self.browser = webdriver.Chrome(executable_path="chromedriver.exe")
        self.links, self.names = [], []
        for source in self.sources:
            self.browser = webdriver.Chrome(executable_path="chromedriver.exe")
            self.browser.get(source)
            links, names = find_links(self.browser)
            self.links += links
            self.names += names
            sleep(random.randint(1, 7))
            self.browser.quit()
        self.list_of_services = []
        self.number_of_crawled_service = 1
        self.process = str(int(self.number_of_crawled_service)) + "/" + str(len(self.links))

    def crawl_by_css(self, css_selector, class_name):
        Typical_customer = self.browser.find_element(By.CSS_SELECTOR, css_selector)
        child_elements = Typical_customer.find_elements(By.CLASS_NAME, class_name)
        properties = []
        for child_element in child_elements:
            text = child_element.text
            properties.append(text)
        return properties

    def crawl(self):
        self.number_of_crawled_service = 1
        for (link, name) in zip(self.links, self.names):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:19]
            sleep(random.randint(1, 5))
            self.browser.quit()
            self.browser = webdriver.Chrome(executable_path="chromedriver.exe")
            self.browser.get(link)
            sleep(random.randint(1, 10))
            # Infomation about the service
            try:
                Typical_customer_selector = "#__next > div:nth-child(3) > div.Container.Container_root__cvVXt.ListingDetail_pageContentContainer__e9LcS.Container_fixedWidth__9MCq_ " \
                                        "> section.Overall > div > div.Grid.Main.Main_root__3LWPm.Grid_col-xs-true__1M56J > div >" \
                                        " div.Grid.Overall_container__QjbAv.Grid_col-xs-12__ND1vj.Grid_col-lg-4__zKMFd > div > div:nth-child(1)"
                Platform_supported_selector = "#__next > div:nth-child(3) > div.Container.Container_root__cvVXt.ListingDetail_pageContentContainer__e9LcS.Container_fixedWidth__9MCq_ " \
                                          "> section.Overall > div > div.Grid.Main.Main_root__3LWPm.Grid_col-xs-true__1M56J > div " \
                                          "> div.Grid.Overall_container__QjbAv.Grid_col-xs-12__ND1vj.Grid_col-lg-4__zKMFd > div > div:nth-child(2)"
                Support_options_selector = "#__next > div:nth-child(3) > div.Container.Container_root__cvVXt.ListingDetail_pageContentContainer__e9LcS.Container_fixedWidth__9MCq_ " \
                                       "> section.Overall > div > div.Grid.Main.Main_root__3LWPm.Grid_col-xs-true__1M56J > div " \
                                       "> div.Grid.Overall_container__QjbAv.Grid_col-xs-12__ND1vj.Grid_col-lg-4__zKMFd > div > div:nth-child(3)"
                Training_options_selector = "#__next > div:nth-child(3) > div.Container.Container_root__cvVXt.ListingDetail_pageContentContainer__e9LcS.Container_fixedWidth__9MCq_ " \
                                        "> section.Overall > div > div.Grid.Main.Main_root__3LWPm.Grid_col-xs-true__1M56J > div " \
                                        "> div.Grid.Overall_container__QjbAv.Grid_col-xs-12__ND1vj.Grid_col-lg-4__zKMFd > div > div:nth-child(4)"
                typical = "\n".join(self.crawl_by_css(Typical_customer_selector, "FeaturesCheck_content__cJa2L"))
                platform = "\n".join(self.crawl_by_css(Platform_supported_selector, "FeaturesCheck_content__cJa2L"))
                support = "\n".join(self.crawl_by_css(Support_options_selector, "FeaturesCheck_content__cJa2L"))
                training = "\n".join(self.crawl_by_css(Training_options_selector, "FeaturesCheck_content__cJa2L"))
            except:
                typical = "None"
                platform = "None"
                support = "None"
                training = "None"

            # Service star rating
            try:
                star_css = "#__next > div:nth-child(3) > div.Container.Container_root__cvVXt.ListingDetail_pageContentContainer__e9LcS.Container_fixedWidth__9MCq_" \
                       "> section.Reviews > div.Grid.Section.Section_root__B71eD.Grid_row__m5vnn > div.Grid.Main.Main_root__3LWPm.Grid_col-xs-true__1M56J" \
                       "> div.Grid.Grid_row__m5vnn.Grid_spacing-3__PFJAb > div.Grid.Summary,Grid_col-xs-12__ND1vj.Grid_col-lg-4__zKMFd" \
                       "> div.Summary_container__5qKGF > div.Summary_item__9TgSZ > div.Grid.Grid_row__m5vnn" \
                       "> div:nth-child(1) > div.Display.Display_root__vNrF9.Display_large__UkiCx" \
                       "> div.Display.Display_root__Z5mts > div.Display.Display_root__7jjFS.Display_large__zqddJ > p.Typography.Typography_root__Zc3Hi.Typography_display-md__giFHF"
                cr_star = self.browser.find_element(By.CSS_SELECTOR, star_css)
                star = cr_star.text.split("\n")
                if star[0] == "Overall Rating":
                    star = star[1]
            except:
                star = 0

            # Service reviews crawling
            try:
                reviews = []
                review_column_selector = "#__next > div:nth-child(3) > div.Container.Container_root__cvVXt.ListingDetail_pageContentContainer__e9LcS.Container_fixedWidth__9MCq_" \
                                     "> section.Reviews > div.Grid.Section.Section_root__B71eD.Grid_row__m5vnn > div.Grid.Main.Main_root__3LWPm.Grid_col-xs-true__1M56J" \
                                     "> div.Grid.Grid_row__m5vnn.Grid_spacing-3__PFJAb > div.Grid.Content.Content_root__YIMPO.Grid_col-xs-12__ND1vj.Grid_col-lg-8__1ihR9" \
                                     "> div.Content_item__CNpuO > div.Reviews_content___KMzz > div:nth-child(3) > div.Grid.Grid_row__m5vnn.Grid_spacing-3__PFJAb" \
                                     "> div.Grid.Grid_col-xs-12__ND1vj.Grid_col-sm-6__ZR6WW"
                crawl_columns = self.browser.find_elements(By.CSS_SELECTOR, review_column_selector)
                review_block_selector = "div.Reviews_snippets__DPrmF > div.Snippet.Snippet_snippet__FVSFz.Snippet_snippetLarge__0gxbA"
                review_selector = "div.Snippet_snippetContainer__EaGBC.Snippet_snippetContainerPadding__hb70r > div.Typography.Typography_root__Zc3Hi.Typography_body-xs__nszN9.Snippet_snippetText__HYcIL"
                for crawl_column in crawl_columns:
                    crawl_blocks = crawl_column.find_elements(By.CSS_SELECTOR, review_block_selector)
                    for crawl_block in crawl_blocks:
                        review = crawl_block.find_element(By.CSS_SELECTOR, review_selector).text.replace("\n", ".")
                        reviews.append(review)
            except:
                reviews = ["", "", "", "", "", ""]

            # Pricing crawling
            sleep(random.randint(1, 10))
            self.browser.quit()
            self.browser = webdriver.Chrome(executable_path="chromedriver.exe")
            self.browser.get(link+'pricing/')
            try:
                pricing_selector = "#__next > div:nth-child(3) > div.Pricing.Pricing_root__oNiLs > div.Container.Container_root__cvVXt.Pricing_pageContentContainer__BoxJj.Container_fixedWidth__9MCq_ " \
                                        "> div.Paper.ListingCard.PricingOverview.PricingOverview_root__an9V5.Paper_root__5E4PB.Paper_elevation-1__sJMjC > div.Grid.Grid_row__m5vnn.Grid_spacing-4__D9_Rf" \
                                        " div.Grid.Grid_col-xs-12__ND1vj.Grid_col-md-8__yhjOh.Grid_col-lg-4__zKMFd > div.PricingOverview_spaceRight__WB3n9.PricingOverview_spaceLeft__nVfTt" \
                                        "> div.PricingVendor.PricingVendor_root__aB9b2 > div"
                cr_price = self.crawl_by_css(pricing_selector, "PricingVendor_vendorDescription__evtXX")
                price = cr_price[0]
                #price = cr_price.replace('\n', '')
            except:
                price = "None"
            tmp = CloudService(self.number_of_crawled_service, name, [typical, platform, support, training], price, reviews, float(star), now)
            self.list_of_services.append(tmp)
            print('Crawled ' + str(self.number_of_crawled_service) + ' services.')
            if self.number_of_crawled_service < len(self.links):
                self.number_of_crawled_service += 1
            sleep(random.randint(1, 5))


if __name__=="__main__":
    database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="qwedfgbnm123")
    schema = 'project1_database'
    cursor = database.cursor()
    cursor.execute('USE ' + schema)
    sql_command = "CREATE TABLE review(" \
                  "review_id INT PRIMARY KEY," \
                  "good_review TEXT," \
                  "bad_review TEXT);" \
                  "" \
                  "CREATE TABLE typical_customer(" \
                  "customer_id INT PRIMARY KEY," \
                  "customer TEXT" \
                  ");" \
                  "" \
                  "CREATE TABLE platform (" \
                  "platform_id INT PRIMARY KEY," \
                  "platform TEXT" \
                  ");" \
                  "" \
                  "CREATE TABLE support_options(" \
                  "support_id INT PRIMARY KEY," \
                  "sp_option TEXT" \
                  ");" \
                  "" \
                  "CREATE TABLE training_option(" \
                  "training_id INT PRIMARY KEY," \
                  "tr_option TEXT" \
                  ");" \
                  "" \
                  "CREATE TABLE info(" \
                  "info_id INT PRIMARY KEY," \
                  "customer_id INT," \
                  "platform_id INT, " \
                  "support_id INT," \
                  "training_id INT," \
                  "FOREIGN KEY(customer_id) REFERENCES typical_customer(customer_id)," \
                  "FOREIGN KEY(platform_id) REFERENCES platform(platform_id)," \
                  "FOREIGN KEY(support_id) REFERENCES support_options(support_id)," \
                  "FOREIGN KEY(training_id) REFERENCES training_option(training_id)" \
                  ");" \
                  "" \
                  "CREATE TABLE service(" \
                  "service_id INT PRIMARY KEY," \
                  "name TEXT," \
                  "review_id INT," \
                  "info_id INT," \
                  "price TEXT," \
                  "star FLOAT," \
                  "date_time DATETIME," \
                  "security_service TEXT," \
                  "FOREIGN KEY(review_id) REFERENCES review(review_id)," \
                  "FOREIGN KEY(info_id) REFERENCES info(info_id)" \
                  ");"
    cursor.execute(sql_command)
    database.commit()
    crawler = Crawler()
    crawler.crawl()
    sort = Sorter(crawler.list_of_services)
    sort.sort()
    insert_info_ele(sort.training, 'training_option')
    insert_info_ele(sort.support, 'support_options')
    insert_info_ele(sort.typical, 'typical_customer')
    insert_info_ele(sort.platform, 'platform')
    insert_info_service_review(sort.reviews, 'review')
    insert_info_service_review(sort.info, 'info')
    insert_info_service_review(sort.service, 'service')




