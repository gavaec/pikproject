# pikproject
<br>This is a parcer to get available offers from developer in two prices for each apartment: cash and 1.99% mortgage.
<br>URL-address consist from name of residential complex and search-filters such as square, floor, price etc.
<br>File <i>parser.py</i> makes requests to get data for every residential complex and type of price and saves data as html-file.
<br>File <i>creator.py</i> gets data using beautyfull-soup from previosly saved html. Data storage is organazied as json-file with objects - apartments. If apartment already exists and price changes, it will be added to apartment price history. If apartment doesn't exist in json, it will be created.
