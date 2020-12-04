from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, CountVectorizer

sparkSession = SparkSession.builder.appName("tf idf Notebook").getOrCreate()
sc = sparkSession.sparkContext
hdfs_nn = "172.31.67.32"
reviews = sparkSession.read.options(header= True).csv("hdfs://%s:9000/user/hadoop/Reviews/part-m-00000" % (hdfs_nn))
# reviews.show()

reviews = reviews.filter(reviews.reviewText.isNotNull()).select("asin","reviewText") #982597

#Use tokenizer to seperate each word for each sentences
tokenizer_word = Tokenizer(inputCol="reviewText", outputCol="Words")
#After tokenizer, we added one col(Words to table) 
words_Data = tokenizer_word.transform(reviews)
# words_Data.show(5)
#Count the number of words
countvectorizer = CountVectorizer(inputCol="Words", outputCol="raw_features")
model = countvectorizer.fit(words_Data)
#Add count to our table
get_count_data = model.transform(words_Data)
#get_count_data.show(5)
#calculate TF-IDF 
idf_value = IDF(inputCol="raw_features", outputCol="idf_value")
idf_model = idf_value.fit(get_count_data)
final_rescaled_data = idf_model.transform(get_count_data)
#final_rescaled_data.show(5)
final_rescaled_data.select("idf_value").show()
#vocabulary list
vocabalary = model.vocabulary

#Calculate TF-IDF 
def extract(value):
    return {vocabalary[i]: float(tfidf_value) for (i, tfidf_value) in zip(value.indices, value.values)}

def save_as_string(value):
    words = ""
    for (i, tfidf_value) in zip(value.indices, value.values):
        temp_value = vocabalary[i] + ":" + str(float(tfidf_value)) + ", "
        words += temp_value
    return words[:-2]

output_file = final_rescaled_data.select('asin','reviewText', 'idf_value').rdd.map(
    lambda x: [x[0], x[1], save_as_string(x[2])])

output_df = sparkSession.createDataFrame(output_file,['asin','reviewText', 'idf_value'])
output_df.show()
output_df.write.csv("hdfs://%s:9000/output/reviews_tfidf_dir" % (hdfs_nn))
sc.stop()
