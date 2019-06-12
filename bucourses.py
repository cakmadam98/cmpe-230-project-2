
#Imports

import pandas as pd
import requests
import itertools
from itertools import groupby
import re
import sys


# SAMPLES
# sample_input1 = "2017-Fall"
# sample_input2 = "2018-Spring"
# sample_input3 = "2018-Summer"
# sample_input4 = "2018-Fall"
# sample_input5 = "2019-Spring"
# sample_input6 = "2019-Summer"

#detect the formal semester info. Useful for link.
# Example: 2018-Fall ---> 2018/2019-1
def getSemester(in1):
    year = in1.split("-")[0]
    term = in1.split("-")[1]
    if term == "Fall":
        return str(year) + "/" + str(int(year)+1) + "-1"
    elif term == "Spring":
        return str(int(year)-1) + "/" + str(year) + "-2"
    elif term == "Summer":
        return str(int(year)-1) + "/" + str(year) + "-3"

#to store all semesters that may be requested.
#Years after 2018 is not included!
def all_semesters():
    semesters = []
    start1 = 1998
    start2 = 1999
    terms = [1,2,3]
    for x in terms:
        semesters.append(str(start1) + "/" + str(start2) + "-" + str(x))
    while start2 != 2019:
        start1 += 1
        start2 += 1
        for x in terms:
            semesters.append(str(start1) + "/" + str(start2) + "-" + str(x))
    return semesters

#Get the requested semesters and store in a list.
#in1 and in2 are the informal inputs, we will change it to formal ones.
def get_requested_semesters(in1, in2):
    requested = []
    start = getSemester(in1)
    end = getSemester(in2)
    semesters = all_semesters()
    start_index = semesters.index(start)
    end_index = semesters.index(end)
    for x in range(start_index, end_index+1):
        requested.append(semesters[x])
    return requested

