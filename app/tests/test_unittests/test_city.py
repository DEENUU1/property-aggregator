import os
import sys

import pytest

from ..conftest import test_get_db
from repositories.city_repository import CityRepository
from repositories.region_repository import RegionRepository
from schemas.location import CityInput, RegionInput

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture()
def region(test_get_db):
    repository = RegionRepository(test_get_db)
    region = repository.create(RegionInput(name="Łódzkie"))
    return region


def test_success_create_city_object(test_get_db, region) -> None:
    repository = CityRepository(test_get_db)
    city = repository.create(CityInput(name="Uć", region_id=region.id))

    assert city.name == "Uć"
    assert city.region_id == region.id


def test_success_get_all_city_objects(test_get_db, region) -> None:
    repository = CityRepository(test_get_db)
    repository.create(CityInput(name="Uć", region_id=region.id))
    repository.create(CityInput(name="Łódź", region_id=region.id))

    get_all = repository.get_all()
    assert len(get_all) == 2
    assert get_all[0].name == "Uć"
    assert get_all[1].name == "Łódź"


def test_success_get_all_city_objects_by_region(test_get_db, region) -> None:
    repository = CityRepository(test_get_db)
    repository.create(CityInput(name="Uć", region_id=region.id))
    repository.create(CityInput(name="Łódź", region_id=region.id))

    get_all = repository.get_all_by_region(region.id)
    assert len(get_all) == 2
    assert get_all[0].name == "Uć"
    assert get_all[1].name == "Łódź"


def test_success_city_exists_by_name(test_get_db, region) -> None:
    repository = CityRepository(test_get_db)
    repository.create(CityInput(name="Uć", region_id=region.id))

    assert repository.city_exists_by_name("Uć")
