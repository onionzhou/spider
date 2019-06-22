import requests
import json

headers = {"Content-Type": "application/x-www-form-urlencoded"}



def post_data():
    data='readme.txt'
    # data = {"cbody": "readmet.txt"}
    r = requests.post("http://192.168.1.19", data=json.dumps(data))
    print(data)
    print(r.status_code)
    print(r.text)

def post_files():
    files = {'11.zip': open('12.zip', 'rb')}
    r =requests.post("http://192.168.1.19",headers=headers,files=files)
    print(r.status_code)
    print(r.text)
    print(r.raw)

def post_file_stream():
    with open("12.zip","rb") as f :
        r =requests.post("http://192.168.1.19",headers=headers,data=f)
    print(r.text)

def open_file_test():
    with open("12.zip","rb") as f:
        print(f.read())

def main():
    post_files()
    # open_file_test()
    # post_data()
    post_file_stream()


if __name__ == '__main__':
    main()