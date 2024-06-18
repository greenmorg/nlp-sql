from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.automap import automap_base

def fetch_full_schema(connection_string: str) -> str:
    engine = create_engine(connection_string)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    inspector = inspect(engine)

    result_string_list = []
    for table_name in inspector.get_table_names():
        result_string_list.append(f"table {table_name}")
        # Print columns in the table
        for column in inspector.get_columns(table_name):
            result_string_list.append(f"\t{column['name']} - {column['type']}")
        # Print foreign keys
            fks = inspector.get_foreign_keys(table_name)
        for fk in fks:
            result_string_list.append(f"\t{fk['constrained_columns']} references {fk['referred_table']}({fk['referred_columns']})")
    return "\n".join(result_string_list)


