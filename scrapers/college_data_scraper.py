import bs4
import json
import unidecode
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# write to json function
def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

# replace all those if statements with this clean function sOON
def objectExists(x):
    if (x != None):
        return x.span.text
    else:
        return ''

# path and name of file 
path = './'
fileName = 'college-data-18'
data = {}

urls = ['https://www.niche.com/colleges/georgia-institute-of-technology/']

print(len(urls))

counter = 1
for url in urls:
    print(counter)
    counter += 1
    my_url = url
    print(my_url)

    # opening connection, grabbing page
    uClient = uReq(my_url)

    # offloads content to a variable
    page_html = uClient.read()

    # closes connection
    uClient.close()

    # html parsing
    page_soup = soup(page_html, "html.parser")

    # name of college
    college_name = page_soup.h1.text
    data[college_name] = {}

    # 'niche report card' or 'niche grade'
    report_card = page_soup.find("div", {"class": "report-card"})
    grades = report_card.findAll("li", {"class": "ordered__list__bucket__item"})
    # dictionary in dictionary for niche report card
    data[college_name]["niche_report_card"] = {}
    for grade in grades:
        grade_label = grade.div.select('div')[0].text
        grade_val = grade.div.select('div')[1].text
        data[college_name]["niche_report_card"][grade_label] = grade_val

    # 'after college'
    after_college = page_soup.find("section", {"id": "after"})
    data[college_name]["after_college"] = {}

    # median earning after 6 years of college
    median_earning_6_years = after_college.find("div", {"class": "profile__bucket--1"}).div.div.div.find("div", {"class": "scalar__value"})
    if (median_earning_6_years != None):
        median_earning_6_years = median_earning_6_years.span.text
    else:
        median_earning_6_years = ''
    data[college_name]["after_college"]["median_earning_6_years"] = median_earning_6_years

    # other after college rates
    other_after_college_rates = after_college.find("div", {"class": "profile__bucket--2"}).div.div.findAll(recursive=False)

    # graduation rate
    graduation_rate = other_after_college_rates[0].find("div", {"class": "scalar__value"})
    if (graduation_rate != None):
        graduation_rate = graduation_rate.span.text
    else:
        graduation_rate = ''
    data[college_name]["after_college"]["graduation_rate"] = graduation_rate

    # employment rate
    employment_rate = other_after_college_rates[1].find("div", {"class": "scalar__value"})
    if (employment_rate != None):
        employment_rate = employment_rate.span.text
    else:
        employment_rate = ''
    data[college_name]["after_college"]["employment_rate"] = employment_rate

    # 'students'
    data[college_name]["students"] = {}

    students_enrolled = page_soup.find("section", {"id": "students"}).find("div", {"class": "profile__bucket--1"}).div.div.findAll(recursive=False)
    # full time
    full_time = students_enrolled[0].find("div", {"class": "scalar__value"})
    if (full_time != None):
        full_time = full_time.span.text
    else:
        full_time = ''

    # part time
    part_time = students_enrolled[1].find("div", {"class": "scalar__value"})
    if (part_time != None):
        part_time = part_time.span.text
    else:
        part_time = ''

    # over 25
    over_25 = students_enrolled[2].find("div", {"class": "scalar__value"})
    if (over_25 != None):
        over_25 = over_25.span.text
    else:
        over_25 = ''

    # pell grant
    pell_grant = students_enrolled[3].find("div", {"class": "scalar__value"})
    if (pell_grant != None):
        pell_grant = pell_grant.span.text
    else:
        pell_grant = ''

    # varsity athletes
    varsity_athletes = students_enrolled[4].find("div", {"class": "scalar__value"})
    if (varsity_athletes != None):
        varsity_athletes = varsity_athletes.span.text
    else:
        varsity_athletes = ''

    data[college_name]["students"]["full_time"] = full_time
    data[college_name]["students"]["part_time"] = part_time
    data[college_name]["students"]["over_25"] = over_25
    data[college_name]["students"]["pell_grant"] = pell_grant
    data[college_name]["students"]["varsity_athletes"] = varsity_athletes

    # 'majors'
    data[college_name]["popular_majors"] = []
    majors = page_soup.find("section", {"id": "majors"}).find("ul", {"class": "popular-entities-list"})
    if (majors != None):
        majors = majors.findAll("li")
        for major in majors:
            data[college_name]["popular_majors"].append(major.h6.string)
    else:
        majors = ''

    # 'cost'
    data[college_name]["cost"] = {}
    cost = page_soup.find("section", {"id": "cost"})

    # net price
    net_price = cost.find("div", {"class": "profile__bucket--1"}).find("div", {"class": "scalar__value"})
    if (net_price != None):
        net_price = net_price.span.text
    else:
        net_price = ''
    data[college_name]["cost"]["net_price"] = net_price

    # aid
    aid = cost.find("div", {"class": "profile__bucket--2"}).div.div.findAll(recursive=False)
    average_aid = aid[0].find("div", {"class": "scalar__value"})
    if (average_aid != None):
        average_aid = average_aid.span.text
    else:
        average_aid = ''

    percentage_aid = aid[1].find("div", {"class": "scalar__value"})
    if (percentage_aid != None):
        percentage_aid = percentage_aid.span.text
    else:
        percentage_aid = ''

    data[college_name]["cost"]["average_aid"] = average_aid
    data[college_name]["cost"]["percentage_aid"] = percentage_aid

    # 'admissions'
    data[college_name]["admissions"] = {}

    my_url = url + 'admissions'
    print(my_url)
    # opening connection, grabbing page
    uClient = uReq(my_url)
    # offloads content to a variable
    page_html = uClient.read()
    # closes connection
    uClient.close()
    # html parsing
    page_soup = soup(page_html, "html.parser")

    # 'statistics'
    data[college_name]["admissions"]["statistics"] = {}

    statistics = page_soup.find("section", {"id": "admissions-statistics"})
    if (statistics != None):
        statistics = page_soup.find("section", {"id": "admissions-statistics"}).find("div", {"class": "profile__buckets"})
    else:
        continue

    # acceptance rate
    acceptance_rate = statistics.find("div", {"class": "profile__bucket--1"}).div.div
    if (acceptance_rate.select('div')[2] != None):
        acceptance_rate = acceptance_rate.select('div')[2].span.text
    else:
        acceptance_rate = ''
    data[college_name]["admissions"]["statistics"]["acceptance_rate"] = acceptance_rate

    # early decision acceptance rate
    other_stats = statistics.find("div", {"class": "profile__bucket--2"}).div.div.findAll(recursive=False)
    early_decision_acceptance_rate = other_stats[0].find("div", {"class": "scalar__value"})
    if (early_decision_acceptance_rate != None):
        data[college_name]["admissions"]["statistics"]["early_decision_acceptance_rate"] = early_decision_acceptance_rate.span.text
    else:
        data[college_name]["admissions"]["statistics"]["early_decision_acceptance_rate"] = ''

    # total applicants
    total_applicants = other_stats[1].find("div", {"class": "scalar__value"})
    if (total_applicants != None):
        data[college_name]["admissions"]["statistics"]["total_applicants"] = total_applicants.span.text
    else:
        data[college_name]["admissions"]["statistics"]["total_applicants"] = ''

    # write to json
    writeToJSONFile(path, fileName, data)
