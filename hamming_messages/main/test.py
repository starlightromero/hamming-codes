from reedsolo import RSCodec

message = "This is a message."
length = len(message)
rsc = RSCodec(length)
b = bytearray()
b.extend(map(ord, message))
b_arr = rsc.encode(b)
arr = b_arr[0:length]
arr_encoding = b_arr[length:]
distored_arr = bytearray()
count = 0
for a in arr_encoding:
    if count % 3 == 0:
        a = 88
    distored_arr.append(a)
    count += 1
# distored_message = distored_arr.decode("utf-8")
# distored_arr.extend(arr_encoding)
print(distored_arr)
# print(distored_message)
new_rsc = RSCodec(12)
new_b = bytearray()
new_b.extend(map(ord, "X"))
new_arr = new_rsc.encode(new_b)
print(new_arr)
