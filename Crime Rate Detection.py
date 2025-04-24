crime_data = {}

def add_crime_data(area, crimes, police_count):
    if area not in crime_data:
        crime_data[area] = {"crimes": {}, "police_stations": 0}
    
    for crime_type, rate in crimes.items():
        crime_data[area]["crimes"][crime_type] = rate
    
    crime_data[area]["police_stations"] = police_count
    print(f"Data updated for {area}.")

def show_area_details(area):
    if area in crime_data:
        data = crime_data[area]
        print(f"\n Area: {area}")
        print(f" Police Stations: {data['police_stations']}")
        print("️ Crimes:")
        for crime, rate in data["crimes"].items():
            print(f"  - {crime}: {rate}")
    else:
        print(f"No data found for area: {area}")

def show_top_crime_area():
    if not crime_data:
        print("No crime data available.")
        return
    
    top_area = max(crime_data.items(), key=lambda x: sum(x[1]["crimes"].values()))
    name, data = top_area
    total_crime = sum(data["crimes"].values())
    
    print(f"\n Top crime area: {name}")
    print(f"Total Crime Rate: {total_crime}")
    print(f"Police Stations: {data['police_stations']}")
    for crime, rate in data["crimes"].items():
        print(f"  - {crime}: {rate}")

def top_areas_by_crime(crime_type):
    ranked = []
    for area, data in crime_data.items():
        if crime_type in data["crimes"]:
            ranked.append((area, data["crimes"][crime_type]))
    
    if not ranked:
        print(f"No areas found with crime: {crime_type}")
        return

    ranked.sort(key=lambda x: x[1], reverse=True)
    print(f"\n Top 5 areas with highest '{crime_type}' crime rate:")
    for i, (area, rate) in enumerate(ranked[:5], 1):
        print(f"{i}. {area} - {rate}")
if __name__ == "__main__":
    while True:
        print("\n---  Crime Rate Detection System ---")
        print("1. Add/Update Crime Data")
        print("2. Show All Crime Data for Area")
        print("3. Show Top Crime Area Overall")
        print("4. Show Top 5 Areas for a Specific Crime")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ").strip()
        
        if choice == "1":
            area = input("Enter area name: ").strip()
            try:
                police_count = int(input("Enter number of police stations: "))
            except ValueError:
                print(" Invalid number. Setting police station count to 0.")
                police_count = 0
            crimes = {}
            while True:
                crime_type = input("Enter crime type (or 'done' to finish): ").strip()
                if crime_type.lower() == 'done':
                    break
                try:
                    rate = int(input(f"Enter rate for '{crime_type}': "))
                    crimes[crime_type] = rate
                except ValueError:
                    print(" Please enter a valid number for the rate.")
            add_crime_data(area, crimes, police_count)

        elif choice == "2":
            area = input("Enter area name to view details: ").strip()
            show_area_details(area)

        elif choice == "3":
            show_top_crime_area()

        elif choice == "4":
            crime_type = input("Enter crime type to search top areas: ").strip()
            top_areas_by_crime(crime_type)

        elif choice == "5":
            print(" Exiting... Stay safe!")
            break

        else:
            print("Invalid choice. Please select 1 to 5.")
