from fetch_all import parse_campus
from convert_to_csv import export

result = parse_campus()
export(result)
print("Done")
