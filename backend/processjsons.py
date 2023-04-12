import json

def main():
    txt_to_json('hotels.txt', 'hotels.json')
    txt_to_json('reviews.txt', 'reviews.json')
    merge_jsons()
    keep_relevant_fields()

def txt_to_json(file, output):
    open(output, 'w').close()
    data = []
    with open(file, 'r') as f:
        for line in f:
            json_data = json.loads(line.strip())
            data.append(json_data)
    with open(output, 'w') as f:
        json.dump(data, f)
    f.close()

#merges the two jsons according to their offering_id and id  
def merge_jsons():
    open('merged_data.json', 'w').close()
    with open('hotels.json') as f:
        hotels_data = json.load(f)
    with open('reviews.json') as f:
        reviews_data = json.load(f)
    merged_data = []
    for hotel in hotels_data:
        for review in reviews_data:
            if hotel['id'] == review['offering_id']:
                merged_data.append({**hotel, **review})
    with open('merged_data.json', 'w') as f:
        json.dump(merged_data, f)
    f.close()

# narrow json down to only fields we are going to use
def keep_relevant_fields():
    open('relevant_fields.json', 'w').close()

    with open("merged_data.json") as file:
        original_data = json.load(file)

    relevant_fields = [
        "name",
        "hotel_class",
        "region",
        "street-address",
        "postal-code",
        "locality",
        "id",
        "service",
        "cleanliness",
        "value",
        "text"
    ]

    relevant_data = []
    for data in original_data:
        new_data = {}
        for key, value in data.items():
            if key in relevant_fields:
                if value != "" and value is not None: # check if the value is not empty or null
                    new_data[key] = data.get(key)
            if key == "address":
                if value.get("region") != "" and value.get("region") is not None:
                    new_data["region"] = value.get("region")
                if value.get("street-address") != "" and value.get("street-address") is not None:
                    new_data["streetaddress"] = value.get("street-address")
                if value.get("postal-code") != "" and value.get("postal-code") is not None:
                    new_data["postalcode"] = value.get("postal-code")
                if value.get("locality") != "" and value.get("locality") is not None:
                    new_data["locality"] = value.get("locality")
            elif key == "ratings":
                if value.get("service") is not None:
                    new_data["service"] = value.get("service")
                if value.get("cleanliness") is not None:
                    new_data["cleanliness"] = value.get("cleanliness")
                if value.get("value") is not None:
                    new_data["value"] = value.get("value")
            # else:
            #     new_data[key] = value
        # for key in relevant_fields:
        #     if key not in new_data:
        #         if key == "name":
        #             new_data['name'] = "PLACEHOLDER"
        #         elif key == "hotel_class":
        #             new_data['hotel_class'] = -1.0
        if len(new_data) > 0: # check if the new_data dictionary has any fields before appending
            relevant_data.append(new_data)

    with open("relevant_fields.json", "w") as file:
        json.dump(relevant_data, file)
    file.close()

if __name__ == "__main__":
    main()