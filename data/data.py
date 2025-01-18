import xml.etree.ElementTree as ET
import datetime

second_file = ET.parse("files/RS_ViaOW.xml")
second_file.write("files/RS_Via-3.xml")

root = ET.parse("files/RS_Via-3.xml").getroot()


def parse_flights():
    flights = []

    for flight in root.findall('.//Flight'):
        source = flight.find("Source").text
        destination = flight.find("Destination").text

        if source == "DXB" and destination == "BKK":
            carrier = flight.find('Carrier').text
            flight_number = flight.find('FlightNumber').text
            departure_time = flight.find('DepartureTimeStamp').text
            arrival_time = flight.find('ArrivalTimeStamp').text
            flight_class = flight.find('Class').text
            number_of_stops = flight.find('NumberOfStops').text
            ticket_type = flight.find('TicketType').text

            flights.append({
                "carrier": carrier,
                "flight_number": flight_number,
                "departure_time": departure_time,
                "arrival_time": arrival_time,
                "flight_class": flight_class,
                "number_of_stops": number_of_stops,
                "ticket_type": ticket_type
            })
    return flights

def parse_pricing():
    pricing = root.findall(".//Pricing")
    total_amounts = []

    for price in pricing:
        total_amount_elements = price.findall(".//ServiceCharges[@ChargeType='TotalAmount']")
        for total_amount in total_amount_elements:
            total_amounts.append(float(total_amount.text))

    return {
        "min_amount": min(total_amounts) if total_amounts else None,
        "max_amount": max(total_amounts) if total_amounts else None
    }

def parse_time():
    flights_info = []
    for flight in root.findall(".//Flight"):
        departure_time = flight.find('DepartureTimeStamp').text
        arrival_time = flight.find('ArrivalTimeStamp').text

        departure_dt = datetime.datetime.fromisoformat(departure_time)
        arrival_dt = datetime.datetime.fromisoformat(arrival_time)

        duration = (arrival_dt - departure_dt).total_seconds() / 60
        flights_info.append((flight, duration))

    return flights_info


def parse_stats():
    flights_info = parse_time()
    pricing = parse_pricing()

    if not flights_info:
        return ({"error": "No flights found"})
    
    fastest_flight = min(flights_info, key=lambda x: x[1])[0]
    slowest_flight = max(flights_info, key=lambda x: x[1])[0]
    average_duration = sum(duration for _, duration in flights_info) / len(flights_info)
    optimal_flight = min(flights_info, key=lambda x: abs(x[1] - average_duration))[0]

    stats = {
        "fastest": {
            "carrier": fastest_flight.find('Carrier').text,
            "flight_number": fastest_flight.find('FlightNumber').text,
            "duration": min(duration for _, duration in flights_info)
        },
        "slowest": {
            "carrier": slowest_flight.find('Carrier').text,
            "flight_number": slowest_flight.find('FlightNumber').text,
            "duration": max(duration for _, duration in flights_info)
        },
        "optimal": {
            "carrier": optimal_flight.find('Carrier').text,
            "flight_number": optimal_flight.find('FlightNumber').text,
            "duration": abs(average_duration)
        },
        "pricing": pricing
    }

    return stats

def compare_xml_files(file1="/home/kirill/Documents/python/assisted/files/RS_Via-3.xml", 
                      file2="/home/kirill/Documents/python/assisted/files/RS_ViaOW.xml"):
    tree1 = ET.parse(file1)
    tree2 = ET.parse(file2)

    root1 = tree1.getroot()
    root2 = tree2.getroot()

    differences = []

    for flight1, flight2 in zip(root1.findall('Flight'), root2.findall('Flight')):
        for elem1, elem2 in zip(flight1, flight2):
            if elem1.tag == elem2.tag and elem1.text != elem2.text:
                differences.append((elem1.tag, elem1.text, elem2.text))

    return differences

diffs = compare_xml_files()
for tag, value1, value2 in diffs:
    print(f"Element: {tag} | File1: {value1} | File2: {value2}")