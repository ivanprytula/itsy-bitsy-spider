import re

FLOAT_POINT_NUMBER_REGEX = r"[-+]?([0-9]*\.[0-9]+|[0-9]+)"

test_string = "3.9 star rating"

match = re.match(FLOAT_POINT_NUMBER_REGEX, test_string)
print(match)
