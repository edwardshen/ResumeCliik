#!/usr/bin/python
# -*- coding: utf-8 -*

import sys
import MySQLdb
from Config import *
from ArticleParser import *

COLON = u'：'
ADVANTAGES = u'優點:'
DISADVANTAGES = u'缺點:'
ATTACHMENT = u'\n附件\n'
AGE = u'歲'
MALE = u'男性'
FEMALE = u'女性'
ID = u'代碼：'
HIGHEST_DEGREE = u'最高學歷：'
DESIRED_POSITION = u'希望職稱：'
WORKING_YEARS = u'工作經歷：'
HOME_ADDRESS = u'居住地：'
APPLIED_POSITION = u'應徵職務：'
CELLPHONE1 = u'行動1：'
CELLPHONE2 = u'行動2：'
HOME_PHONE = u'家中：'
OFFICE_PHONE = u'公司：'
CONTACT_METHOD = u'聯絡方式：'
APPLIED_JOB_TYPE = u'求職身分：'
CURRENT_JOB_STATUS = u'就業狀態：'
AVAILABLE_WORKING_DAY = u'可上班日：'
DRIVER_LICENSE = u'持有駕照：'
OWNED_CARS = u'自備車輛：'
HEAVY_DUTY_MOTORCYCLE = u'普通重型機車'
LIGHT_MOTORCYCLE = u'輕型機車'
CAR = u'普通小型車'
DATE_OF_RESUME_MODIFICATION = u'履歷修改日：'
BASIC_PROFILE = u'基本資料：'
MARRIED = u'已婚'
UNMARRIED = u'未婚'
YEAR_OF_BIRTH = u'年次'
MILITARY_STATUS = u'兵役狀況：'
NO_NEED_FOR_MILITARY = u'免役'
ENGLISH_NAME = u'英文姓名：'
HEIGHT_AND_WEIGHT = u'身高體重：'
CENTIMETER = u'公分'
KILOGRAM = u'公斤'
DESIRED_POSITION_TYPE = u'希望職務類別：'
DESIRED_INDUSTRY = u'希望從事產業：'
DESIRED_WORKING_LOCATION = u'希望工作地點：'
DESIRED_SALARY = u'希望待遇：'
MONTHLY_PAY = u'月薪'
DOLLAR = u'元'
NO_MIND = u'不拘'
DESIRED_HOLIDAY_PATTERN = u'希望休假制度：'
DESIRED_TITLE = u'希望職務名稱：'
DESIRED_JOB_DESCRIPTION = u'希望職務內容：'
TOTAL_WORKING_EXPERIENCE = u'工作總經驗累計：'
JOB_EXPERIENCE = u'工作經歷'
RECENT_JOB = u'最近工作：'
LAST_ONE_JOB = u'前一工作：'
LAST_TWO_JOB = u'前二工作：'
LAST_THREE_JOB = u'前三工作：'
INDUSTRY_TYPE = u'產業類別：'
COMPANY_SIZE = u'公司規模：'
POSITION_TYPE = u'職務類別：'
MANAGEMENT_RESPONSIBILITY = u'管理責任：'
TITLE = u'職務名稱：'
JOB_DESCRIPTION = u'工作內容：'
HIGHEST_EDUCATION_LEVEL = u'最高教育程度：'
UNIVERSITY = u'大學'
HIGHSCHOOL = u'高中'
HIGHEST = u'最高：'
SECOND_HIGHEST = u'次高：'
LANGUAGE = u'語文：'
DIALECT = u'方言：'
TOOLS = u'擅長工具：'
SKILLS = u'工作技能：'
CERTIFICATES = u'認證資格：'
PERSONAL_BASIC_PROFILE = u'個人基本資料'
DESIRED_JOB_ATTRIBUTES = u'希望求職條件'
TYPING_SPEED = u'中╱英文打字：'
IMAGE_PROCESSING_TOOLS = u'影像處理類：'
ENGLISH_LANGUAGE_CERTIFICATE = u'英語相關證照：'
TOURISM_CERTIFICATE = u'旅遊相關證照：'
EDUCATION_BACKGROUND = u'教育背景'
LANGUAGE_CAPABILITY = u'語文能力'
SKILLS_AND_ABLITIES = u'技能專長'
AUTOBIOGRAPHY = u'自傳'
PERSONAL_AUTOBIOGRAPHY = u'．個人自傳：'
YEAR = u'年'
NOT_ENTERED = u'\u672a\u586b'
CELLPHONE = u'手機'
FULLTIME = u'上班族'
STILL_WORKING = u'仍在職'
INSTANTLY = u'即時'




