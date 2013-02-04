from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from helper_base import HelperBase
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait

class WebDriverHelper(object):
    
    def __init__(self, manager):
        self.manager = manager
#        brow2 = self.config['selenium']['browser']
        browser = manager.get_property("selenium")['browser']
        remote_selenium = manager.get_property("selenium")['remote_server'].encode("utf-8") 
        if remote_selenium == "none":
            if browser == "IE":
                self.driver = webdriver.Ie()
                self.driver.maximize_window()
            elif browser == "chrome":
                options = Options();
                options.add_argument("--start-maximized");
                self.driver = webdriver.Chrome(chrome_options = options)
            else:
                self.driver = webdriver.Firefox()
                self.driver.maximize_window()
        else:
            if browser == "IE":
                caps = DesiredCapabilities.INTERNETEXPLORER
                self.driver = webdriver.Remote(remote_selenium, caps)
                self.driver.maximize_window()
            elif browser == "chrome":
                options = Options();
                options.add_argument("--start-maximized"); 
                caps = options.to_capabilities()
                self.driver = webdriver.Remote(remote_selenium, caps)
            else:
                fp = webdriver.FirefoxProfile('ui_tests/firefox_profile_for_selenium')
                caps = DesiredCapabilities.FIREFOX
                self.driver = webdriver.Remote(remote_selenium, caps, browser_profile = fp)
                self.driver.maximize_window()
        self.driver.implicitly_wait(manager.get_property("selenium")['implicit_wait'])
        if manager.get_property("test_object") == 'local_ui':
            self.driver.get(manager.get_property("ui")['local_ui_url'])
        elif manager.get_property("test_object") == 'lom':
            self.driver.get(manager.get_property("ui")['lom_ui_url'])
        else:
            raise Exception ('UI under test is not specified')
    def stop(self):
        self.driver.quit()
        #self.assertEqual([], self.verificationErrors)
        
    def get_driver(self):
        return self.driver
    
    
class WebDriverWrapper(HelperBase):

    def __init__(self, manager):
        super(WebDriverWrapper, self).__init__(manager)
        self.driver = manager.get_webdriver_helper().get_driver()
        
    def open_absolute_url(self, url):
        self.driver.get(url)
        
    def open_url(self, url_part = ''):
        self.driver.get(self.manager.get_property("ui")['local_ui_url'] + url_part)
        
    def find_element(self, locator_type, locator):
        if locator_type == 'id':
            return self.driver.find_element_by_id(locator)
        elif locator_type == 'name':
            return self.driver.find_element_by_name(locator)
        elif locator_type == 'xpath':
            return self.driver.find_element_by_xpath(locator)
        elif locator_type == 'css':
            return self.driver.find_element_by_css_selector(locator)
        elif locator_type == 'link':
            return self.driver.find_element_by_link_text(locator)
        
        
    def wait_for_loading_finished(self, time = 10):
#        if not (self.wait_for_element_present('css', 'div.loading', 1) == None):
#            self.wait_for_element_not_visible('css', 'div.loading', time)
#            
#        try: self.wait_for_element_present('css', 'div.loading', 1)
#        except TimeoutException, e: return
#        self.wait_for_element_not_visible('css', 'div.loading')
        
        try: self.wait_for_element_present('css', 'span.loadingText', 1)
        except TimeoutException, e: return
        self.wait_for_element_not_visible('css', 'span.loadingText')
        
    def is_element_present(self, locator_type, locator):
        try: self.find_element(locator_type, locator)
        except NoSuchElementException, e: return False
        return True
        
    def is_element_not_present(self, locator_type, locator):
        self.driver.implicitly_wait(0)
        if self.is_element_present(locator_type, locator):
            return False
        else:
            return True
        self.driver.implicitly_wait(self.manager.get_property("selenium")['implicit_wait'])
        
    def is_element_enabled(self, locator_type, locator):
        return self.find_element(locator_type, locator).is_enabled()
        
    def is_element_visible(self, locator_type, locator):
        return self.find_element(locator_type, locator).is_displayed()
    
    def type_in(self, locator_type, locator, string):
        self.find_element(locator_type, locator).clear()
        self.find_element(locator_type, locator).send_keys(string)
        
    def click(self, locator_type, locator):
        self.find_element(locator_type, locator).click()
            
    def wait_for_url(self, url):
        bams = self.driver.current_url()
        print bams
        WebDriverWait(self.driver, 10).until(lambda driver : driver.current_url() == url)
        
    def wait_for_element_present(self, locator_type, locator, time = 10):
        element = WebDriverWait(self.driver, time).until(lambda driver : self.find_element(locator_type, locator), 'Element ' + locator + ' not found after ' + str(time) + ' seconds')
        return element
    
    def wait_for_element_not_present(self, locator_type, locator, time = 10):
        element = WebDriverWait(self.driver, time).until(lambda driver : self.is_element_not_present(locator_type, locator))
        return element
    
    def wait_for_element_visible(self, locator_type, locator, time = 10):
        element = WebDriverWait(self.driver, time).until(lambda driver : self.find_element(locator_type, locator).is_displayed())
        return element
    
    def wait_for_element_not_visible(self, locator_type, locator, time = 10):
        element = WebDriverWait(self.driver, time).until_not(lambda driver : self.find_element(locator_type, locator).is_displayed())
        return element
    
    def wait_for_element_enabled(self, locator_type, locator, time = 10):
        element = WebDriverWait(self.driver, time).until(lambda driver : self.find_element(locator_type, locator).is_enabled())
        return element
    
    def get_alert_text(self):
        return self.driver.switch_to_alert().text
    
    def decline_alert(self):
        self.driver.switch_to_alert().dismiss()
    