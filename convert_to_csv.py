import json
import csv


def export(courses, file='in_person'):
    with open(f'{file}.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['dept', 'num', 'name', 'gen_ed_req',
                    'section', 'sln', 'enrollment', 'credit', 'status',
                    'description'])
        for course in courses:
            segments = course['class'].split(' ')
            dept = ' '.join(segments[:-1])
            num = segments[-1]
            for section in course['sections']:
                writer.writerow([
                    dept, num, course['name'], course['gen_ed_req'],
                    section['section'], section['sln'], section['enrollment'],
                    section['credit'], section['status'], section['description']
                ])


def convert(file='in_person'):
    with open(f'{file}.json') as f:
        courses = json.load(f)
        export(courses, file)
        print(f'Converted {file}.json ')


if __name__ == '__main__':
    convert()
