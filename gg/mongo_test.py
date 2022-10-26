from pymongo import MongoClient

client = MongoClient('mongodb://rouser:piL7VcU5WQ@events.goodgame.ru:27017/stats')

print('БАЗЫ ДАННЫХ:', client.list_database_names())

db = client['stats']
website = db['website']

print('КОЛЛЕКЦИИ:', website)