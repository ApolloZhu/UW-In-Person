import json
import csv


def export(courses, file='in_person'):
    with open(f'{file}.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for course in courses:
            segments = course['class'].split(' ')
            dept = ' '.join(segments[:-1])
            num = segments[-1]
            for section in course['sections']:
                writer.writerow([
                    dept, num, course['name'], course['gen_ed_req'],
                    section['sln'], section['description']
                ])


def convert(file='in_person'):
    with open(f'{file}.json') as f:
        courses = json.load(f)
        export(courses, file)
        print(f'Converted {file}.json ')


if __name__ == '__main__':
    convert()
