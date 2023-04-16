"""
Primeiro programa de interação com banco de dados utilozando SQL utilizando SQLAlchemy e modelo ORM
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()

class User(Base):
    """
    Esta classe representa a tabela user_account dentro do SQlite.
    """

    __tablename__ = "user_account"

    #Atributos
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"

        class Address(Base):
            __tablename__ = "address"
            id = Column(Integer, primary_key=True)
            email_address = Column(String(30), nullable=False)
            user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
            user = relationship("User", back_populates="address")

            def __repr__(self):
                return f"Address(id={self.id}, email_address={self.email_address})"

                print(User.__tablename__)
                print(Address.__tablename__)

                #Conexão com o banco de dados
                engine = create_engine("sqlite://")

                #Criando as classes como tabela no Banco de Dados
                Base.metadata.create_all(engine)

                #Depreciando - Será removido em futuro release
                print(engine.table_names())

                #Investiga o esquema de banco de dados
                inspetor_engine = inspect(engine)
                print(inspetor_engine.has_table("user_account"))
                print(inspetor_engine.get_table_names())
                print(inspetor_engine.default_schema_name)

                with Session(engine) as session:
                    dayane = User(
                        name='dayane',
                        fullname='Dayane Ferreira',
                        address=[Address(email_address='dayanesilvaf@outlook.com.br')]
                    )

                    christopher = User(
                        name='christopher',
                        fullname='Christopher Chevalier',
                        address=[Address(email_address='christopherchevalier03@gmail.com'),
                        Address
                        (email_address='christopherchevalier03@gmail.com')]
                    )

                    finn = User(name='finn', fullname='Finn Gutierrez')

                    #Enviado para o BD (persitência de dados)
                    session.add_all([dayane, christopher, finn])

                    session.commit()

                    stmt = select(User).where(User.name.in_(["dayane", 'christopher']))
                    print('Recuperando usuários a partir de condição de filtragem')
                    for user in session.scalars(stmt):
                        print(user)

                        stmt_address = select(Address).where(Address.user_id.in_([2]))
                        print('\nRecuperando os endereços de email de Christopher')
                        for address in session.scalars(stmt_address):
                            print(address)

                            stmt_order = select(User).order_by(User.fullname.desc())
                            print("\nRecuperando info de maneira ordenada")
                            for result in session.scalars(stmt_order):
                                print(result)

                                stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
                                print("\n")
                                for result in session.scalars(stmt_join):
                                    print(result)

                                    print(select(User.fullname, Address.email_address).join_from(Address, User))

                                    connection = engine.connect()
                                    results = connection.execute(stmt_join).fetchall()
                                    print("\nExecutando statement a partir da connection")
                                    for result in results:
                                        print(result)

                                        stmt_count = select(func.count('*')).select_from(User)
                                        print('\nTotal de instâncias em User')
                                        for result in session.scalars(stmt_count):
                                            print(result)

                                            #Encerrando de fato a session
                                            session.close()