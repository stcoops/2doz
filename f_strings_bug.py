# odd Bug i encountered calling the get_attribute_index function
# of main.py (line 58) Potentially my fault for overloading f with
# too many brackets lol but also could be an issue to be resolved.

def get_attribute_index(attribute):
    headers = ["a","b","c","d"]
    for index, header in enumerate(headers):
        if header == attribute:
            return index


row = ["1","2","3","4"]
print(row[get_attribute_index("b")])
#not sure if my fault or  not lol
print(f"{row[get_attribute_index("b")]}")