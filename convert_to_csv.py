import json
import csv


with open('in_person.json') as f:
    with open('in_person.csv', 'w') as csvfile:
        courses = json.load(f)
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
        print('Converted')
