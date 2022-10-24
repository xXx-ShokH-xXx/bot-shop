def create_tables(database, pars_oop):
    database.create_categories_table()
    database.create_products_table()

    database.insert_categories('phones')
    database.insert_categories('tv')
    database.insert_categories('air-conditioners')
    database.insert_categories('stiralniye-mashini')

    products_list = [pars_oop('phones').get_info(), pars_oop('tv').get_info(), pars_oop('air-conditioners').get_info(),
                     pars_oop('stiralniye-mashini').get_info()]

    for products in products_list:
        for product in products:
            product_name = product['title']
            product_link = product['link']
            product_price = product['price']
            product_image = product['image']
            category_id = product['category_id']

            database.insert_products(product_name, product_link, product_price, product_image, category_id)
