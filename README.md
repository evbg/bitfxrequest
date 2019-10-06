[![Code style:
black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

# bitfxrequest

bitfxrequest - a simple client for the bitfinex REST API: https://api-pub.bitfinex.com/v2/ which helps to get a list of symbols of such currencies which have an exchange rate against the dollar, and also get the values of the last CLOSE and average VOLUME for the last 10 days.

---

*Contents:*
**[Installation](#installation)** |
**[Requirements](#requirements)** |
**[Versioning](#versioning)** |
**[Authors](#authors)** |
**[License](#license)**

---

## Getting Started

### Installation

#### Manual install
```
git clone https://github.com/evbg/bitfxrequest.git
cd bitfxrequest
python setup.py install
```

#### Installing directly from the [repository](https://github.com/evbg/bitfxrequest) on GitHub.com
```
pip install git+https://github.com/evbg/bitfxrequest.git
```


### Requirements

bitfxrequest requires [requests](https://pypi.org/project/requests/) library.


## Versioning

We use [SemVer](http://semver.org/) for versioning.


## Authors

* **Evgeny V. Bogodukhov** - *Initial work* - [evbg](https://github.com/evbg)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
