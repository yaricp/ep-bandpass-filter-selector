from src.passband_searcher import PassbandSearcher


class TestPassBandSearcher:
    pbs = PassbandSearcher(
        curves=[],
        filter_borders={"low":[0,0,1], "high": [0,0,1]},
        tick_times=[],
        where_search_extremums=[],
        check_average=True,
        check_square=False,
        config_filter={}
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