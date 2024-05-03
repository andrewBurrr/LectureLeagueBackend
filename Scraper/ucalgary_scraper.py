import os
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from parsers import CourseParser
from datatypes import Course


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
                # print("Raw Parent Text:", repr(parent_text))
                # print("URL:", self.url)
                # print("Data:", self.data)


class Node:
    def __init__(self, title, code, type, children):
        self.title = title
        self.code = code
        self.type = type
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


if __name__ == '__main__':

    faculty_scraper = FacultyScraper('https://www.ucalgary.ca/pubs/calendar/staging/archives/2023/course-by-faculty.html')
    faculty_scraper.scrape()
    print_tree("", faculty_scraper.tree, True)
