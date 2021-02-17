# amazon-location-geofence-uploader

This utility script uploads geofences defined as GeoJSON into an ![Amazon Location Service](https://aws.amazon.com/location/) geofence collection.

## Usage

```
./upload_geofence.py <file> <geofence_collection_name>
```

Where:

* `file`: path to the GeoJSON file containing the geofences.
* `geofence_collection_name`: name of the geofence collection as defined in Amazon Location Service.

## Working mechanism

The script will iterate through all the features defined in the GeoJSON file and will upload those of type `Polygon`, ignoring the rest. Polygons can be defined as the sole feature, or within a `FeatureCollection`.

## ID generation

Amazon Location Service expects an ID for each geofence. The script currently assigns an ID following these steps:

1. If the GeoJSON polygon has a property called `id`, then that's what will be used.
2. If not, then a UUIDv4 identifier is generated.


For example, this will use the provided ID:

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [
        [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
        [100.0, 1.0], [100.0, 0.0]
      ]
    ]
  },
  "properties": {
    "id": "MyGeofenceId"
  }
}
```

Whereas this will produce an automatically-generated ID:

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [
        [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
        [100.0, 1.0], [100.0, 0.0]
      ]
    ]
  }
}
```
