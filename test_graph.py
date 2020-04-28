from ariadne import graphql_sync
from type_defs import schema
import json

RESIDENT_QUERY = """
query {
  residentById(_id: 1) {
    name
  }
}
"""

BUILDING_QUERY = """
query {
  buildingById(_id: 1) {
    name
  }
}
"""

DEEP_BUILDING_QUERY = """
query {
  buildingById(_id: 1) {
    name
    residents {
      name
      building {
        name
      }
    }
  }
}
"""


def test_residentById():
    data = {"query": RESIDENT_QUERY}
    success, result = graphql_sync(schema, data)
    assert success == True
    assert result["data"]["residentById"]["name"] == "Dino"


def test_buildingById():
    data = {"query": BUILDING_QUERY}
    success, result = graphql_sync(schema, data)
    assert success == True
    assert result["data"]["buildingById"]["name"] == "Barfy Gardens"


def test_buildingById_deep():
    data = {"query": DEEP_BUILDING_QUERY}
    success, result = graphql_sync(schema, data)
    assert success == True
    assert result["data"]["buildingById"]["name"] == "Barfy Gardens"
    assert result["data"]["buildingById"]["residents"][0]["name"] == "Dino"
    assert (
        result["data"]["buildingById"]["residents"][0]["building"]["name"]
        == "Barfy Gardens"
    )
