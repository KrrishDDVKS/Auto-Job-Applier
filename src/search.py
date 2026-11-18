import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from webdriver_manager.chrome import ChromeDriverManager

from info import extract_resume_data

URL = "https://www.kforce.com/find-work/search-jobs/#/?t=&l=%5B%5D"

# Configure Chrome
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 20)
i=0
try:
    while True:
        i+=1
        # Step 1: Open careers website
        driver.get(URL)

        print("Opened Kforce Careers")

        # Step 2: Wait for the page to load
        wait.until(
            lambda d: d.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        time.sleep(3)

        # Step 3: Find the job search input
        # Inspect the website if these selectors need adjustment.
        search_box = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//input[@placeholder='Search by Job Title or Skill']"
            ))
        )

        # Step 4: Search for AI/ML Engineer
        search_box.clear()
        search_box.send_keys("AI/ML Engineer")
        search_box.send_keys(Keys.ENTER)

        print("Searching for AI/ML Engineer jobs...")

        # Step 5: Wait for search results
        time.sleep(5)
        
        #______________________________________________________________________
        # Iterated for 30 days to find the best job listings and apply to them.
        date = driver.find_elements(
                By.XPATH, '//body[1]/div[2]/div[1]/main[1]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[' + str(i) + ']/h2[1]/span[1]' 
            )

        dates = date[0].text
        dates = datetime.strptime(dates, "%m/%d/%Y")
        print("Job Posting Dates:", dates)
        # current date
        current_date = datetime.strptime(time.strftime("%m/%d/%Y"), "%m/%d/%Y")
        print("Current Date:", current_date)

        if abs((current_date - dates).days) > 30:
            print("Job is older than 30 days. No new job to apply.")
            break
        else:
            print("Job is posted within 30 days. Proceeding to apply.")
            # Step 6: Extract job listings
            job_elements = driver.find_elements(
                By.XPATH, '//li[' + str(i) + ']//h2[1]/a' 
            )
                #""
                #//li[2]//h2[1]
                

            print("\n--- Job Search Results ---\n")

            seen = set()

            for job in job_elements:
                title = job.text.strip()
                link = job.get_attribute("href")

                if title and link and link not in seen:
                    seen.add(link)

                    print("Job Title:", title)
                    print("Job URL:", link)
                    print("-" * 60)

                    job.click()
                    time.sleep(3)

                if i==1:
                    cookie_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((
                        By.ID, "onetrust-accept-btn-handler"
                    )))

                    cookie_button.click()
                    print("Cookies accepted")

                job_elements = driver.find_elements(
                                By.XPATH, '//button[@id="TK_WIDGET_INITIATOR"]'
                            )
                for button in job_elements:
                    if button.is_displayed():
                        button.click()
                        time.sleep(2)
                        break


                apply_now = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((
                By.XPATH,'//a[@onclick="TK.redirectToLinkRequest(\'form\',\'form\')"]'
                #"//*[self::a or self::button][contains(normalize-space(.), 'Apply Now')]"
                )))

                # Step 3: Click Apply Now
                apply_now.click()

                file_path = "C:/Users/Krishna Desaboina/TC/TC Project/autoapply 1/config/resume.docx"

                data = extract_resume_data(file_path)
                time.sleep(3)
                driver.find_element(By.XPATH, "//input[@id='firstName']").send_keys(data["First name"])
                driver.find_element(By.XPATH, "//input[@id='lastName']").send_keys(data["Last name"])
                driver.find_element(By.XPATH, "//input[@id='emailAddress']").send_keys(data["email"])
                driver.find_element(By.XPATH, "//input[@id='emailAddressVerify']").send_keys(data["email"])
                driver.find_element(By.XPATH, "//input[@id='phoneNumberAll']").send_keys(data["Phone"])
                state_dropdown = driver.find_element(By.XPATH, "//select[@id='state']")
                select = Select(state_dropdown)
                select.select_by_visible_text("Georgia")
                
                driver.find_element(By.XPATH, "//input[@id='postalCode']").send_keys(data["Zip"])

                upload_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@id='uploadFileSystemResume']")
                ))
                upload_element.send_keys(file_path)

                checkbox = driver.find_element(By.XPATH, "//input[@id='eligibility0']")
                time.sleep(5)
                if not checkbox.is_selected():
                    checkbox.click()

                job_elements = driver.find_elements(
                                        By.XPATH, '//input[@id="SubmitButton"]'
                                    )
                for button in job_elements:
                    if button.is_displayed():
                        button.click()
                        time.sleep(2)
                        break

                    
    # Step 7: Keep browser open for inspection
    input("\nPress Enter to close the browser...")

finally:
    driver.quit()
