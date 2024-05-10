# Đọc hình ảnh bằng chế độ nhị phân ('rb')
with open("image.jpg", "rb") as image_file:
    # Đọc nội dung của hình ảnh
    image_data = image_file.read()

# Lưu dữ liệu ảnh dưới dạng văn bản vào một tệp text
with open("image_data.txt", "w") as text_file:
    # Chuyển dữ liệu của ảnh thành dạng văn bản bằng phương pháp base64
    import base64
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    text_file.write(image_base64)

# Đọc lại dữ liệu từ tệp text
with open("image_data.txt", "r") as text_file:
    # Đọc dữ liệu ảnh từ tệp văn bản và chuyển nó trở lại thành dạng nhị phân
    image_base64 = text_file.read()
    image_data = base64.b64decode(image_base64)

# Lưu lại dữ liệu ảnh dưới dạng nhị phân ('rb')
with open("image_new.jpg", "wb") as image_new_file:
    image_new_file.write(image_data)
