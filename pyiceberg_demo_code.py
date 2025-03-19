from pyiceberg.catalog import load_catalog
from datetime import date, datetime, timezone
import uuid
import pyarrow as pa
from pyiceberg.io.pyarrow import pyarrow_to_schema
from pyiceberg.schema import Schema
from pyiceberg.types import NestedField, StringType, IntegerType, BooleanType, DateType, DecimalType, LongType
from pyiceberg.partitioning import PartitionSpec, PartitionField
from pyiceberg.transforms import IdentityTransform, YearTransform
import time

arrow_schema = pa.schema(
    [
        ("name", pa.string()),
        ("id", pa.int32()),
        ("date", pa.date32()),
    ]
)

data = [
    {"name": "Alice", "id": 1, "date": 17623},  # 2018-05-15
    {"name": "Bob", "id": 2, "date": 18512},    # 2020-11-23
    {"name": "Charlie", "id": 3, "date": 19174} # 2022-07-07
]

arrow_table = pa.Table.from_pylist(data, schema=arrow_schema)

demo_catalog = load_catalog(
    name="rest",
    **{
        "type": "rest",
        "uri": "http://localhost:8181/api/catalog",
        "warehouse": "polaris",
        "credential": "root:s3cr3t",
        "scope": "PRINCIPAL_ROLE:ALL"
    },
)


# iceberg_schema = Schema(
#         NestedField(field_id=1, name="name", field_type=StringType(), required=True),
#         NestedField(field_id=2, name="id", field_type=IntegerType(), required=True),
#         NestedField(field_id=3, name="date", field_type=DateType(), required=True),
#         schema_id=1,
#         identifier_field_ids=[],
#     )

print(arrow_table)

demo_catalog.create_namespace_if_not_exists("demo_ns")

print(demo_catalog.list_namespaces("demo_ns"))

if demo_catalog.table_exists("demo_ns.demo_table_1"):
    demo_catalog.drop_table("demo_ns.demo_table_1")

demo_catalog.create_table("demo_ns.demo_table_1", schema=arrow_schema)

print(demo_catalog.list_tables("demo_ns"))

table = demo_catalog.load_table("demo_ns.demo_table_1")

# table.update_spec().add_field("date", YearTransform()).commit()

with table.update_spec() as update:
    update.add_field("date", YearTransform())

table.append(arrow_table)

print(table.scan().to_pandas())


# Read as arrow table
print(table.scan().to_arrow())

print(table.scan(row_filter="name = 'Alice' OR date = '2022-07-01'").to_pandas())

with table.update_schema() as update:
    # Add new columns
    update.add_column("comments", StringType())
    update.add_column("salary", DecimalType(9, 3))
    
    # Rename an existing column
    update.rename_column("id", "employee_id")

    # Delete an existing column
    # update.delete_column("name")

print(table.schema())

table = demo_catalog.load_table("demo_ns.demo_table_1")
    
with table.update_schema() as update:    
    update.delete_column("comments")

    update.delete_column("salary")

    update.rename_column("employee_id", "id")

    
# with table.update_spec() as update:
#     # Add a partition field with identity transform
#     update.add_identity("employee_id")

# with table.update_spec() as update:
#     # Rename an existing partition field
#     update.rename_field("employee_id", "test_field")

# with table.update_spec() as update:
#     # Remove an existing partition field
#     update.remove_field("test_field")


print(table.spec())

print(table.schema())

print(table.snapshots())

previous_timestamp = int(time.time()*1000)

table.append(arrow_table)

# 2024-01-27 15:30:45
previous_snapshot = table.snapshot_as_of_timestamp(previous_timestamp, inclusive=True)

# only returns data in arrow_table_1
print(table.scan(snapshot_id=previous_snapshot.snapshot_id).to_pandas())

# returns data in both arrow_table_1 and
print(table.scan().to_pandas())


with table.transaction() as txn:
    # update schema
    with txn.update_schema() as update:
        update.add_column("comments", StringType())
        update.add_column("salary", DecimalType(9, 3))

    # update spec
    with txn.updaet_spec() as update:
        update.add_identity("employee_id")

    txn.overwrite(arrow_table)

    txn.set_properties({"key": "value"})

table.scan(selected_fields=["name", "date"], limit=10).to_arrow()



# with rest_catalog.create_table_transaction("tpch.test2", schema=arrow_schema) as txn:
#     txn.append(arrow_table)

# table = rest_catalog.create_table("tpch.test3", schema=arrow_schema)

# table = rest_catalog.load_table("tpch.test3")
# table.append(arrow_table)
# print(table.scan().to_arrow())