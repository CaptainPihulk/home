import requests


# response = requests.post('http://127.0.0.1:5000/upscale', json={'input_path': 'lama_300px.png'})

# print(response.status_code)
# print(response.json())

response = requests.get('http://127.0.0.1:5000/tasks/55817069-ff4a-49d9-b396-9c711b49bf65gi')

print(response.status_code)
print(response.json())
