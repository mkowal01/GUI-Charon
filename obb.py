import pickle

def new_buffer(buffer):
    print("OOB Data:", buffer)

# Obiekt do zapisania
data = {"name": "JakubT", "age": 23}

# Serializacja z funkcją buffer_callback
with open("out_of_band_data.pkl", "wb") as file:
    # Zapisujemy dane do pliku z buffer_callback
    pickle.dump(data, file, protocol=5, buffer_callback=new_buffer())
with open("out_of_band_data.pkl", "rb") as file:
    data = pickle.load(file)
print(data)