db = MySQLdb.connect(host=DATABASE_HOST, user=DATABASE_USERID, passwd=DATABASE_PASSWD, db=DATABASE_NAME, charset='utf8', \
				 	use_unicode=True)
				
cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER_SET_CLIENT=utf8;')
cursor.execute('SET CHARACTER_SET_CONNECTION=utf8;')
cursor.execute('SET CHARACTER_SET_RESULTS=utf8;')

def get_main_content_from_raw_email(emailid, table_name=EMAIL_TABLE_NAME):
    sql_command = 'select body from %s where id=%s;'%(table_name, emailid)
    cursor.execute(sql_command)
    body_text = cursor.fetchall()[0][0].replace('\r','\n')

    tags_to_remove = TAGS_TO_REMOVE
    tags_to_remove.update({"td":["<td ",">"], "tr":["<tr ",">"], "table":["<table ",">"], \
							'href':['<a href', ">"],'meta':['<meta ','>']})
    body_text = RemoveTags(body_text, tags_to_remove)
    get_rid_of = ['<tr>', '</tr>', '<td>', '</td>', '</center>', '</body>', '</html>','</head>','<body>','<center>']
    for r in get_rid_of:
        body_text = body_text.replace(r,'')
    while '\n\n\n' in body_text:
        body_text = body_text.replace('\n\n\n','\n')

    body_text = body_text.replace(COLON+'\n\n', COLON).replace(COLON+'\n',COLON)
    main_content_begin = body_text[body_text.find(ADVANTAGES)+10:].find('\n\n')+body_text.find(ADVANTAGES) + 10
    main_content_end = body_text.find(ATTACHMENT)
    main_content = body_text[main_content_begin:main_content_end].lstrip('\n')
    return main_content

def get_applicant_name(main_content):
    return main_content.split(' ')[0]

def get_applicant_age(main_content):
    return int(main_content.replace(AGE,' ').split(' ')[1])

def get_applicant_gender(main_content):
    if MALE==main_content.replace(AGE,'\n').split('\n')[2]:
        return 'M'
    return 'F'

def get_entry(main_content, entry_name):
    return main_content[main_content.find(entry_name)+len(entry_name):].split('\n')[0]

def get_applicant_ID(main_content):
    return int(get_entry(main_content, ID))

def get_applicant_education_level(main_content):
	return get_entry(main_content, HIGHEST_DEGREE).split(' ')
	
def get_applicant_desired_position(main_content):
    return get_entry(main_content, DESIRED_POSITION)

def get_applicant_working_years(main_content):
    return get_entry(main_content, WORKING_YEARS)

def get_applicant_home_address(main_content):
    return get_entry(main_content, HOME_ADDRESS)
	
def get_applied_position(main_content):
    return get_entry(main_content, APPLIED_POSITION)

def get_phone(main_content, phone_type):
    phone = get_entry(main_content, phone_type)
    if phone!=NOT_ENTERED:
        return phone
    return None

def get_applicant_cellphones(main_content):
    return filter(lambda x: x!=None, \
		 (get_phone(main_content, CELLPHONE1), get_phone(main_content, CELLPHONE2)))
		
def get_applicant_home_phone(main_content):
    return get_phone(main_content, HOME_PHONE)

def get_applicant_office_phone(main_content):
    return get_phone(main_content, OFFICE_PHONE)

def get_applicant_contact_info(main_content):
    return get_entry(main_content, CONTACT_METHOD)

def get_applied_job_type(main_content):
    return get_entry(main_content, APPLIED_JOB_TYPE)

def get_applicant_current_job_status(main_content):
    return get_entry(main_content, CURRENT_JOB_STATUS)

def get_applicant_available_working_day(main_content):
    return get_entry(main_content, AVAILABLE_WORKING_DAY)

def get_applicant_driver_licenses(main_content):
    return get_entry(main_content, DRIVER_LICENSE).split(u'\u3001')

def get_applicant_owned_cars(main_content):
    return get_entry(main_content, OWNED_CARS).split(u'\u3001')

def get_resume_modified_date(main_content):
    return get_entry(main_content, DATE_OF_RESUME_MODIFICATION)

