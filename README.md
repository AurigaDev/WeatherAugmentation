# WeatherAugmentation

Given geo-located data, for machine learning/deep learning purposes, apply coarse weather attribution by looking at best consistent data available.

In US, weather underground has hundreds of sensors in large cities, and very fine granularity around rural US. For locations outside the US there is no high resolution data available for weather, so leverages Airport weather sensors around the world.

Airports need fairly high accuracy sensors, and fairly high frequency which covers high accuracy, high frequency, and decent coverage around the world, including lower developed countries as weather reporting standards are set internationally. METAR stations are of specific interest.

To assign weather discretely, coordinates are applied through reference point, current implementation required looking for cloest stations in a given country, but this can easily be aggregated for all stations in world. 

# Original Design and Design Considerations.

Original design leveraged https://en.wikipedia.org/wiki/Voronoi_diagram but this was generalized to KDTree structure, to collect k nearest points, which would be useful for more fine-grain analysis. The main considerations for KDTree was performance and being able to maintain multiple nearest points to check each nearby station for consistentish weather. METAR stations were selected for decent distribution, international requirements on quality, and ability to assign weather to events retroactively and globally. METAR data is saved since recording began, while the quality has drifted in the positive direction over time with additional features being added with newer features, in general was selected as best possible source for international selection. Open Weather Map was looked at for domestic data for extremly high resolution, and being able to query data through library directly, but no history, or guarentee on quality of data was found.

Open Weather Map also used to validate with high granular data exactly on weather sensor of OWM but not included in METAR stations. Approximate weather can be diffed for temperature, perciptiation, and visibility such that accuracy of coarse approximation can be measured.

# Limitation

The issue with coarse analysis is while weather in general will not change drastically in short spatial locality, there are natural boundaries such as mountains and deserts which can create barriers for many of the features of interest including visibility, temperature, and percipitation. Therefore by looking at the k closest stations, more trust can be built on data if there is concensus. Additionally if a data source such as an earth wind map can be crawled and interpreted for downwind, and added with meteorologist expertise, more assurance can be made on the quality of data. 

# Execution

python Weather.py

This queries user for country of interest, in this example was looking at highly diverse terrain and looking for weather samples that varied greatly at the time in region with numerous natural boundaries, so chose area in middle east. 
