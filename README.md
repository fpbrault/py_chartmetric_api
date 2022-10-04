# py_chartmetric_api

py_chartmetric_api is a simple Python library for retrieving data from [chartmetrics.com](https://chartmetric.com/).

## Requirements
- Python 3.9 or later

## Installation

Clone the repository and then install the requirements

```bash
pip install requirements.txt
```

## Usage

```python
import py_chartmetric_api

# returns first 100 artists that had a first relaase 30 days ago or less
py_chartmetric_api.artist.get_artists_with_filters(0, 100, {"firstReleaseDaysAgo": "30"})

# returns 300 artists that have between 1000 and 100000 spotify followers
py_chartmetric_api.artist.get_artists_by_stats("sp_followers", 1000, 100000, 300)

```
Refer to examply.py for a more in-depth example

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)