from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime
from student.models import Student
from department.models import Department
from course.models import Course, CourseHistory

# I'll just use codes for course name for now
# Ass
# Module: selenium
# Inputs: username, password, otp
# Outputs: 
# (Student): major, major2, tot_cred, year
# (Course History) courses
def run():
    # Headless option
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--log-level=3"); # to silence them bois

    # Driver declaration and link
    DRIVER_PATH = r'course_picker/app/chromedriver.exe'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options) # adds options=options for driver for headless
    driver.get('https://cais.kaist.ac.kr/notice')

    # Change language to english
    h1 = driver.find_element(By.ID, 'lien')
    h1.click()

    # My login credentials
    student = Student.objects.filter(student_id='20200846').first()
    username = student.username
    password = student.password

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
    # Insert //*[@id="email"] to use email
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="phone"]'))).click()
    # time.sleep(2) # to avoid the devtools output
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

    # Open school registration tab
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="langKor"]')))
    driver.get('https://cais.kaist.ac.kr/studentProfile')

    # Fetch major and double major
    major = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[2]/table/tbody/tr[4]/td[2]').text
    major2 = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[2]/table/tbody/tr[6]/td').text
    datetime_str = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[2]/table/tbody/tr[5]/td[1]').text
    datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d')
    year = datetime.now().year - datetime_object.year + 1

    print('Major: ' + major)
    print('Major2: ' + major2)
    print('Year: ' + str(year))

    student.year = year
    student.save()

    # Open grade report tab
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="langKor"]')))
    driver.get('https://cais.kaist.ac.kr/grade')

    # List all relevant years
    start_year = datetime_object.year
    current_year = datetime.now().year

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

    # print('\nList of Courses Taken:')
    # for i in courses:
    #     print(i)
    # print('\n')

    # Create a godforsaken list of courses taken
    student2 = Student.objects.filter(student_id='20200846').first()
    student_history = CourseHistory.objects.filter(student=student2)
    if student_history.exists():
        student_history = student_history.first()
    else:
        student_history = CourseHistory(
            student=student2,
        )
        student_history.save()


    print('\nList of Courses Taken:')
    for i in courses:
        if i[0:2] == 'EE':
            department = Department.objects.filter(code='EE').first()
            print('EE course', i, department.code)
        elif i[0:2] == 'CS':
            department = Department.objects.filter(code='CS').first()
            print('CS course', i, department.code)
        else:
            department = Department.objects.filter(code='HSS').first()
            print('HSS courses', i, department.code)

        course = Course.objects.filter(title=i, department=department)
        if course.exists():
            course = course.first()
        else:
            course = Course(
                department=department,
                title=i,
            )
            course.save()

        history = student_history.courses.all()
        if course not in history:
            student_history.courses.add(course)

    student_history.save()
    print('\n')


    # Close driver
    # time.sleep(120)
    driver.close()
    driver.quit()
