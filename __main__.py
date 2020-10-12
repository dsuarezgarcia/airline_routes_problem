# -*- encoding: utf-8 -*-

'''
    Title: The airports routes problem.

    Description: an airline operates at different airports, list collected in AIRPORTS.
                 The available direct routes the airline offers can be seen at ROUTES.
                 A route [X, Y] means travellers can fly from X to Y, but NOT viceversa.
                 Having the routes [X, Y], [Y, Z], ..., [Z, N] enables travellers to fly
                 from X to N. The airline wants travellers to be able to fly from an origin
                 airport to any destination, regardless of the number of stopovers they'd
                 have to make.

    Goal: given an origin airport STARTING_AIRPORT, find the minimum new routes needed so
          travellers can fly from STARTING_AIRPORT to any destination airport.
'''

AIRPORTS = [
"BGI", "CDG", "DEL", "DOH", "DSM", "EWR", "EYW", "HND", "ICN",
"JFK", "LGA", "LHR", "ORD", "SAN", "SFO", "SIN", "TLV", "BUD"
]

ROUTES = [
["DSM", "ORD"],
["ORD", "BGI"],
["BGI", "LGA"],
["SIN", "CDG"],
["CDG", "SIN"],
["CDG", "BUD"],
["DEL", "DOH"],
["DEL", "CDG"],
["TLV", "DEL"],
["EWR", "HND"],
["HND", "ICN"],
["HND", "JFK"],
["ICN", "JFK"],
["JFK", "LGA"],
["EYW", "LHR"],
["LHR", "SFO"],
["SFO", "SAN"],
["SFO", "DSM"],
["SAN", "EYW"]
]
 
STARTING_AIRPORT = "LGA"


''' Main. '''
def main():

    # O(n)
    (direct_routes_dict, inverse_direct_routes_dict) = create_direct_routes_dicts()

    airports = set(AIRPORTS)
    airports.remove(STARTING_AIRPORT)

    # O(n+m)
    missing_routes = get_missing_routes(airports, direct_routes_dict)
    if len(missing_routes) == 0:
        print(STARTING_AIRPORT + " already reaches all airports.")
        return

    # O(n*2(n+m))
    (full_routes_dict, inverse_full_routes_dict) = create_full_routes_dicts(
            airports, direct_routes_dict, inverse_direct_routes_dict, missing_routes)

    # Calculate the minimum new routes to add to ROUTES for reaching all
    # airports from STARTING_AIRPORT
    new_minimum_routes = retrieve_new_needed_routes(
            full_routes_dict, inverse_full_routes_dict, missing_routes)

    pretty_pring_new_needed_routes(new_minimum_routes)

''' 
    Creates the dictionaries 'OriginAirport -> Set<DestinationAirport>' and 
    'DestinationAirport <- Set<OriginAirport>' of DIRECT routes (no stopovers).
'''
def create_direct_routes_dicts():

    routes_dict = dict()
    inverse_routes_dict = dict()

    for route in ROUTES:
        if route[0] in routes_dict:
            routes_dict[route[0]].add(route[1])
        else:
            routes_dict[route[0]] = {route[1]}
        if route[1] in inverse_routes_dict: 
            inverse_routes_dict[route[1]].add(route[0])
        else:
            inverse_routes_dict[route[1]] = {route[0]}

    return (routes_dict, inverse_routes_dict)

''' Returns the STARTING_AIRPORT unavailable routes. '''
def get_missing_routes(airports, direct_routes_dict):

    starting_airport_available_destinations = retrieve_airport_available_routes(
            STARTING_AIRPORT, direct_routes_dict, set())
    if STARTING_AIRPORT in starting_airport_available_destinations:
        starting_airport_available_destinations.remove(STARTING_AIRPORT)

    return airports.difference(starting_airport_available_destinations)

''' Returns the airport available routes to fly to. '''
def retrieve_airport_available_routes(airport, direct_routes_dict, airport_available_routes):

    if airport in direct_routes_dict:      
        for dest_airport in direct_routes_dict[airport]:
            if dest_airport not in airport_available_routes:
                airport_available_routes.add(dest_airport)
                airport_available_routes.intersection(
                        retrieve_airport_available_routes(
                                dest_airport, direct_routes_dict, airport_available_routes))

    return airport_available_routes  

''' 
    Creates the dictionaries 'OriginAirport -> Set<DestinationAirport>' and
    'DestinationAirport <- Set<OriginAirport>' of FULL routes (with stopovers).
'''
def create_full_routes_dicts(airports, direct_routes_dict,inverse_direct_routes_dict, missing_routes):

    full_routes_dict = dict()
    inverse_full_routes_dict = dict()

    for airport in airports: 
        airport_available_routes = retrieve_airport_available_routes(airport, direct_routes_dict, set())
        if airport in airport_available_routes:
            airport_available_routes.remove(airport)
        full_routes_dict[airport] = airport_available_routes
        # Calculate the full inverse routes ONLY for the missing STARTING_AIRPORT routes
        if airport in missing_routes:
            airport_inverse_available_routes = retrieve_airport_available_routes(
                    airport, inverse_direct_routes_dict, set())
            if airport in airport_inverse_available_routes:
                airport_inverse_available_routes.remove(airport)
            inverse_full_routes_dict[airport] = airport_inverse_available_routes

    return (full_routes_dict, inverse_full_routes_dict)

''' Calculates the minimum new routes to add to ROUTES for reaching all airports from STARTING_AIRPORT. '''
def retrieve_new_needed_routes(full_routes_dict, inverse_full_routes_dict, missing_airports):

    # missing_airports : the airports that STARTING_AIRPORT cannot originally reach
    # full_routes_dict : the 'Airport -> Set<DestinationAirport>' map
    # inverse_full_routes_dict : the 'DestinationAirport <- Set<Airport>' map

    new_needed_routes = []

    done = False
    # Assuming you won't have an inifite loop.
    while not done:

        best_missing_airport_route = None

        missing_airport = missing_airports.pop()
        for origin_airport in inverse_full_routes_dict[missing_airport]:
            count = 0
            for destination_airport in full_routes_dict[origin_airport]:
                if destination_airport in missing_airports:
                    count += 1
            if best_missing_airport_route is None:
                best_missing_airport_route = [origin_airport, count]
            elif count > best_missing_airport_route[1]:
                best_missing_airport_route = [origin_airport, count]

        if best_missing_airport_route is None:
            best_missing_airport_route = [missing_airport, -1]

        new_needed_route = best_missing_airport_route[0]

        new_needed_routes.append(new_needed_route)
        best_new_route_destinations = full_routes_dict[new_needed_route]
        best_new_route_destinations.add(new_needed_route)
        missing_airports = list(set(missing_airports).difference(best_new_route_destinations))
        if len(missing_airports) == 0:
            done = True

    return new_needed_routes

''' Pretty prints the new minimum needed routes. '''
def pretty_pring_new_needed_routes(new_needed_routes):
    print("New minimum routes:")
    for new_route in new_needed_routes:
        print(STARTING_AIRPORT + " - > " + new_route)

if __name__ == '__main__':
    main()