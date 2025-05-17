import pyspark
from delta import *
from delta.tables import *
from pyspark.sql.functions import *

builder = pyspark.sql.SparkSession.builder.appName("MyApp") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

deltaTable = DeltaTable.forPath(spark, "/tmp/delta-table")

# Update every even value by adding 100 to it
print('Update every even value by adding 100 to it')
deltaTable.update(
  condition = expr("id % 2 == 0"),
  set = { "id": expr("id + 100") })

# Delete every even value
print('Delete every even value')
deltaTable.delete(condition = expr("id % 2 == 0"))

# Upsert (merge) new data
print('Upsert (merge) new data')
newData = spark.range(0, 20)

deltaTable.alias("oldData") \
  .merge(
    newData.alias("newData"),
    "oldData.id = newData.id") \
  .whenMatchedUpdate(set = { "id": col("newData.id") }) \
  .whenNotMatchedInsert(values = { "id": col("newData.id") }) \
  .execute()

deltaTable.toDF().show()

# Read old version of the table
print('Read old version of the table')
df = spark.read.format("delta").option("versionAsOf", 0).load("/tmp/delta-table")
df.show()

# next examples doesn't work
# Write a stream of data to a table
print('Write a stream of data to a table')
streamingDf = spark.readStream.format("rate").load()
stream = streamingDf.selectExpr("value as id").writeStream.format("delta").option("checkpointLocation", "/tmp/checkpoint").start("/tmp/delta-table")

#Read a stream of changes from a table
print('Read a stream of changes from a table')
stream2 = spark.readStream.format("delta").load("/tmp/delta-table").writeStream.format("console").start()