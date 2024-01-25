import pytest
from ep_bandpass_filter_selector import (
    PassbandSelector, export_data
)


@pytest.fixture()
def prepare_item_pbs():
    """Fixture for create and delete PassbandSelector item."""
    pbs = PassbandSelector(

    )
    yield pbs
    print("something after test")


class TestPassbandSelector:
    pbs = PassbandSelector(
        curves=[],
        tick_times=[],
        fsr=25,
        max_search_range=(0.02, 0.03),
        min_search_range=(0.05, 0.06),
    )

    def test_get_reproduct(self):
        filtered_curves = [
            [1,2,3,4,5],
            [1,2,2,4,5],
            [1,2,3,3,5]
        ]
        result = self.pbs.get_reproduct(filtered_curves)
        assert result == 1

    def test_get_delta_extremum(self):
        filtered_curves = [
            [1,2,3,4,5],
            [1,2,2,4,5],
            [1,2,3,3,5]
        ]
        result = self.pbs.get_delta_extremum(filtered_curves)
        assert result == 2