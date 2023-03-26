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
                new_data[key] = data.get(key)
            if key == "address":
                new_data["region"] = value.get("region")
                new_data["streetaddress"] = value.get("street-address")
                new_data["postalcode"] = value.get("postal-code")
                new_data["locality"] = value.get("locality")
            elif key == "ratings":
                new_data["service"] = value.get("service")
                new_data["cleanliness"] = value.get("cleanliness")
                new_data["value"] = value.get("value")
            # else:
            #     new_data[key] = value
        relevant_data.append(new_data)

    with open("relevant_fields.json", "w") as file:
        json.dump(relevant_data, file)
    file.close()

if __name__ == "__main__":
    main()