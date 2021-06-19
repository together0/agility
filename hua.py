from apps.auxiliary.model import First_second_mapping

dict = {1:["1","11"], 2:["2","22"]}

if 3 in dict:
    print("yes")
else:
    print("no")

print(dict.keys())



mappings = First_second_mapping.query.filter(First_second_mapping.second_trace_code == trace_code)\
                .with_entities(First_second_mapping.vaccine_id).all()