# Grabs all the necessary links for given semester range
def getAllLinks():
    All_links = []
    links = ['https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=ASIA&bolum=ASIAN+STUDIES', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=ASIA&bolum=ASIAN+STUDIES+WITH+THESIS', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=ATA&bolum=ATATURK+INSTITUTE+FOR+MODERN+TURKISH+HISTORY', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=AUTO&bolum=AUTOMOTIVE+ENGINEERING', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=BM&bolum=BIOMEDICAL+ENGINEERING', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=BIS&bolum=BUSINESS+INFORMATION+SYSTEMS', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=CHE&bolum=CHEMICAL+ENGINEERING', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=CHEM&bolum=CHEMISTRY', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=CE&bolum=CIVIL+ENGINEERING', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=COGS&bolum=COGNITIVE+SCIENCE', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=CSE&bolum=COMPUTATIONAL+SCIENCE+%26+ENGINEERING', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=CET&bolum=COMPUTER+EDUCATION+%26+EDUCATIONAL+TECHNOLOGY', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=CMPE&bolum=COMPUTER+ENGINEERING', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=INT&bolum=CONFERENCE+INTERPRETING', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=CEM&bolum=CONSTRUCTION+ENGINEERING+AND+MANAGEMENT', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=CCS&bolum=CRITICAL+AND+CULTURAL+STUDIES', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=EQE&bolum=EARTHQUAKE+ENGINEERING', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=EC&bolum=ECONOMICS', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=EF&bolum=ECONOMICS+AND+FINANCE', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=ED&bolum=EDUCATIONAL+SCIENCES', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=CET&bolum=EDUCATIONAL+TECHNOLOGY', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=EE&bolum=ELECTRICAL+%26+ELECTRONICS+ENGINEERING', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=ETM&bolum=ENGINEERING+AND+TECHNOLOGY+MANAGEMENT', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=ENV&bolum=ENVIRONMENTAL+SCIENCES', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=ENVT&bolum=ENVIRONMENTAL+TECHNOLOGY', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=XMBA&bolum=EXECUTIVE+MBA', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=FE&bolum=FINANCIAL+ENGINEERING', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=PA&bolum=FINE+ARTS', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=FLED&bolum=FOREIGN+LANGUAGE+EDUCATION', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=GED&bolum=GEODESY', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=GPH&bolum=GEOPHYSICS', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=GUID&bolum=GUIDANCE+%26+PSYCHOLOGICAL+COUNSELING', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=HIST&bolum=HISTORY', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=HUM&bolum=HUMANITIES+COURSES+COORDINATOR', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=IE&bolum=INDUSTRIAL+ENGINEERING', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=INCT&bolum=INTERNATIONAL+COMPETITION+AND+TRADE', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=MIR&bolum=INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=MIR&bolum=INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST+WITH+THESIS', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=INTT&bolum=INTERNATIONAL+TRADE', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=INTT&bolum=INTERNATIONAL+TRADE+MANAGEMENT', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=LS&bolum=LEARNING+SCIENCES', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=LING&bolum=LINGUISTICS', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=AD&bolum=MANAGEMENT', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=MIS&bolum=MANAGEMENT+INFORMATION+SYSTEMS', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=MATH&bolum=MATHEMATICS', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=SCED&bolum=MATHEMATICS+AND+SCIENCE+EDUCATION', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=ME&bolum=MECHANICAL+ENGINEERING', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=MECA&bolum=MECHATRONICS+ENGINEERING', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=BIO&bolum=MOLECULAR+BIOLOGY+%26+GENETICS', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=PHIL&bolum=PHILOSOPHY', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=PE&bolum=PHYSICAL+EDUCATION', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=PHYS&bolum=PHYSICS', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=POLS&bolum=POLITICAL+SCIENCE%26INTERNATIONAL+RELATIONS', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=PRED&bolum=PRIMARY+EDUCATION', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=PSY&bolum=PSYCHOLOGY', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=YADYOK&bolum=SCHOOL+OF+FOREIGN+LANGUAGES', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=SCED&bolum=SECONDARY+SCHOOL+SCIENCE+AND+MATHEMATICS+EDUCATION', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=SPL&bolum=SOCIAL+POLICY+WITH+THESIS', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=SOC&bolum=SOCIOLOGY', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=SWE&bolum=SOFTWARE+ENGINEERING', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=SWE&bolum=SOFTWARE+ENGINEERING+WITH+THESIS', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=TRM&bolum=SUSTAINABLE+TOURISM+MANAGEMENT', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=SCO&bolum=SYSTEMS+%26+CONTROL+ENGINEERING', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=TRM&bolum=TOURISM+ADMINISTRATION', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=WTR&bolum=TRANSLATION', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=TR&bolum=TRANSLATION+AND+INTERPRETING+STUDIES', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=TK&bolum=TURKISH+COURSES+COORDINATOR', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=TKL&bolum=TURKISH+LANGUAGE+%26+LITERATURE', 'https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=LL&bolum=WESTERN+LANGUAGES+%26+LITERATURES']
#    links = ["https://registration.boun.edu.tr/scripts/sch.asp?donem=2018/2019-2&kisaadi=CHEM&bolum=CHEMISTRY"] // This is a test link
    leftLink = []
    rightLink = []


 #   with open('/Users/berk/WinvestiJupyter/Untitled Folder 1/testURLS.txt', 'r') as file:
 #       links.append(file.readlines())




    for link in links:
 #       link = link.replace('\n', '')
        temp = link.split("2018/2019-2")

        leftLink.append(temp[0])
        rightLink.append(temp[1])


    for left, right in zip(leftLink, rightLink):
        for semester in semesters:
            All_links.append(left + semester + right)

    return All_links

# Get course codes for a departmant

def get_courses_from_df(df):
    courses = df["Code.Sec"].tolist()
    return courses

def get_total_course_codes(dataframes):
    course_codes = []
    course_codes_full = []

    for df in dataframes:
        courses = get_courses_from_df(df)
        for course in courses:
            course_codes.append(course)

    for course_code in course_codes:
        #to skip empty boxes.
        if pd.isnull(course_code):
            continue
        #to get rid of section number use split.
        temp = course_code.split(".")
        course_codes_full.append(temp[0])

    #removes dublicates.
    course_codes = remove_dublicates(course_codes_full)


    return course_codes


