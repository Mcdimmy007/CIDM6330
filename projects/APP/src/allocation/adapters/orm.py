from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry  # type: ignore
from sqlalchemy.orm import relationship
from allocation.domain.model import OrderLine, Batch, Product

metadata_fm = MetaData()
mapper_registry = registry(metadata_fm)

batches_table = Table(
    "batches",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("reference", String(50)),
    Column("sku", String(50), ForeignKey("products.sku")),
    Column("available_quantity", Integer),
)

order_lines_table = Table(
    "order_lines",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("order_reference", String(50)),
    Column("sku", String(50)),
    Column("quantity", Integer),
)

allocation_table = Table(
    "allocations",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("batch_id", Integer, ForeignKey("batches.id")),
    Column("order_line_id", Integer, ForeignKey("order_lines.id")),
)

product_table = Table(
    "products", mapper_registry.metadata, Column("sku", String, primary_key=True)
)


def map_allocation():
    mapper_registry.map_imperatively(OrderLine, order_lines_table)
    mapper_registry.map_imperatively(
        Batch,
        batches_table,
        properties={
            "_allocated_order_lines": relationship(
                OrderLine,
                secondary=allocation_table,
                collection_class=set,
            )
        },
    )
    mapper_registry.map_imperatively(
        Product, product_table, properties={"batches": relationship(Batch)}
    )


map_allocation()
