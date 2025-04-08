from django.utils import timezone
from products.models import Product
from outflows.models import Outflow
from categories.models import Category
from brands.models import Brand
from django.utils.formats import number_format
from django.db.models import Sum, F


def get_product_metrics():
    products = Product.objects.all()
    total_quantity = sum(product.quantity for product in products)
    total_cost_price = sum(
        [product.cost_price * product.quantity for product in products]
    )
    total_selling_price = sum(
        [product.selling_price * product.quantity for product in products]
    )
    product_metrics = {
        "total_quantity": total_quantity,
        "total_cost_price": number_format(
            value=total_cost_price, decimal_pos=2, force_grouping=True
        ),
        "total_selling_price": number_format(
            value=total_selling_price, decimal_pos=2, force_grouping=True
        ),
        "total_profit": number_format(
            value=total_selling_price - total_cost_price,
            decimal_pos=2,
            force_grouping=True,
        ),
    }
    return product_metrics


def get_sales_metrics():
    outflows = Outflow.objects.all()
    total_sales = Outflow.objects.count()
    # total_sold_products = sum([outflow.quantity for outflow in outflows])
    total_sold_products = (
        Outflow.objects.aggregate(total_sum=Sum("quantity"))["total_sum"] or 0
    )
    total_sales_cost = sum(
        [outflow.quantity * outflow.product.cost_price for outflow in outflows]
    )
    total_sales_value = sum(
        [outflow.quantity * outflow.product.selling_price for outflow in outflows]
    )
    total_sales_profit = total_sales_value - total_sales_cost

    sales_metrics = {
        "total_sales": total_sales,
        "total_sold_products": total_sold_products,
        "total_sales_value": number_format(
            value=total_sales_value, decimal_pos=2, force_grouping=True
        ),
        "total_sales_profit": number_format(
            value=total_sales_profit, decimal_pos=2, force_grouping=True
        ),
    }
    return sales_metrics


def get_daily_sales_data():
    today = timezone.now().date()
    dates = [str(today - timezone.timedelta(days=i)) for i in range(6, -1, -1)]
    values = []

    for date in dates:
        total_sales = (
            Outflow.objects.filter(created_at__date=date).aggregate(
                total_sales=Sum(F("product__selling_price") * F("quantity"))
            )["total_sales"]
            or 0  # noqa: W503
        )

        values.append(float(total_sales))

    return {
        "dates": dates,
        "values": values,
    }


def get_daily_sales_quantity_data():
    today = timezone.now().date()
    dates = [str(today - timezone.timedelta(days=i)) for i in range(6, -1, -1)]
    quantities = []

    for date in dates:
        quantity_sales = Outflow.objects.filter(created_at__date=date).count()
        quantities.append(float(quantity_sales))

    return {
        "dates": dates,
        "quantities": quantities,
    }


def get_product_count_by_category():
    categories = Category.objects.all()
    build = {
        category.name: Product.objects.filter(category=category).count()
        for category in categories
    }
    return {"names": list(build.keys()), "quantities": list(build.values())}
    # return build


def get_product_count_by_brand():
    brands = Brand.objects.all()
    build = {
        brand.name: Product.objects.filter(brand=brand).count() for brand in brands
    }
    return {"names": list(build.keys()), "quantities": list(build.values())}
    # return build
