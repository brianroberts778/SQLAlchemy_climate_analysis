# SQLAlchemy Climate Analysis

## Step 1 - Climate Analysis and Exploration
Uses Python and SQLAlchemy to do basic climate analysis and data exploration of a climate database. All of the following analysis is completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* Chose a start date and end date for your trip. Make sure that your vacation range is approximately 3-15 days total.
* Uses SQLAlchemy `create_engine` to connect to the sqlite database.
* Uses SQLAlchemy `automap_base()` to reflect the tables into classes and save a reference to those classes called `Station` and `Measurement`.

### Precipitation Analysis

* Designs a query to retrieve the last 12 months of precipitation data.
* Selected only the `date` and `prcp` values.
* Loads the query results into a Pandas DataFrame and set the index to the date column.
* Sorts the DataFrame values by `date`.
* Plots the results using the DataFrame `plot` method.
* Uses Pandas to print the summary statistics for the precipitation data.

### Station Analysis

* Designed a query to calculate the total number of stations.
* Designed a query to find the most active stations.
  * Lists the stations and observation counts in descending order.
  * Determines which station has the highest number of observations.
* Designed a query to retrieve the last 12 months of temperature observation data (TOBS).
  * Filtered by the station with the highest number of observations.
  * Plots the results as a histogram with `bins=12`.
  
- - -

## Step 2 - Climate App

Now that the initial analysis is complete, I've designed a Flask API based on the queries developed above.

* Uses Flask to create your routes.

### Routes

* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`
  * Converts the query results to a dictionary using `date` as the key and `prcp` as the value.
  * Returns the JSON representation of the dictionary.

* `/api/v1.0/stations`
  * Returns a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * Query the dates and temperature observations of the most active station for the last year of data.
  * Return a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
  * Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
  * When given the start only, calculates `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
  * When given the start and the end date, calculates the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

- - -
