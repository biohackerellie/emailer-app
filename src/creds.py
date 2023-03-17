
####Convert client secret to encoded binary. I ended up not using it in the release code, but it could be useful for some

import base64

with open('client_secret.json', 'rb') as f:
    binary_data = f.read()

encoded_data = base64.b64encode(binary_data).decode('utf-8')




CLIENT_SECRET_DATA = f'''
{encoded_data}
'''

print(CLIENT_SECRET_DATA)