#### Coursename
def get_coursenames_from_df(df):
    coursenames = df["Name"].tolist()
    return coursenames

def get_coursename(dataframes):
    course_names = []
    course_names_full = []

    for df in dataframes:
        coursenames = get_coursenames_from_df(df)
        for coursename in coursenames:
            course_names_full.append(coursename)

    #removes dublicates.
    course_names = remove_dublicates(course_names_full)

    return course_names

def remove_dublicates(x):
  return list(dict.fromkeys(x))

def get_course_code_summary(courses):
    course_codes = []
    course_codes_full = []
    undergrad = []
    grad = []

    for course in courses:
        #to skip empty boxes.
        if pd.isnull(course):
            continue
        #to get rid of section number use split.
        temp = course.split(".")
        course_codes_full.append(temp[0])

    #removes dublicates.
    course_codes = remove_dublicates(course_codes_full)

    #determine if course is grad or undergrad level.
    for code in course_codes:
        #to skip empty boxes.
        if pd.isnull(code):
            continue
        #kodda geçen ilk integer'ı bulur, match object return eder.
        m = re.search("\d", code)
        if int(code[m.start()]) < 5:
            undergrad.append(code)
        else:
            grad.append(code)

    return "U" + str(len(undergrad)) + " " + "G" + str(len(grad))
#### Distinct Instructor

def get_distinct_instructors_num(df):
    instructors = df["Instr."].tolist()
    instructors = remove_dublicates(instructors)
 #   print(instructors)
    return len(instructors)
#### Term Summary

def get_term_summary(df):
    courses = df["Code.Sec"].tolist()
    string1 = get_course_code_summary(courses)
    string2 = get_distinct_instructors_num(df)
    return string1 + " I" + str(string2)

#### Given classes in a semester
# course_codes are the all offered classes in all semesters
# courses is for example classes of 2018-Spring
def get_term_available_courses(df, course_codes_all):
    term_summary = get_term_summary(df)
    course_codes_this_term = []
    wanted_list = []
    if 'checker' in df.columns:

        while(len(wanted_list) != length):
            wanted_list.append("")
        wanted_list[0] = "U0 G0 I0"
        return wanted_list
    courses = get_courses_from_df(df)
    for course in courses:
        #to skip empty boxes.
        if pd.isnull(course):
            continue
        #to get rid of section number use split.
        temp = course.split(".")
        course_codes_this_term.append(temp[0])

    course_codes_this_term = remove_dublicates(course_codes_this_term)


    for course_code in course_codes_all:
        if course_code in course_codes_this_term:
            wanted_list.append("X")
        else:
            wanted_list.append("")
    wanted_list[0] = term_summary
    return wanted_list


# Group links with the same departmant
def getGroupedLinks(All_links):
    def departmantSeperate(val):
        return val.split("bolum=")[1]

    x_sorted = sorted(All_links, key=departmantSeperate)
    x_grouped = [list(it) for k, it in groupby(x_sorted, departmantSeperate)]
    return x_grouped

#Helper method. Deletes section info and duplicates.
def clear_course_codes(courses):
    new = []
    for course in courses:
        #to skip empty boxes.
        if pd.isnull(course):
            continue
        #to get rid of section number use split.
        temp = course.split(".")
        new.append(temp[0])

    courses_new = remove_dublicates(new)
    return courses_new


# get total offerings of courses in one department. eventually you can search for multiple of departments.
# courses_on_different_semesters = [[cmpe2018/2019-1], [cmpe2018/2019-2], .........]
def get_total_offerings_courses(courses_on_different_semesters,course_codes_all):

    #TEMİZLEME
    courses_on_different_semesters_cleared = []

    #clearing course section part.
    for courses in courses_on_different_semesters:
        courses = clear_course_codes(courses)
        courses_on_different_semesters_cleared.append(courses)

    #İŞLEM
    #Bizden istenilen listeyi 0'lardan oluşacak şekilde initialize ediyorum.
    requested_list = [0]*len(course_codes_all)

    index = 0
    for course in course_codes_all:
        for x in courses_on_different_semesters_cleared:
            if course in x:
                requested_list[index] += 1
        index += 1

    return requested_list


