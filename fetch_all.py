import re
import json
import requests
from bs4 import BeautifulSoup  # import html5lib


def main():
    campus = ''  # Seattle
    # campus = '/B'  # Bothell
    # campus = '/T'  # Tacoma
    result = parse_campus(campus)
    with open('in_person.json', 'w') as fp:
        json.dump(result, fp)
        print(f'Exported {len(result)} Courses/Sections')


def parse_campus(campus='', verbose=False):
    result = list()
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
        if verbose:
            print(f'Processing {department}')
        parse(campus, department, result)
    return result


def parse(campus, department, result):
    r = requests.get(
        f'https://www.washington.edu/students/timeschd{campus}/AUT2020/{department}')
    soup = BeautifulSoup(r.text, 'html.parser')
    current_class = ''
    current_name = ''
    current_gen_ed_req = ''
    sections = []
    for table in soup.find_all('table'):
        pre = table.find('pre')
        if pre:
            sln = pre.find('a').text
            description = pre.text.strip()
            if 'OFFERED VIA REMOTE LEARNING' not in description:
                if re.search('\d+', sln):
                    description = re.sub(sln, '', description, 1)
                status = re.search('Open|Closed|Restr|>', description).group()
                description = re.sub(status, '', description, 1)
                status = 'Entry Code Required' if status == '>' else status
                status = 'Restrictions Apply' if status == 'Restr' else status
                enrollment = re.search(r'\d+/\s+\d+', description)
                enrollment = enrollment[0] if enrollment else ''
                enrollment = re.sub(r'/\s+', '/', enrollment)
                section = re.search(r'[A-Z]+', description)
                section = section[0] if section else ''
                description = re.sub(section, '', description, 1)
                credit = re.search(r'\d+\-\d+|\w+', description)
                credit = credit[0] if credit else ''
                description = re.sub(credit, '', description, 1)
                sections.append({
                    'sln': sln,
                    'section': section,
                    'description': re.sub(r'\s+', ' ', description),
                    'status': status,
                    'enrollment': enrollment,
                    'credit': credit
                })
        else:
            if current_class and sections:
                result.append({
                    'class': current_class,
                    'name': current_name,
                    'gen_ed_req': current_gen_ed_req,
                    'sections': sections
                })
            sections = []
            links = table.find_all('a')
            if len(links) == 2:
                current_class = re.sub(r'\s+', ' ', links[0].text).strip()
                current_name = links[1].text
                gen_eds = table.find_all('b')
                for b in gen_eds:
                    if re.match("\(", b.text):
                        if re.search("C|DIV|I&S|NW|QSR|VLPA|W", b.text):
                            current_gen_ed_req = b.text[1:-1]
                print(
                    f'    Parsing {current_class} {current_name} {current_gen_ed_req}')
    if current_class and sections:
        result.append({
            'class': current_class,
            'name': current_name,
            'gen_ed_req': current_gen_ed_req,
            'sections': sections
        })


if __name__ == '__main__':
    main()
