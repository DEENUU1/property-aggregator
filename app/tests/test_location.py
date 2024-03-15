import os
import sys

from conftest import test_get_db
from repositories.region_repository import RegionRepository
from schemas.location import RegionInput

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_create_region(test_get_db):
    repository = RegionRepository(test_get_db)
    created_region = repository.create(RegionInput(name="Test Region"))
    assert created_region.name == "Test Region"


def test_get_all_regions(test_get_db):
    repository = RegionRepository(test_get_db)
    repository.create(RegionInput(name="Test Region"))
    regions = repository.get_all()
    assert len(regions) == 2


def test_get_region_by_id(test_get_db):
    repository = RegionRepository(test_get_db)
    created_region = repository.create(RegionInput(name="Test Region"))
    fetched_region = repository.get_by_id(created_region.id)
    assert fetched_region.name == "Test Region"


def test_update_region(test_get_db):
    repository = RegionRepository(test_get_db)
    created_region = repository.create(RegionInput(name="Test Region"))
    region = repository.get_by_id(created_region.id)
    updated_region_input = RegionInput(name="Updated Region")
    updated_region = repository.update(region, updated_region_input)
    assert updated_region.name == "Updated Region"


def test_delete_region(test_get_db):
    repository = RegionRepository(test_get_db)
    created_region = repository.create(RegionInput(name="Test Region"))
    region = repository.get_by_id(created_region.id)
    assert repository.delete(region)
