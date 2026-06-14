from products.models import Product


def get_related_products(product, limit=6):

    products = Product.objects.filter(is_public=True, supplier__is_public=True).exclude(
        id=product.id
    )

    scored_products = []

    for p in products:
        score = 0

        # same category
        if p.category_id == product.category_id:
            score += 3

        # same country
        if p.origin_country == product.origin_country:
            score += 2

        # same supplier
        if p.supplier_id == product.supplier_id:
            score += 1

        scored_products.append((score, p))

    # sort by score descending
    scored_products.sort(key=lambda x: x[0], reverse=True)

    # return only products
    return [p for score, p in scored_products][:limit]
