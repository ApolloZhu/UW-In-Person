import json
import csv


with open('in_person.json') as f:
    with open('in_person.csv', 'w') as csvfile:
        courses = json.load(f)
        writer = csv.writer(csvfile)
        for course in courses:
            segs = course["class"].split(" ")
            dept = ' '.join(segs[:-1])
            num = segs[-1]
            for section in course["sections"]:
                writer.writerow([
                    dept, num, course["name"],
                    section["sln"], section["description"]
                ])
