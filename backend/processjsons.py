import json

def main():
    hotels_to_json()
    reviews_to_json()
    merge_jsons()
    keep_relevant_fields()

#converts hotel txt file to json
def hotels_to_json():
    open('hotels.json', 'w').close()

    data = []
    with open('hotels.txt', 'r') as f:
        for line in f:
            json_data = json.loads(line.strip())
            data.append(json_data)

    with open('hotels.json', 'w') as f:
        json.dump(data, f)

#converts reviews txt file to json
def reviews_to_json():
    open('reviews.json', 'w').close()

    data = []
    with open('reviews.txt', 'r') as f:
        for line in f:
            json_data = json.loads(line.strip())
            data.append(json_data)

    with open('reviews.json', 'w') as f:
        json.dump(data, f)

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

# narrow json down to only fields we are going to use 
def keep_relevant_fields():
    open('relevant_fields.json', 'w').close()

    with open("merged_data.json") as file:
        original_data = json.load(file)

    relevant_fields = [
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
                if key == "address":
                    new_data["region"] = value.get("region")
                    new_data["street-address"] = value.get("street-address")
                    new_data["postal-code"] = value.get("postal-code")
                    new_data["locality"] = value.get("locality")
                elif key == "ratings":
                    new_data["service"] = value.get("service")
                    new_data["cleanliness"] = value.get("cleanliness")
                    new_data["value"] = value.get("value")
                else:
                    new_data[key] = value
        relevant_data.append(new_data)
    
    with open("relevant_fields.json", "w") as file:
        json.dump(relevant_data, file)

if __name__ == "__main__":
    main()