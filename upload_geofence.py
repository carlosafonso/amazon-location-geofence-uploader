#!/usr/bin/env python

import argparse
import boto3
import geojson
import itertools
import logging
import uuid


logging.basicConfig(level='INFO')
logger = logging.getLogger()


class PropertyBasedIdGenerator(object):
	def generate_id(self, feature):
		if 'properties' in feature and 'id' in feature.properties:
			return feature.properties['id']
		return uuid.uuid4()


def parse_geojson(data, id_generator):
	if data.type == 'FeatureCollection':
		polygons = list(filter(lambda x: x != None, [parse_geojson(f, id_generator) for f in data.features]))
		return list(itertools.chain(*polygons))
	if data.type == 'Feature' and data.geometry.type == 'Polygon':
		return [
			{
				'GeofenceId': str(id_generator.generate_id(data)),
				'Geometry': {
					'Polygon': data.geometry.coordinates
				}
			}
		]

	logger.warning('Skipping feature with geometry type %s' % (data.geometry.type))
	return None


def main(file, geofence_collection):
	als_client = boto3.client('location')
	id_generator = PropertyBasedIdGenerator()

	try:
		with open(file, 'r') as f:
			polygons = parse_geojson(geojson.load(f), id_generator)

			response = als_client.batch_put_geofence(
				CollectionName=geofence_collection,
				Entries=polygons
			)

			logger.info('All geofences have been uploaded.')
	except AttributeError as e:
		logger.error('GeoJSON file does not have a valid structure (%s)' % (str(e)))
	except FileNotFoundError as e:
		logger.error('GeoJSON file "%s" could not be found (%s)' % (file, str(e)))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Helper utility to upload GeoJSON geofences to an Amazon Location Service geofence collection')
	parser.add_argument('file',
						help='The path to the GeoJSON file to be uploaded as a new geofence')
	parser.add_argument('geofence_collection',
						help='The name of the geofence collection defined in Amazon Location Service')
	args = parser.parse_args()
	main(args.file, args.geofence_collection)
