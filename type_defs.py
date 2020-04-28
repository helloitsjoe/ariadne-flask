from ariadne import load_schema_from_path, make_executable_schema, QueryType, ObjectType
import json

type_defs = load_schema_from_path("schema.graphql")

query = QueryType()
building = ObjectType("Building")
resident = ObjectType("Resident")


@query.field("allBuildings")
def all_buildings(_, info):
    with open("./data/buildings.json") as file:
        return json.load(file)["buildings"]


@query.field("allResidents")
def all_residents(_, info):
    with open("./data/residents.json") as file:
        return json.load(file)["residents"]


@query.field("buildingById")
def building_by_id(_, info, _id):
    with open("./data/buildings.json") as file:
        data = json.load(file)
        for building in data["buildings"]:
            if building["id"] == _id:
                return building


@query.field("residentById")
def resident_by_id(_, info, _id):
    with open("./data/residents.json") as file:
        data = json.load(file)
        for resident in data["residents"]:
            if resident["id"] == _id:
                return resident


@building.field("residents")
def residents_in_building(building, info):
    with open("./data/residents.json") as file:
        data = json.load(file)
        residents = [
            resident
            for resident in data["residents"]
            if resident["building"] == building["id"]
        ]
        # The above is a different syntax for this:
        # residents = []
        # for resident in data["residents"]:
        #     print(resident)
        #     if resident["building"] == building["id"]:
        #         residents.append(resident)
        return residents


@resident.field("building")
def building_for_resident(resident, info):
    with open("./data/buildings.json") as file:
        data = json.load(file)
        for building in data["buildings"]:
            if building["id"] == resident["building"]:
                return building


# Alternative to @query.field('fieldName')...
# query.set_field("allBuildings", all_buildings)
# query.set_field("allResidents", all_residents)
# query.set_field("buildingById", building_by_id)
# query.set_field("residentById", resident_by_id)
# building.set_field("residents", residents_in_building)
# resident.set_field("building", building_for_resident)

# Note: array for bindables is deprecated, individual args preferred now
# https://ariadnegraphql.org/docs/resolvers
schema = make_executable_schema(type_defs, query, building, resident)
