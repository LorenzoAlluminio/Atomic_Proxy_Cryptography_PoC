
# TODO increase number of bits
keys=generate_keys(32,32)

c = []
for i in range(1,5):
    c.append(round(i,keys))

keys2=generate_keys(32,32)
proxy_key = generate_proxy_key(keys['privateKey'].x, keys2['privateKey'].x, keys2['privateKey'].p)

