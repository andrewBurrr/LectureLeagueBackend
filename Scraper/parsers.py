import re


class Parser:
    dom = ""

    def __init__(self, dom):
        self.dom = dom


class FacultyParser(Parser):
    def title(self):
        title_dom = self.dom.select_one('.unitis-business-unit .uofc-row-expander')
        if title_dom:
            title = title_dom.get_text(strip=True)
        else:
            title = None

        code_dom = self.dom.select_one(".unitis-business-unit .target")
        if code_dom:
            code = code_dom.attrs['name']
        else:
            code = None

        return title, code

    def phone_room_email_website(self):
        lists = {"phones": None, "rooms": None, "email": None, "website": None}
        for item in lists:
            text = []
            list_dom = self.dom.next_sibling.select(".unitis-%s-list li" % item)

            if list_dom:
                for each in list_dom:
                    if each.string:
                        text.append(each.string.strip())
                    else:
                        text.append(each.get_text(strip=True))

            if item == "website":
                text = list(filter(lambda x: not x.find("http"), text))  # Only leave link with http

            if text:
                lists[item] = text

        return lists['phones'], lists['rooms'], lists['email'], lists['website']

    def aka(self):
        aka = None
        contents_dom = self.dom.next_sibling.select(".details-row-cell .content")

        if contents_dom and len(contents_dom) >= 2:
            content_dom = contents_dom[1].select("p")

            for each in content_dom:
                text = each.get_text(strip=True)

                aka_reg_res = re.match(r"Also Known as:(.*)", text)
                if aka_reg_res:
                    aka = aka_reg_res.group(1).split(", ")

        return aka

    def parent(self):
        parent_type_dom = self.dom.select_one(".unitis-business-unit-parents .unitis-campuscontacts-unit-type")
        if parent_type_dom:
            parent_type = parent_type_dom.string
        else:
            parent_type = None

        parent_title_dom = self.dom.select_one(".unitis-business-unit-parents a")
        if parent_title_dom:
            parent_title = parent_title_dom.string
        else:
            parent_title = None

        return parent_title, parent_type

    def directory_of_people(self):
        directory_dom = self.dom.next_sibling.select_one(".unitis-directory-link a")
        if directory_dom:
            directory = directory_dom.attrs['href']
        else:
            directory = None
        return directory


class CourseParser(Parser):
    def title_number_topic(self):
        keys = self.dom.select(".course-code")
        title = keys[0].get_text(strip=True)
        number = keys[1].get_text(strip=True)
        topic = keys[2].get_text(strip=True)
        return title, number, topic

    def description_subtopics(self):
        description_dom = self.dom.select_one(".course-desc")

        description = []
        sub_topics = {}
        concat_text = " "

        for description_dom in description_dom.contents:
            sub_topics_reg = r"[0-9]{3}\.([0-9]{2})[\.]? ([A-Za-z \,\(\)\'\-][^0-9<]*)"
            sub_topics_reg_res_all = re.findall(
                sub_topics_reg, str(description_dom))

            if sub_topics_reg_res_all:  # Contain sub topics
                for sub_topics_reg_res in sub_topics_reg_res_all:
                    decimal = sub_topics_reg_res[0]
                    topic = sub_topics_reg_res[1].strip()
                    sub_topics[decimal] = topic
                concat_text = "<br>"
            elif description_dom.name == "a":  # Link
                description.append(str(description_dom).strip())
            elif description_dom.string:  # Pure string
                description.append(str(description_dom.string.strip()))
            else:
                description.append(description_dom.decode_contents().strip())
        pass

        description = concat_text.join(description)

        if not description:
            description = None

        if not sub_topics:
            sub_topics = None

        return description, sub_topics

