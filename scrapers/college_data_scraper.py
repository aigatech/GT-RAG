import bs4
import json
import unidecode
from progressbar import progressbar2

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# progressbar object
pbar = ProgressBar()

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
for url in pbar(urls):
	print(counter)
	counter += 1
	my_url = url
	print(my_url)


	# opening connection, grabbing page
	uClient = uReq(my_url)

	#offloads content to a variable
	page_html = uClient.read()

	# closes connection
	uClient.close()

	# html parsing
	page_soup = soup(page_html, "html.parser")

	# name of college
	college_name = page_soup.h1.text
	data[college_name] = {}



	# 'niche report card' or 'niche grade'
	report_card = page_soup.find("div", {"class":"report-card"})
	grades = report_card.findAll("li", {"class":"ordered__list__bucket__item"})
	# dictionary in dictionary for niche report card
	data[college_name]["niche_report_card"] = {}
	for grade in grades:
		grade_label = grade.div.select('div')[0].text
		grade_val = grade.div.select('div')[1].text
		data[college_name]["niche_report_card"][grade_label] = grade_val



	# 'after college'
	after_college = page_soup.find("section", {"id":"after"})
	data[college_name]["after_college"] = {}

	# median earning after 6 years of college
	median_earning_6_years = after_college.find("div", {"class":"profile__bucket--1"}).div.div.div.find("div", {"class":"scalar__value"})
	if (median_earning_6_years != None):
		median_earning_6_years = median_earning_6_years.span.text
	else:
		median_earning_6_years = ''
	data[college_name]["after_college"]["median_earning_6_years"] = median_earning_6_years

	# other after college rates
	other_after_college_rates = after_college.find("div", {"class":"profile__bucket--2"}).div.div.findAll(recursive=False)
	
	# graduation rate
	graduation_rate = other_after_college_rates[0].find("div", {"class":"scalar__value"})
	if (graduation_rate != None):
		graduation_rate = graduation_rate.span.text
	else:
		employment_rate = ''
	data[college_name]["after_college"]["graduation_rate"] = graduation_rate

	# employment rate
	employment_rate = other_after_college_rates[1].find("div", {"class":"scalar__value"})
	if (employment_rate != None):
		employment_rate = employment_rate.span.text
	else:
		employment_rate = ''
	data[college_name]["after_college"]["employment_rate"] = employment_rate
	
	

	# 'students'
	data[college_name]["students"] = {}

	students_enrolled = page_soup.find("section", {"id":"students"}).find("div", {"class":"profile__bucket--1"}).div.div.findAll(recursive=False)
	# full time
	full_time = students_enrolled[0].find("div", {"class":"scalar__value"})
	if (full_time != None):
		full_time = full_time.span.text
	else:
		full_time = ''
	
	# part time
	part_time = students_enrolled[1].find("div", {"class":"scalar__value"})
	if (part_time != None):
		part_time = part_time.span.text
	else:
		part_time = ''
	
	# over 25
	over_25 = students_enrolled[2].find("div", {"class":"scalar__value"})
	if (over_25 != None):
		over_25 = over_25.span.text
	else:
		over_25 = ''
	
	# pell grant
	pell_grant = students_enrolled[3].find("div", {"class":"scalar__value"})
	if (pell_grant != None):
		pell_grant = pell_grant.span.text
	else:
		pell_grant = ''

	# varsity athletes
	varsity_athletes = students_enrolled[4].find("div", {"class":"scalar__value"})
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
	majors = page_soup.find("section", {"id":"majors"}).find("ul", {"class":"popular-entities-list"})
	if (majors != None):
		majors = majors.findAll("li")
		for major in majors:
			data[college_name]["popular_majors"].append(major.h6.string)
	else:
		majors = ''

	# 'cost'
	data[college_name]["cost"] = {}
	cost = page_soup.find("section", {"id":"cost"})

	# net price
	net_price = cost.find("div", {"class":"profile__bucket--1"}).find("div", {"class":"scalar__value"})
	if (net_price != None):
		net_price = net_price.span.text
	else:
		net_price = ''
	data[college_name]["cost"]["net_price"] = net_price

	# aid
	aid = cost.find("div", {"class":"profile__bucket--2"}).div.div.findAll(recursive=False)
	average_aid = aid[0].find("div", {"class":"scalar__value"})
	if (average_aid != None):
		average_aid = average_aid.span.text
	else:
		average_aid = ''
	
	percentage_aid = aid[1].find("div", {"class":"scalar__value"})
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
	#offloads content to a variable
	page_html = uClient.read()
	# closes connection
	uClient.close()
	# html parsing
	page_soup = soup(page_html, "html.parser")



	# 'statistics'
	data[college_name]["admissions"]["statistics"] = {}
	
	statistics = page_soup.find("section", {"id":"admissions-statistics"})
	if (statistics !=  None):
		statistics = page_soup.find("section", {"id":"admissions-statistics"}).find("div", {"class":"profile__buckets"})
	else:
		continue

	# acceptance rate
	acceptance_rate = statistics.find("div", {"class":"profile__bucket--1"}).div.div
	if (acceptance_rate.select('div')[2] != None):
		acceptance_rate = acceptance_rate.select('div')[2].span.text
	else:
		acceptance_rate = ''
	data[college_name]["admissions"]["statistics"]["acceptance_rate"] = acceptance_rate

	# early decision acceptance rate
	other_stats =  statistics.find("div", {"class":"profile__bucket--2"}).div.div.findAll(recursive=False)
	early_decision_acceptance_rate = other_stats[0].find("div", {"class":"scalar__value"})
	if (early_decision_acceptance_rate != None):
		data[college_name]["admissions"]["statistics"]["early_decision_acceptance_rate"] = early_decision_acceptance_rate.span.text
	else:
		data[college_name]["admissions"]["statistics"]["early_decision_acceptance_rate"] = ''

	# total applicants
	total_applicants = other_stats[1].find("div", {"class":"scalar__value"})
	if (total_applicants != None):
		data[college_name]["admissions"]["statistics"]["total_applicants"] = total_applicants.span.text
	else:
		data[college_name]["admissions"]["statistics"]["total_applicants"] = ''
	

	# sat 
	sat = statistics.find("div", {"class":"profile__bucket--3"}).div.div.findAll(recursive=False)

	# sat range
	sat_range = sat[0].find("div", {"class":"scalar__value"})
	if (sat_range != None):
		data[college_name]["admissions"]["statistics"]["sat_range"] = sat_range.span.text
	else:
		data[college_name]["admissions"]["statistics"]["sat_range"] = ''

	# sat reading
	sat_reading = sat[1].find("div", {"class":"scalar__value"})
	if (sat_reading != None):
		data[college_name]["admissions"]["statistics"]["sat_reading"] = sat_reading.span.text
	else:
		data[college_name]["admissions"]["statistics"]["sat_reading"] = ''
		
	# sat math
	sat_math = sat[2].find("div", {"class":"scalar__value"})
	if (sat_math != None):
		data[college_name]["admissions"]["statistics"]["sat_math"] = sat_math.span.text
	else:
		data[college_name]["admissions"]["statistics"]["sat_math"] = ''

	# sat submission percentage
	sat_submission_percentage = sat[3].find("div", {"class":"scalar__value"})
	if (sat_submission_percentage != None):
		data[college_name]["admissions"]["statistics"]["sat_submission_percentage"] = sat_submission_percentage.span.text
	else:
		data[college_name]["admissions"]["statistics"]["sat_submission_percentage"] = ''


	# act
	act = statistics.find("div", {"class":"profile__bucket--4"}).div.div.findAll(recursive=False)

	# act range
	act_range = act[0].find("div", {"class":"scalar__value"})
	if (act_range != None):
		data[college_name]["admissions"]["statistics"]["act_range"] = act_range.span.text
	else:
		data[college_name]["admissions"]["statistics"]["act_range"] = ''
	
	# act english
	act_english = act[1].find("div", {"class":"scalar__value"})
	if (act_english != None):
		data[college_name]["admissions"]["statistics"]["act_english"] = act_english.span.text
	else:
		data[college_name]["admissions"]["statistics"]["act_english"] = ''

	# act math
	act_math = act[2].find("div", {"class":"scalar__value"})
	if (act_math != None):
		data[college_name]["admissions"]["statistics"]["act_math"] = act_math.span.text
	else:
		data[college_name]["admissions"]["statistics"]["act_math"] = ''

	# act writing
	act_writing = act[3].find("div", {"class":"scalar__value"})
	if (act_writing != None):
		data[college_name]["admissions"]["statistics"]["act_writing"] = act_writing.span.text
	else:
		data[college_name]["admissions"]["statistics"]["act_writing"] = ''

	# act submission percentage
	act_submission_percentage = act[4].find("div", {"class":"scalar__value"})
	if (act_submission_percentage != None):
		data[college_name]["admissions"]["statistics"]["act_submission_percentage"] = act_submission_percentage.span.text
	else:
		data[college_name]["admissions"]["statistics"]["act_submission_percentage"] = ''


	# 'deadlines'
	data[college_name]["admissions"]["deadlines"] = {}
	deadlines = page_soup.find("section", {"id":"admissions-deadlines"}).find("div", {"class":"profile__buckets"})

	# bucket 1
	deadlines_1 = deadlines.find("div", {"class":"profile__bucket--1"}).div.div.findAll(recursive=False)
	
	# application deadline
	application_deadline = deadlines_1[0].find("div", {"class":"scalar__value"})
	if (application_deadline != None):
		data[college_name]["admissions"]["deadlines"]["application_deadline"] = application_deadline.span.text
	else:
		data[college_name]["admissions"]["deadlines"]["application_deadline"] = ''
	
	# early decision deadline
	early_decision_deadline = deadlines_1[1].find("div", {"class":"scalar__value"})
	if (early_decision_deadline != None):
		data[college_name]["admissions"]["deadlines"]["early_decision_deadline"] = early_decision_deadline.span.text
	else:
		data[college_name]["admissions"]["deadlines"]["early_decision_deadline"] = ''

	# early action deadline
	early_action_deadline = deadlines_1[2].find("div", {"class":"scalar__value"})
	if (early_action_deadline != None):
		data[college_name]["admissions"]["deadlines"]["early_action_deadline"] = early_action_deadline.span.text
	else:
		data[college_name]["admissions"]["deadlines"]["early_action_deadline"] = ''

	# offers early decision
	offers_early_decision = deadlines_1[3].find("div", {"class":"scalar__value"})
	if (offers_early_decision != None):
		data[college_name]["admissions"]["deadlines"]["offers_early_decision"] = offers_early_decision.span.text
	else:
		data[college_name]["admissions"]["deadlines"]["offers_early_decision"] = ''

	# offers early action
	offers_early_action = deadlines_1[4].find("div", {"class":"scalar__value"})
	if (offers_early_action != None):
		data[college_name]["admissions"]["deadlines"]["offers_early_action"] = offers_early_action.span.text
	else:
		data[college_name]["admissions"]["deadlines"]["offers_early_action"] = ''


	# bucket 2
	deadlines_2 = deadlines.find("div", {"class":"profile__bucket--2"}).div.div.findAll(recursive=False)

	# application fee
	application_fee = deadlines_2[0].find("div", {"class":"scalar__value"})
	if (application_fee != None):
		data[college_name]["admissions"]["deadlines"]["application_fee"] = application_fee.span.text
	else:
		data[college_name]["admissions"]["deadlines"]["application_fee"] = ''

	# application website
	application_website = deadlines_2[1].find("div", {"class":"profile__website__url"})
	if (application_website != None):
		data[college_name]["admissions"]["deadlines"]["application_website"] = application_website.text
	else:
		data[college_name]["admissions"]["deadlines"]["application_website"] = ''

	# accepts common app
	accepts_common_app = deadlines_2[2].find("div", {"class":"scalar__value"})
	if (accepts_common_app != None):
		data[college_name]["admissions"]["deadlines"]["accepts_common_app"] = accepts_common_app.span.text
	else:
		data[college_name]["admissions"]["deadlines"]["accepts_common_app"] = ''

	# accepts coalition app
	accepts_coalition_app = deadlines_2[3].find("div", {"class":"scalar__value"})
	if (accepts_coalition_app != None):
		data[college_name]["admissions"]["deadlines"]["accepts_coalition_app"] = accepts_coalition_app.span.text
	else:
		data[college_name]["admissions"]["deadlines"]["accepts_coalition_app"] = ''



	# 'requirements'
	data[college_name]["admissions"]["requirements"] = {}
	requirements = page_soup.find("section", {"id":"admissions-requirements"}).find("div", {"class":"profile__buckets"}).findAll("div", {"class":"fact__table__row__value"})

	data[college_name]["admissions"]["requirements"]["gpa"] = requirements[0].text
	data[college_name]["admissions"]["requirements"]["rank"] = requirements[1].text
	data[college_name]["admissions"]["requirements"]["transcript"] = requirements[2].text
	data[college_name]["admissions"]["requirements"]["college_prep_coures"] = requirements[3].text
	data[college_name]["admissions"]["requirements"]["sat/act"] = requirements[4].text
	data[college_name]["admissions"]["requirements"]["recommendations"] = requirements[5].text


	writeToJSONFile(path, fileName, data)