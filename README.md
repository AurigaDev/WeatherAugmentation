# WeatherAugmentation

Given geo-located data, for machine learning/deep learning purposes, apply coarse weather attribution by looking at best consistent data available.

In US, weather underground has hundreds of sensors in large cities, and very fine granularity around rural US. For locations outside the US there is no high resolution data available for weather, so leverages Airport weather sensors around the world.

Airports need fairly high accuracy sensors, and fairly high frequency which covers high accuracy, high frequency, and decent coverage around the world, including lower developed countries as weather reporting standards are set internationally. METAR stations are of specific interest.

To assign weather discretely, coordinates are applied through reference point, current implementation required looking for cloest stations in a given country, but this can easily be aggregated for all stations in world. 

# Original Design and Design Considerations.

Original design leveraged https://en.wikipedia.org/wiki/Voronoi_diagram but this was generalized to KDTree structure, to collect k nearest points, which would be useful for more fine-grain analysis. The main considerations for KDTree was performance and being able to maintain multiple nearest points to check each nearby station for consistentish weather. 

# Limitation

The issue with coarse analysis is while weather in general will not change drastically in short spatial locality, there are natural boundaries such as mountains and deserts which can create barriers for many of the features of interest including visibility, temperature, and percipitation. Therefore by looking at the k closest stations, more trust can be built on data if there is concensus. Additionally if a data source such as an earth wind map can be crawled and interpreted for downwind, and added with meteorologist expertise, more assurance can be made on the quality of data.

