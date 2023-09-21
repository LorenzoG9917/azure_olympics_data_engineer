## Notebook de transformación de la data , este notebook es el que se menciona en el paso 14.
configs = {"fs.azure.account.auth.type": "OAuth",
"fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
"fs.azure.account.oauth2.client.id": "[Application(client)ID]" # ACTUALIZAR,
"fs.azure.account.oauth2.client.secret": '[Secretkey(Value)]' # ACTUALIZAR,
"fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/[Directory(tenant)ID]/oauth2/token" # ACTUALIZAR}

dbutils.fs.mount(
source = "abfss://[NombreContainer]@[NombreStorageAccount].dfs.core.windows.net", # contrainer@storageacc
mount_point = "/mnt/tokyoolymic",
extra_configs = configs)

%fs
  ls "mnt/tokyoolymic"

spark # IT'S NO neccesary to create spark session because data bricks already configurate this

athletes = spark.read.format("csv").option("header","true").load("/mnt/tokyoolymic/raw-data/athletes.csv")
coaches = spark.read.format("csv").option("header","true").load("/mnt/tokyoolymic/raw-data/coaches.csv")
entriesgender = spark.read.format("csv").option("header","true").load("/mnt/tokyoolymic/raw-data/entriesgender.csv")
medals = spark.read.format("csv").option("header","true").option("inferSchema","True").load("/mnt/tokyoolymic/raw-data/medals.csv") # infer Schema to get the correct dtype from the columns
teams = spark.read.format("csv").option("header","true").option("inferSchema","True").load("/mnt/tokyoolymic/raw-data/teams.csv") # infer Schema to get the correct dtype from the columns


# Get the data in the proper format
# Manually apply the correct format
# Convert all the dtype of the columns to integer
entriesgender = entriesgender.withColumn("Female",col("Female").cast(IntegerType()))\
    .withColumn("Male",col("Male").cast(IntegerType()))\
    .withColumn("Total",col("Total").cast(IntegerType()))


# Find the top countries with the Highest number of gold medals
top_gold_medals_countries = medals.orderBy("Gold",ascending=False).select("Team_Country","Gold")


# Calculate the average number of entries by gender for each discipline

average_entries_by_gender = entriesgender.withColumn(
    'Avg_Female',entriesgender['Female'] / entriesgender['Total']
).withColumn(
    'Avg_Male',entriesgender['Male'] / entriesgender['Total']
)

average_entries_by_gender.show()



# Write the data in the folder transformed-data
athletes.repartition(1).write.mode("overwrite").option("header","true").csv('/mnt/tokyoolymic/transformed-data/athletes')
coaches.repartition(1).write.mode("overwrite").option("header","true").csv('/mnt/tokyoolymic/transformed-data/coaches')
entriesgender.repartition(1).write.mode("overwrite").option("header","true").csv('/mnt/tokyoolymic/transformed-data/entriesgender')
medals.repartition(1).write.mode("overwrite").option("header","true").csv('/mnt/tokyoolymic/transformed-data/medals')
teams.repartition(1).write.mode("overwrite").option("header","true").csv('/mnt/tokyoolymic/transformed-data/teams')
top_gold_medals_countries.repartition(1).write.mode("overwrite").option("header","true").csv('/mnt/tokyoolymic/transformed-data/top_gold_medals_countries')
average_entries_by_gender.repartition(1).write.mode("overwrite").option("header","true").csv('/mnt/tokyoolymic/transformed-data/average_entries_by_gender')
