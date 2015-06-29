# Welcome!

Python-daqss is a python module that serves as a wrapper around the API for the Dorchester Air Quality Sensor Study (DAQSS). The module makes it simple to access air quality data for the project. As of summer 2015, there are a total of five sensor nodes deployed in Dorchester, MA.

Each node continuously measures ozone (O3), nitrogen oxide (NO), nitrogen dioxide (NO2), carbon monoxide (CO), relative humidity (RH), temperature (T), and particulate matter (PM).

The API is key, password protected; credentials can be obtained by emailing <a href="mailto:dhagan@mit.edu">dhagan@mit.edu</a>.

## Installation

You can easily install the python module a couple of different ways:

### git

    >>> git clone https://github.com/dhhagan/python-daqss.git
    >>> cd python-daqss
    >>> python setup.py install

### wget

    >>> wget https://github.com/dhhagan/python-daqss/archive/master.zip
    >>> unzip master.zip
    >>> cd python-daqss/
    >>> sudo python setup.py install

## Quickstart

Once you have obtained credentials and installed the library, you can set up an instance of the `Daqqs` class:

    import daqss
    api = daqss.Daqss(api_key, api_pswd)

You can check to see if your credentials work by pinging the server which will print `True` if everything is a go!

    api.ping()

Typically, each call returns a tuple containing the API response status and the response json. An example of a call to get a list of all of the nodes would look something like this:

    status, resp = api.get_nodes()


The entire API wrapper is documented under the [API page](/API)!