#### Total Offerings Summary
# FOR EXAMPLE : instructors_list = [[teacherA,teacherB], [teacherA,teacherB,teacherC], [teacherA]]
# For I : Collect all instructers in all semester for each classes offered and return it after removing duplicates.
# Same for U and G.


def get_total_offerings_summary(courses_list, instructors_list):

    #Cleaning

    courses_list_cleared = []
    instructors_list_cleared = []

    #clearing course section part.
    for courses in courses_list:
        courses = clear_course_codes(courses)
        for course in courses:
            courses_list_cleared.append(course)

    courses_list_cleared = remove_dublicates(courses_list_cleared)

    #number of grad and undergrad
    grad = []
    undergrad = []

    #determine if course is grad or undergrad level.
    for course in courses_list_cleared:
        #to skip empty boxes.
        if pd.isnull(course):
            continue
        #kodda geçen ilk integer'ı bulur, match object return eder.
        m = re.search("\d", course)
        if int(course[m.start()]) < 5:
            undergrad.append(course)
        else:
            grad.append(course)

    num_undergrad = str(len(undergrad))
    num_grad = str(len(grad))

    # Number of Distinct Instructors Part
    for instructors in instructors_list:
        instructors = remove_dublicates(instructors)
        for instructor in instructors:
            instructors_list_cleared.append(instructor)

    num_instructors = str(len(remove_dublicates(instructors_list_cleared)))

    # return the answer.
    s = "U" + num_undergrad + " G" + num_grad + " I" + num_instructors
    return s



#### Distinct Instructor For Spesific Course
def get_distinct_instructor_list(courses_list,instructors_list):
    #Cleaning
    courses_list_cleared = []
    courses_new = []

    #clearing course section part.
    for courses in courses_list:
        for course in courses:
            #to skip empty boxes.
            if pd.isnull(course):
                continue
            #to get rid of section number use split.
            temp = course.split(".")
            course = temp[0]

    #Find total(distinct) list from courses_list.
    total = []
    for courses in courses_list:
        for course in courses:
            total.append(course)
    total = remove_dublicates(total)

    # Define the list from set and courses part.
    big_list = []
    for x in total:
        big_list.append([x, set()])

    # Append to big_list by traversing every semester
    for courses,instructors in zip(courses_list, instructors_list):
        for course,instructor in zip(courses,instructors):
            for e in big_list:
                if course == e[0]:
                    e[1].add(instructor)

    # let's return our answer.
    l = []
    for e in big_list:
        l.append(len(e[1]))
    return l


#### Total Offerings For Spesific Course
def total_offerings_of_course(courses_list, instructors_list):

    #clearing course section part.
    courses_new = []
    for courses in courses_list:
        for course in courses:
            #to skip empty boxes.
            if pd.isnull(course):
                continue
            #to get rid of section number use split.
            temp = course.split(".")
            courses_new.append(temp[0])

    total = remove_dublicates(courses_new)

    #print(total)


    right_list = get_distinct_instructor_list(courses_list,instructors_list)
    left_list = get_total_offerings_courses(courses_list,total)

    l = []

    for x,y in zip(left_list, right_list):
        l.append(str(x) + "/" + str(y))

    return l










# Get wanted semesters
semesters = get_requested_semesters(sys.argv[1],sys.argv[2])

All_links = getAllLinks()


# Predefine needed lists
groupedLinks = getGroupedLinks(All_links)
DeptList = []
CourseCodeList = []
CourseNameList = []
TotalOfferingsList = []
SemestersList = []
for i in range(0, len(semesters)):
    SemestersList.append([])

