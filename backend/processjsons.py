import json

def main():
    hotels_to_json()
    reviews_to_json()
    merge_jsons()
    keep_relevant_fields()

def hotels_to_json():
    open('hotels.json', 'w').close()

    data = []
    with open('hotels.txt', 'r') as f:
        for line in f:
            json_data = json.loads(line.strip())
            data.append(json_data)

    with open('hotels.json', 'w') as f:
        json.dump(data, f)

def reviews_to_json():
    open('reviews.json', 'w').close()

    data = []
    with open('reviews.txt', 'r') as f:
        for line in f:
            json_data = json.loads(line.strip())
            data.append(json_data)

    with open('reviews.json', 'w') as f:
        json.dump(data, f)

def merge_jsons():
    open('merged_data.json', 'w').close()

    # Load hotels data
    with open('hotels.json') as f:
        hotels_data = json.load(f)

    # Load reviews data
    with open('reviews.json') as f:
        reviews_data = json.load(f)

    # Merge data based on unique identifier
    merged_data = []
    for hotel in hotels_data:
        for review in reviews_data:
            if hotel['id'] == review['offering_id']:
                merged_data.append({**hotel, **review})

    # Write merged data to new JSON file
    with open('merged_data.json', 'w') as f:
        json.dump(merged_data, f)

def keep_relevant_fields():
    open('relevant_fields.json', 'w').close()

    # Read the original data from the file
    with open("merged_data.json") as file:
        original_data = json.load(file)

    # The list of relevant fields
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

    # Extract the relevant fields from the original data
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
    
    # Write the relevant data to a new file
    with open("relevant_fields.json", "w") as file:
        json.dump(relevant_data, file)

if __name__ == "__main__":
    main()