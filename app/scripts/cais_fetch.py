from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import datetime


from department.models import Department
from course.models import Course, Class, CourseHistory
from student.models import Student

# Create your views here.

# Module: selenium
# Inputs: username, password, otp
# Outputs: tot_cred, courses
def run():
    # Headless option
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--log-level=3"); # to silence driver

    # Driver declaration and link
    DRIVER_PATH = r'course_picker/app/chromedriver.exe'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options) # adds options=options for driver for headless
    driver.get('https://cais.kaist.ac.kr/notice')

    # Change language to english
    h1 = driver.find_element(By.ID, 'lien')
    h1.click()

    # My login credentials
    username = '##################'
    password = '##################'

    # Insert user name and continue
    h2 = driver.find_element(By.ID, 'IdInput')
    h3 = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/fieldset/ul/li[2]/input[2]')

    h2.send_keys(username)
    h3.click()

    # Insert password and continue
    h4 = driver.find_element(By.ID, 'passwordInput')
    h5 = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/fieldset/ul/li[3]/input[2]')

    h4.send_keys(password)
    h5.click()

    # 2-step authentication
    # This time, you can input the OTP from terminal
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="email"]'))).click()
    time.sleep(2) # to avoid the devtools output
    print('\n==========================')
    otp = input('OTP Code: ')
    print('==========================\n')

    # Then, insert the OTP code
    h6 = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/fieldset/ul/li[4]/input')
    h7 = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/fieldset/ul/li[5]/input')

    h6.send_keys(otp)
    h7.click()

    # Wait until the title of the CAIS page appears
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="head"]/a')))

    # Try changing language to English
    try:
        lang_eng = driver.find_element(By.XPATH, '//*[@id="langEng"]')
        lang_eng.click()
    except NoSuchElementException:
        print('The page is already in English')

    # Open grade report tab
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="langKor"]')))
    driver.get('https://cais.kaist.ac.kr/grade')

    # List all relevant years
    start_year = 2020
    current_year = datetime.date.today().year

    list = []
    courses = []

    list.append(str(0))
    for i in range(start_year, current_year + 1):
        list.append(str(i))

    # Fetch total credits and courses taken
    tot_cred = driver.find_element(By.XPATH, '//*[@id="gradeContent"]/table[1]/tbody/tr/td[2]').text

    for year in list:
        temp = driver.find_elements(By.XPATH, '//*[@id="'+year+'"]/td[4]') # find_elements, not find_element
        for i in (temp):
            courses.append(i.text)

    # Print total credits and courses taken
    print('Total credits: ' + tot_cred)

    print('\nList of Courses Taken:')
    student = Student.objects.filter(username='timmy').first()
    print(student.name)
    student_history = CourseHistory(
        student=student,
    )
    student_history.save()

    for i in courses:
        if i[0:3] == 'HSS':
            department = Department.objects.filter(code='HSS').first()
            print('HSS course', i, department.code)
        elif i[0:2] == 'CS':
            department = Department.objects.filter(code='CS').first()
            print('CS course', i, department.code)
        else:
            department = Department.objects.filter(code='Other').first()
            print('Other courses', i, department.code)

        course = Course.objects.filter(title=i, department=department)
        if course.exists():
            course = course.first()
        else:
            course = Course(
                department=department,
                title=i,
            )
            course.save()

        student_history.courses.add(course)

    student_history.save()

    print('\n')

    # Close driver
    time.sleep(120)
    driver.close()
    driver.quit()