def get_applicant_basic_profile(main_content):
    return map(lambda x: x.strip(), get_entry(main_content, BASIC_PROFILE).split('/'))

def get_applicant_military_status(main_content):
    return get_entry(main_content, MILITARY_STATUS)

def get_applicant_height_and_weight(main_content):
    return map(lambda x: x.strip(), get_entry(main_content, HEIGHT_AND_WEIGHT).split('/'))

def get_desired_position_type(main_content):
    return get_entry(main_content, DESIRED_POSITION_TYPE)

def get_desired_industry(main_content):
    return get_entry(main_content, DESIRED_INDUSTRY)

def get_desired_working_locations(main_content):
    return get_entry(main_content, DESIRED_WORKING_LOCATION).split(u'\u3001')

def get_desired_salalry(main_content):
    return map(lambda x: int(x), \
			get_entry(main_content, DESIRED_SALARY).replace(DOLLAR,'').split(' ')[1].split('~'))

def get_desired_holiday_pattern(main_content):
    return get_entry(main_content, DESIRED_HOLIDAY_PATTERN)

def get_desired_title(main_content):
    return get_entry(main_content, DESIRED_TITLE)

def get_desired_job_description(main_content):
    return get_entry(main_content, DESIRED_JOB_DESCRIPTION)

def get_applicant_total_working_experience(main_content):
    return get_entry(main_content, TOTAL_WORKING_EXPERIENCE).strip(YEAR)

def get_job_history(main_content, previous_job_type):
    content = main_content[main_content.find(DESIRED_JOB_ATTRIBUTES)+len(DESIRED_JOB_ATTRIBUTES):]
    begin = content.find(previous_job_type)
    job_history = content[begin:].split('\n\n')[0]
    job_title = get_entry(job_history, previous_job_type)
    industry_type = get_entry(job_history, INDUSTRY_TYPE)
    company_size = get_entry(job_history, COMPANY_SIZE).strip(u'人')
    position_type = get_entry(job_history, POSITION_TYPE)
    management_responsibility = get_entry(job_history, MANAGEMENT_RESPONSIBILITY)
    title = get_entry(job_history, TITLE)
    job_description = get_entry(job_history, JOB_DESCRIPTION)
    return job_title, industry_type, company_size, position_type, management_responsibility, title, job_description

def get_applicant_recent_job(main_content):
    return get_job_history(main_content, RECENT_JOB)

def get_applicant_last1_job(main_content):
    return get_job_history(main_content, LAST_ONE_JOB)

def get_applicant_last2_job(main_content):
    return get_job_history(main_content, LAST_TWO_JOB)

def get_applicant_last3_job(main_content):
    return get_job_history(main_content, LAST_THREE_JOB)

def get_applicant_highest_education_level(main_content):
    return get_entry(main_content, HIGHEST_EDUCATION_LEVEL)

def get_applicant_highest_education(main_content):
    return get_entry(main_content, HIGHEST)

def get_applicant_2nd_highest_education(main_content):
    return get_entry(main_content, SECOND_HIGHEST)

def get_applicant_languages(main_content):
    return get_entry(main_content, LANGUAGE)

def get_applicant_dialects(main_content):
    return get_entry(main_content, DIALECT)

def get_applicant_tools(main_content):
    return get_entry(main_content, TOOLS)

def get_applicant_skills(main_content):
    skills = get_entry(main_content, SKILLS)
    if skills.find(CERTIFICATES)==0:
        return None
    return skills

def get_applicant_certificates(main_content):
    return get_entry(main_content, CERTIFICATES)

def get_applicant_typing_speed(main_content):
    return get_entry(main_content, TYPING_SPEED)

def get_applicant_image_processing_tools(main_content):
    return get_entry(main_content, IMAGE_PROCESSING_TOOLS)

def get_applicant_english_certificates(main_content):
    return get_entry(main_content, ENGLISH_LANGUAGE_CERTIFICATE)

def get_applicant_tourism_certificates(main_content):
    return get_entry(main_content, TOURISM_CERTIFICATE)

def get_applicant_autobiography(main_content):
    return main_content[main_content.find(PERSONAL_AUTOBIOGRAPHY)+len(PERSONAL_AUTOBIOGRAPHY):].split('\n\n')[0]










main_content = get_main_content_from_raw_email(1)

