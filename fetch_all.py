import re
import json
import requests
from bs4 import BeautifulSoup  # import html5lib


def main():
    campus = ''  # Seattle
    # campus = '/B'  # Bothell
    # campus = '/T'  # Tacoma

    result = list()
    parse_campus('', result)
    with open('in_person.json', 'w') as fp:
        json.dump(result, fp)
        print(f'Exported {len(result)} Courses/Sections')


def parse_campus(campus, result):
    url = f'https://www.washington.edu/students/timeschd{campus}/AUT2020/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html5lib')  # Handle broken HTML
    departments = set()
    for a in soup.find('div', 'uw-body').find_all('a'):
        try:
            if a['href'].endswith('.html') and '/' not in a['href']:
                departments.add(a['href'])
        except:
            pass
    for department in departments:
        print(f'Processing {department}')
        parse(campus, department, result)


def parse(campus, department, result):
    r = requests.get(
        f'https://www.washington.edu/students/timeschd{campus}/AUT2020/{department}')
    soup = BeautifulSoup(r.text, 'html.parser')
    current_class = ''
    current_name = ''
    sections = []
    for table in soup.find_all('table'):
        pre = table.find('pre')
        if pre:
            sln = pre.find('a').text
            description = pre.text.strip()
            if 'OFFERED VIA REMOTE LEARNING' not in description:
                sections.append({
                    'sln': sln,
                    'description': re.sub(r'\s+', ' ', description)
                })
        else:
            if current_class and sections:
                result.append({
                    'class': current_class,
                    'name': current_name,
                    'sections': sections
                })
            sections = []
            links = table.find_all('a')
            if len(links) == 2:
                current_class = re.sub(r'\s+', ' ', links[0].text).strip()
                current_name = links[1].text
                print(f'    Parsing {current_class} {current_name}')


if __name__ == '__main__':
    main()
