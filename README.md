# Tom Pichard Capstone

## Below, Update from April 28 2016

Progress to date is the following and all these steps involved much discovery, elaboration and learning:

* I was able to load historical stock time-series data (IBM for this POC) leveraging the [Yahoo_Finance module]( https://pypi.python.org/pypi/yahoo-finance/1.2.1#usage-examples) which natively created a Pandas dataframe with the OpenHighLowClose data.
* Several data transformation steps were then performed to prepare the data for processing and visualization:
 * Re-sorting and re-indexing of the data.
 * Normalizing the OHL data for historical adjustment to the stock's adjusted historical closing price which translated into writing functions to populate new columns in the original dataset based on conditional data in said dataset.
* Next, I was able to leverage the [matplotlib.finance module](http://matplotlib.org/api/finance_api.html) to render OHLC bar charts for the historical data.
* Then, I wrote a loop method to identify local lows. These local low placements in time within the time-series were then appended to the dataset with an identifying column (LLOW). This series is going to provide the foundational data from which to create the trading model.

The steps above can be viewed in the current notebook called Build001 located in this repo. 



##Below, initial update from March 31 2016

A particular stock chart pattern that I have witnessed in the past has intrigued me. I used to call it the parabolic acceleration pattern. Its characteristic configuration is defined by not only higher lows over a defined time period but lows that progressively go higher. The curve that fits underneath the lows in the establishing timeframe appears to be non- linear, i.e., a typical straight trendline does not fit but rather a form that is more  hyperbolic, exponential, non linear does.

I have witnessed this pattern many times and i have associated it with a stock or commodity 'breaking out' to the upside. But this evidence is anecdotal to my own point of view and I would like to validate it with real data over a broad spectrum. The question I would like to answer then is the following: Once this 'power' pattern is identified in the inital timeframe, how predictive of ensuing gains is it in a timeframe of equal magnitude to the set-up timeframe?

I will use stock data from Yahoo Finance using historical daily time series of highs, lows, and closes.

I am very familiar with the stock market and its patterns. I worked in the markets several years ago and so I chose this subject area because of the familiarity I have with it, and my continuing interest in the domain.

I think that the scope is reasonable for a capstone for this class and I will learn the following while realising it:

	1- Fetch stock data from an API at scale using Python.

	2- Manipulate, munge and prepare the data for analysis using Pandas.

	3- Design elaborate Python code structures and algorithms to hunt, identify and earmark these
	patterns along a time series then build a simple trading rule for validation.

	4- Get my head into the math equations (power, exponential functions) that will be needed for
	mapping/identifying the patterns and any non-linear regressions needed.

There, that's it. I anticipate many challenges especially upfront in designing and testing the code to identify the pattern so I can work with it, also finding a general rule to map over varying stock price numbers into a generalized grid that be normalized for the curve fitting? It's one thing to identify the pattern, it's another to transcribe that pattern into a 'library' of applicable math formulas with an allowable range of expressions? I guess the simpler the better and I'll have plenty of data to dispel any overfitting errors I guess.


	