# Travers each departmant and create their table. In the end all departmants tables will be joined within the above define lists
for departmantlinks in groupedLinks:
    dataframes = []
    isItFirst = True
    semesterCount = 0

    ThisDeptList = []
    ThisCourseCodeList = []
    ThisCourseNameList = []
    ThisTotalOfferingsList = []
    ThisSemestersList = []
    for i in range(0, len(semesters)):
        ThisSemestersList.append([])

    # Travers each semester for a departmant
    for pagelink in departmantlinks:
        # Try to get the html
        try:
            r = requests.get(pagelink)
            html = r.content
            dfAll = pd.read_html(html)
            df = dfAll[3]
            headers = df.iloc[0]
            processed_df  = pd.DataFrame(df.values[1:], columns=headers)
            dataframes.append(processed_df)


            if(isItFirst):
                df = dfAll[0]
                depName = df.at[1,1]
                ThisDeptList.append(depName)

            isItFirst = False

        # If can't get the html (like summer semester not existing for a departmant, copy first getted dataframe and mark it as copied (checked)).
        except:

            temp2_df = dataframes[0].copy(deep=True)
            temp2_df["checker"] = "checker"
            dataframes.append(temp2_df)

            continue

    ThisCourseCodeList = get_total_course_codes(dataframes)
    ThisCourseNameList = get_coursename(dataframes)

    unsorted = ThisCourseCodeList
    ThisCourseCodeList, ThisCourseNameList =(list(t) for t in zip(*sorted(zip(ThisCourseCodeList, ThisCourseNameList))))

    CourseCodeSummary = get_course_code_summary(ThisCourseCodeList)
    ThisCourseCodeList.insert(0, CourseCodeSummary)
    ThisCourseNameList.insert(0, " ")
    length = len(ThisCourseCodeList)


    while(len(ThisCourseNameList) < length):
        ThisCourseNameList.append("")
    while(len(ThisDeptList) < length):
        ThisDeptList.append("")
    while(len(ThisTotalOfferingsList) < length):
        ThisTotalOfferingsList.append("")


    # Checking whether a course is included in semester or not
    for df in dataframes:
        ThisSemestersList[semesterCount].extend(get_term_available_courses(df, ThisCourseCodeList))
        semesterCount = semesterCount + 1


    all_semesters_courses = []
    all_semesters_instructors = []
    for df in dataframes:
        all_semesters_courses.append(get_courses_from_df(df))
        all_semesters_instructors.append(df["Instr."].tolist())


    total_offerings_summary = get_total_offerings_summary(all_semesters_courses, all_semesters_instructors)
    ThisTotalOfferingsList = total_offerings_of_course(all_semesters_courses, all_semesters_instructors)
    unsorted, ThisTotalOfferingsList =(list(t) for t in zip(*sorted(zip(unsorted, ThisTotalOfferingsList))))

    ThisTotalOfferingsList.insert(0, total_offerings_summary)

    DeptList.extend(ThisDeptList)
    CourseCodeList.extend(ThisCourseCodeList)
    CourseNameList.extend(ThisCourseNameList)
    TotalOfferingsList.extend(ThisTotalOfferingsList)

    for i in range(0, len(semesters)):
        SemestersList[i].extend(ThisSemestersList[i])

# Create Data for dataframe
Data = {'Dept./Prog. (name)':  DeptList,
        'Course Code': CourseCodeList,
        'Course Name': CourseNameList,
        'Total Offerings': TotalOfferingsList,
        }
columns = ['Dept./Prog. (name)','Course Code','Course Name']


# Add semesters to dataframe
for semesterLabel, crosses in zip(semesters, SemestersList):
    Data[semesterLabel] = crosses
    columns.append(semesterLabel)
# Finally add Total Offerings to dataframe
columns.append('Total Offerings')
Schedule = pd.DataFrame(Data, columns=columns)
Schedule.set_index('Dept./Prog. (name)', inplace=True)
# Print it to csv
print(Schedule.to_csv())
