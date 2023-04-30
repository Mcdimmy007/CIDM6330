from sqlalchemy import Table, MetaData, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import registry, relationship

from allocation.domain import model
<<<<<<< HEAD

# https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#imperative-mapping
# using SQLAlchemy 2.0-style imperative mapping
mapper_registry = registry()
=======
from sqlalchemy import Column, Date, ForeignKey, Integer, MetaData, String, Table, event
from sqlalchemy.orm import registry, relationship

logger = logging.getLogger(__name__)

mapper_registry = registry()

# metadata = MetaData()
>>>>>>> ab31b3ba1a1fb4bbdf5f126182980f97ca51702c

order_lines = Table(
    "order_lines",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
)

products = Table(
    "products",
    mapper_registry.metadata,
    Column("sku", String(255), primary_key=True),
    Column("version_number", Integer, nullable=False, server_default="0"),
)

batches = Table(
    "batches",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", ForeignKey("products.sku")),
    Column("_purchased_quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)

allocations = Table(
    "allocations",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)

<<<<<<< HEAD

def start_mappers():
=======
allocations_view = Table(
    "allocations_view",
    mapper_registry.metadata,
    Column("orderid", String(255)),
    Column("sku", String(255)),
    Column("batchref", String(255)),
)


def start_mappers():
    logger.info("Starting mappers")
>>>>>>> ab31b3ba1a1fb4bbdf5f126182980f97ca51702c
    lines_mapper = mapper_registry.map_imperatively(model.OrderLine, order_lines)
    batches_mapper = mapper_registry.map_imperatively(
        model.Batch,
        batches,
        properties={
            "_allocations": relationship(
                lines_mapper,
                secondary=allocations,
                collection_class=set,
            )
        },
    )
    mapper_registry.map_imperatively(
<<<<<<< HEAD
        model.Product, products, properties={"batches": relationship(batches_mapper)}
=======
        model.Product,
        products,
        properties={"batches": relationship(batches_mapper)},
>>>>>>> ab31b3ba1a1fb4bbdf5f126182980f97ca51702c
    )
