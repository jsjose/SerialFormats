# write a serliazed avro file to disk and read it back in and print it out to the console using a strucutred schema with name, favorite_number, and favorite_color
# Usage: python AvroExample.py <avro file name> <schema file name> <name> <favorite_number> <favorite_color>   
# Example: python AvroExample.py test.avro schema.avsc "John Doe" 7 "red"

import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import sys

# Load the schema from the file
schema = avro.schema.parse(open(sys.argv[2], "rb").read())

# Write the data to the file
writer = DataFileWriter(open(sys.argv[1], "wb"), DatumWriter(), schema)
writer.append({"name": sys.argv[3], "favorite_number": int(sys.argv[4]), "favorite_color": sys.argv[5]})
writer.close()

# Read the data from the file
reader = DataFileReader(open(sys.argv[1], "rb"), DatumReader())
for user in reader:
    print (user)
reader.close()

# generate the schema file using the following command and save it to a file
# python -m avro.schema schema.avsc schema.json     # where schema.avsc is the schema file and schema.json is the output file
# can you generate an example schema file using the following command and save it to a file

# python -m avro.schema example.avsc example.json
# { "type": "record", "name": "example", "fields": [ { "name": "name", "type": "string" }, { "name": "favorite_number", "type": "int" }, { "name": "favorite_color", "type": "string" } ] }
# od -v -t x1z users.avro