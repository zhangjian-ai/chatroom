from fdfs_client.client import Fdfs_client, get_tracker_conf


# 上传图片
path = get_tracker_conf('/Users/zhangjian/PycharmProjects/chatroom/backend/backend/utils/fastdfs/client.conf')
client = Fdfs_client(path)

# ret = client.upload_by_filename('/Users/zhangjian/Documents/icon/32321.jpeg')
# print(ret)

if __name__ == '__main__':
    file_id = "group1/M00/00/00/CgAQCWGyDtGAf8BwAAFgICuF1q414.jpeg".encode()
    result = client.delete(file_id)
    print(result)

    # content = client.download_to_buffer(file_id.encode())
    #
    # print(content)

    # string = "123 345 567"
    # print(list(string))
