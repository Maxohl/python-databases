from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DECIMAL
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import inspect
from sqlalchemy import select

Base = declarative_base()


from sqlalchemy.orm import relationship

class Client(Base):
    __tablename__ = "client_account"
    # attributes
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    cpf = Column(Integer, unique=True)
    endereco = Column(String(100))

    # Define the one-to-many relationship
    accounts = relationship("Account", back_populates="client")

    def __repr__(self):
        return f"Client(nome={self.nome}, cpf={self.cpf}, endereco={self.endereco})"


class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True)
    tipo = Column(String(50))
    agencia = Column(String(50))
    numero = Column(Integer)
    id_cliente = Column(Integer, ForeignKey("client_account.id"))
    saldo = Column(DECIMAL)

    # Define the many-to-one relationship
    client = relationship("Client", back_populates="accounts")

    def __repr__(self):
        return (
            f"Account(id={self.id}, "
            f"tipo={self.tipo}, "
            f"agencia={self.agencia}, "
            f"numero={self.numero}, "
            f"saldo={self.saldo})"
        )

    

# database connection
engine = create_engine("sqlite://")

# creating the tables in the database using the classes
Base.metadata.create_all(engine)

# Investigates the database schema
inspetor_engine = inspect(engine)

print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

with Session(engine) as session:
    fatima = Client(
        nome="Fatima",
        cpf=123456789,
        endereco="São Paulo"
    )

    george = Client(
        nome="George",
        cpf=987654321,
        endereco="Rio de Janeiro"
    )

    guilherme = Client(
        nome="Guilherme",
        cpf=135798642,
        endereco="Rio Grande do Sul"
    )

    vivianne = Client(
        nome="Vivianne",
        cpf=246897541,
        endereco="Minas Gerais"
    )

    # Creating account instances for each client
    fatima_accounts = [
        Account(tipo="Conta Corrente", agencia="1234", numero=1, saldo=1000),
        Account(tipo="Conta Poupança", agencia="5678", numero=2, saldo=500)
    ]
    george_accounts = [
        Account(tipo="Conta Corrente", agencia="5678", numero=3, saldo=2000),
        Account(tipo="Conta Poupança", agencia="1234", numero=4, saldo=1500)
    ]
    guilherme_accounts = [
        Account(tipo="Conta Corrente", agencia="1234", numero=5, saldo=3000),
        Account(tipo="Conta Poupança", agencia="5678", numero=6, saldo=2000)
    ]
    vivianne_accounts = [
        Account(tipo="Conta Corrente", agencia="5678", numero=7, saldo=2500),
        Account(tipo="Conta Poupança", agencia="1234", numero=8, saldo=1800)
    ]

    # Assigning accounts to clients
    fatima.accounts.extend(fatima_accounts)
    george.accounts.extend(george_accounts)
    guilherme.accounts.extend(guilherme_accounts)
    vivianne.accounts.extend(vivianne_accounts)

    # Adding clients and accounts to the session
    session.add_all([fatima, george, guilherme, vivianne])

    # Committing changes
    session.commit()


search_query_client = select(Client).where(Client.nome.in_(["Guilherme"]))
print("Recuperando cliente a partir do Nome.")
for client in session.scalars(search_query_client):
    print(client.nome)

search_query_account = select(Account).where(Account.saldo > 2000)
print("Recuperando contas com saldo maior que R$ 2000.00")
for account in session.scalars(search_query_account):
    print(f'Client: {account.client} \n Balance: {account.saldo}')


join_query = select(Client, Account).join(Account).where(
    Client.id == Account.id_cliente,
    Account.tipo == "Conta Corrente"
)

print("Recuperando Conta Corrente para cada Cliente:")
for client, account in session.execute(join_query):
    print(f"Cliente: {client.nome} | Conta Corrente: {account.numero} | Saldo: {account.saldo}")
