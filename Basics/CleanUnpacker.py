# creating a function named as process_log(data)

def process_log(data):
    timestamp, *payload, checksum = data


    return payload[::-1]


print(process_log([162506, "ERR", "AUTH", "RETRY", "0xFA21"]))