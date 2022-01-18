# Learn FastAPI

### command to run the app

`uvicorn app.main:app --reload`


### pydantic

<https://pydantic-docs.helpmanual.io/#rationale>

pydantic is primarily a parsing library, not a validation library. Validation is a means to an end: building a model which conforms to the types and constraints provided.
In other words, pydantic guarantees the types and constraints of the output model, not the input data.
This might sound like an esoteric distinction, but it is not. If you're unsure what this means or how it might affect your usage you should read the section about Data Conversion below.
Although validation is not the main purpose of pydantic, you can use this library for custom validation.

### psycopyg
Driver to talk to the database server and perform SQL queries on that.

### Object Relational Mapper

--> Performing the database operations using the traditional programming language and not the query language of the dbms.

### SQLAlchemy
<https://www.sqlalchemy.org/>

SQLAlchemy is most famous for its object-relational mapper (ORM), an optional component that provides the data mapper pattern, where classes can be mapped to the database in open ended, multiple ways - allowing the object model and database schema to develop in a cleanly decoupled way from the beginning.

### JWT token
The token contains the information which asserts if a client is authenticated or not.
It looks like a encrypted string but it is not encrypted.


### Alembic
Migration tool that works with SQLAlchemy. It reads our models and create the corresponding tables and column.

## Hosting
