from typing import Optional
from datetime import date
from allocation.domain import model
from allocation.service_layer.unit_of_work import AbstractUnitOfWork


def allocate(order_line: model.OrderLine, uow: AbstractUnitOfWork):
    with uow:
        product = uow.products.get(order_line.sku)
        print(product.batches)
        allocated_ref = product.allocate(order_line)
        uow.commit()
    return allocated_ref


def add_batch(
    uow: AbstractUnitOfWork,
    reference: str,
    sku: str,
    available_quantity: int,
    eta: Optional[date] = None,
) -> None:
    with uow:
        product = uow.products.get(sku)
        if product is None:
            product = model.Product(sku, [])
            uow.products.add(product)
            print("new product")
        product.batches.append(
            model.Batch(
                reference=reference,
                sku=sku,
                available_quantity=available_quantity,
                eta=eta,
            )
        )
        uow.commit()

