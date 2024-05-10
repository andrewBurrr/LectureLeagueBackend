import datetime
import json
import random
import re
import uuid
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from parsers import CourseParser
from datatypes import Course


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


course_fixtures = []


class FacultyScraper:
    def __init__(self, url):
        self.url = url
        self.tree = Node("University of Calgary", None, "Institution", [])

    def scrape(self):
        print("Scraping faculties...")
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        faculties_dom = soup.select('#ctl00_ctl00_pageContent .item-container')

        for faculty_dom in faculties_dom:
            faculty_title_dom = faculty_dom.select_one('.generic-title')
            faculty_title = faculty_title_dom.string.strip()
            if faculty_title.endswith(', School of'):
                corrected_faculty_title = 'School of ' + faculty_title[:-len(', School of')]
            else:
                corrected_faculty_title = faculty_title

            self.tree.children.append(Node(corrected_faculty_title, None, "Faculty", []))

            class_doms = faculty_dom.select_one('.generic-body p')

            for class_dom in class_doms.find_all('a', class_='link-text'):
                class_title = class_dom.previous_sibling
                class_code = class_dom.string
                class_url = class_dom['href']
                course_scraper = CourseScraper(urljoin(self.url, class_url))
                course_scraper.scrape()
                # If the class is a top-level class, add it to the faculty
                if course_scraper.parent is None:
                    for faculty in self.tree.children:
                        if faculty.title == corrected_faculty_title:
                            faculty.children.append(Node(class_title, class_code, "Class", course_scraper.data))
                            break
                else:
                    parent_node = self.tree.search(course_scraper.parent)

                    if parent_node:  # Add node to its parent it exists
                        parent_node.children.append(Node(class_title, class_code, "Class", course_scraper.data))
                    else:
                        for faculty in self.tree.children:
                            if faculty.title == corrected_faculty_title:
                                faculty.children.append(Node(course_scraper.parent, None, "Department", []))
                                for department in faculty.children:
                                    if department.title == course_scraper.parent:
                                        department.children.append(Node(class_title, class_code, "Class", course_scraper.data))
                                        break
                                break


class CourseScraper:
    def __init__(self, url):
        self.url = url
        self.parent = None
        self.data = []

    def scrape(self):
        global course_fixtures
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        parent_dom = soup.select_one('span#ctl00_ctl00_pageContent_ctl01_ctl02_cnBody')

        if parent_dom:
            for a_tag in parent_dom.find_all('a'):
                a_tag.replace_with('')

            parent_text = parent_dom.get_text(strip=True).split('\n')[0].replace('\xa0', ' ').strip()
            parent_regexes = [
                r".*?(?: see|See|contact|consult) (?:the)?(.*?)(?:’s)?(?: website|[:.])",
            ]

            parent_title = None
            for parent_regex in parent_regexes:
                match = re.match(parent_regex, parent_text)
                if match:
                    parent_title = match.group(1).replace('website', '').replace('.', '').replace(':', '').strip()
                    break
            if parent_title:
                self.parent = parent_title

            code = soup.select_one('.page-title').string.strip().split(' ')[-1]

            courses_dom = soup.select('#ctl00_ctl00_pageContent .item-container table[bgcolor][cellpadding][align]')

            for course_dom in courses_dom:
                course_parser = CourseParser(course_dom)
                title, number, topic = course_parser.title_number_topic()
                description, subtopics = course_parser.description_subtopics()
                self.data.append(Course(title, code, number, topic, description, subtopics, parent_title))

                course_fixtures.append({
                    "model": "institutions.Course",
                    "pk": str(uuid.uuid4()),
                    "fields": {
                        "institution": "",
                        "name": title,
                        "code": code,
                        "number": number,
                        "description": description,
                        "date_created": datetime.datetime.now().isoformat(),
                        "date_updated": datetime.datetime.now().isoformat()
                    }
                })


class Node:
    def __init__(self, title, code, category, children):
        self.title = title
        self.code = code
        self.type = category
        self.children = children

    def __str__(self):
        if self.code:
            return f"{self.title} ({self.code}) ({self.type})"
        else:
            return f"{self.title} ({self.type})"

    def search(self, title):
        if self.title == title:
            return self
        for child in self.children:
            if type(child) == Node:
                result = child.search(title)
                if result:
                    return result
        return None


def print_tree(prefix, node, is_tail):
    name = str(node)
    connection = "└── " if is_tail else "├── "
    print(prefix + connection + name)
    if type(node) == Node:
        children = node.children
        for i, child in enumerate(children):
            is_last = i == len(children) - 1
            print_tree(prefix + ("    " if is_tail else "│   "), child, is_last)


def get_fake_institutions(num):
    names = ['University of']
    cities = ['Calgary', 'Edmonton', 'Vancouver', 'Toronto', 'Montreal', 'Ottawa', 'Victoria', 'Winnipeg']
    states = ['Alberta', 'British Columbia', 'Ontario', 'Quebec', 'Manitoba', 'Saskatchewan', 'Nova Scotia']
    countries = ['Canada']
    descriptions = ['A university', 'A college', 'An institution']

    fake_institutions = []

    for i in range(num):
        city = random.choice(cities)
        fake_institution = {
            "model": "institutions.Institution",
            "pk": str(uuid.uuid4()),
            "fields": {
                "name": random.choice(names) + ' ' + city,
                "city": city,
                "state": random.choice(states),
                "country": random.choice(countries),
                "description": random.choice(descriptions),
                "date_created": datetime.datetime.now().isoformat(),
                "date_updated": datetime.datetime.now().isoformat()
            }
        }
        fake_institutions.append(fake_institution)

    return fake_institutions


def get_fake_users(num):
    first_names = ['John', 'Jane', 'Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Hank']
    last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor']
    emails = ['@gmail.com', '@yahoo.com', '@hotmail.com', '@outlook.com', '@icloud.com', '@protonmail.com', '@aol.com']
    password = 'pbkdf2_sha256$720000$VnXhYPJb20agTiewkeVo2v$CqPLUYSsjq5bgCrqf0WchfOn0WZbePcb560Qm4Pc9ts='

    fake_users = []
    for i in range(num):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        user = {
            "model": "users.CustomUser",
            "pk": str(uuid.uuid4()),
            "fields": {
                "email": first_name.lower() + last_name.lower() + random.choice(emails),
                "first_name": first_name,
                "last_name": last_name,
                "password": password,
                "is_active": True,
                "is_staff": False,
                "date_joined": datetime.datetime.now().isoformat()
            }
        }
        fake_users.append(user)
    return fake_users


if __name__ == '__main__':

    current_directory = Path.cwd()
    target = current_directory / 'core'

    users = get_fake_users(10)
    write_json(users, target / 'users.json')

    institutions = get_fake_institutions(10)
    write_json(institutions, target / 'institutions.json')

    faculty_scraper = FacultyScraper('https://www.ucalgary.ca/pubs/calendar/staging/archives/2023/course-by-faculty.html')
    faculty_scraper.scrape()

    for institution in institutions:
        for idx, course in enumerate(course_fixtures):
            course_fixtures[idx]['fields']['institution'] = institution['pk']
    write_json(course_fixtures, target / 'courses.json')
