import pprint
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")

db = client.test
collection = db.Client_Account

# Sample client account data
client_accounts = [
    {
        "client_name": "Fatima",
        "cpf": 123456789,
        "address": "São Paulo",
        "accounts": [
            {"type": "Conta Corrente", "agency": "1234", "number": 1, "balance": 1000},
            {"type": "Conta Poupança", "agency": "5678", "number": 2, "balance": 500}
        ]
    },
    {
        "client_name": "George",
        "cpf": 987654321,
        "address": "Rio de Janeiro",
        "accounts": [
            {"type": "Conta Corrente", "agency": "5678", "number": 3, "balance": 2000},
            {"type": "Conta Poupança", "agency": "1234", "number": 4, "balance": 1500}
        ]
    },
    {
        "client_name": "Guilherme",
        "cpf": 135798642,
        "address": "Rio Grande do Sul",
        "accounts": [
            {"type": "Conta Corrente", "agency": "1234", "number": 5, "balance": 3000},
            {"type": "Conta Poupança", "agency": "5678", "number": 6, "balance": 2000}
        ]
    },
    {
        "client_name": "Vivianne",
        "cpf": 246897541,
        "address": "Minas Gerais",
        "accounts": [
            {"type": "Conta Corrente", "agency": "5678", "number": 7, "balance": 2500},
            {"type": "Conta Poupança", "agency": "1234", "number": 8, "balance": 1800}
        ]
    }
]

# Insert client account data into the collection
for account_data in client_accounts:
    result = collection.insert_one(account_data)
    print(f"Inserted client account with ID: {result.inserted_id}")

# Print all documents in the collection
print("Todos os documentos na coleção Client_Account:")
for document in collection.find():
    pprint.pprint(document)

# Search for one client by name
print("\nRecuperando documento por nome de cliente:")
pprint.pprint(collection.find_one({"client_name": "George"}))

# Search for clients with a balance above 2000
print("\nRecuperando todos documentos com saldo acima de 2000:")
for document in collection.find({"accounts.balance": {"$gt": 2000}}):
    pprint.pprint(document)

# Search for all clients and only their Conta Corrente accounts
print("\nRecuperando todos os clientes e suas contas correntes:")
for document in collection.find({}, {"accounts": {"$elemMatch": {"type": "Conta Corrente"}}}):
    pprint.pprint(document)
