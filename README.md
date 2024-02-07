# ep-bandpass-filter-selector

The EP Bandpass Filter Selector package cycles through various combinations of high- and low-pass cutoffs of the bandpass frequency filter within user-specified limits and selects the optimal filtering option. Optimization is carried out basing on the ratio of the EP interpeak amplitude to the EP curves variability coefficient.


## Requirements

Package require python >= 3.11.5.
For development require python3-venv.
Tested on Manjaro Linux.


## Installation

For usual using:

```
$ pip install ep_bandpass_filter_selector
```

For development:

```
$ git clone https://github.com/yaricp/ep-bandpass-filter-selector.git
$ cd ep-bandpass-filter-selector/
$ scripts/./install.sh
```

`install.sh` will download and set up the necessary packages in the .venv folder.


## Usage

This package can be imported as a separated module:

```
$ python3
>>> from eeg_filters.upload import prepare_data
>>> from ep_bandpass_filter_selector import PassbandSelector
>>> (
    sample_rate, list_times, list_ticks, list_out
) = prepare_data("file_data_path.dat")
>>> pbs = PassbandSelector(
    curves=list_out,
    tick_times=list_ticks,
    fsr=sample_rate,
    max_search_range: (0.016, 0.023),
    min_search_range: (0.022, 0.028)
)
>>> result = pbs.start()
>>> print(result[0])
20,200
```
In this example, all curves from the file_data_path.dat were used for selecting the passband filter.
Also, additional parameters were used with the default values. 
Their values are listed here:

filter_low_limit_range = 1, 30
step_low_filter = 1
filter_high_limit_range = 100, 500
step_high_filter = 10

You can declare them when creating an item of PassbandSelector.
For example:

```
>>> pbs = PassbandSelector(
    curves=list_out,
    tick_times=list_ticks,
    fsr=sample_rate,
    max_search_range=(0.016, 0.023),
    min_search_range=(0.022, 0.028),
    filter_low_limit_range=[5, 20],
    step_low_filter=5,
    filter_high_limit_range=[100, 300],
    step_high_filter=50,
    type_mean="average",
    cheb_filter_order=3,
    cheb_ripple=3
)
```
Another notation is also possible for declaring parameters.
For example:

```
>>> pbs = PassbandSelector(
    curves=list_out,
    tick_times=list_ticks,
    fsr=sample_rate,
    max_search_range=(0.016, 0.023),
    min_search_range=(0.022, 0.028),
    fllr=[5, 20],
    slf=5,
    fhlr=[100, 300],
    shf=50,
    tm="average",
    chfo=3,
    chr=3
)
```

## Export data

On this moment there is only export to CSV format.

```
>>> from ep_bandpass_filter_selector import export_data
>>> export_data(
    "filepath_for_export.csv",
    list(result[0]),
    result[1]
) 
```
