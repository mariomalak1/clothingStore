def put_sizes_in_to_options_in_select_widget_form(form):
    for i in form:
        print("#" * 50)
        print(i)
    return form

def get_id_of_product_from_option_widget(option_widget_str):
    product_code = ""
    for letter in option_widget_str:
        if letter == "-":
            break
        product_code += letter
    # print(product_code[:len(product_code) - 1])
    return product_code


# form.fields["size"].attrs = {"onclick": "changeMe()"}
# for select_field in form:
#     if select_field.label == "Product":
#         for option in select_field:
#             product_code = get_id_of_product_from_option_widget(option.data["label"])
#             product_detail = ProductDetail.objects.filter(product_code__icontains=product_code).first()
#             if product_detail:
#                 print(product_detail.name)
#                 all_sizes_of_product = product_detail.sizes.all()
#                 lis_of_sizes_of_product = []
#                 for size in all_sizes_of_product:
#                     lis_of_sizes_of_product.append(size.name)
#                 print(f"{product_detail.product_code} :", lis_of_sizes_of_product)
#             # get all sizes that in product details of this product
#             # put them in list
#             # put the list in attrs as key sizes
#             # option.data["attrs"]["sizes"] = ""
#             # print(option.data)
#
# # form = put_sizes_in_to_options_in_select_widget_form(form)
#
# # print(form.fields["size"].attrs)