import sys
import requests

fhir_server_url = "http://localhost:8080/fhir"


def read_dicom_file(file_path: str):
    with open(file_path, "rb") as f:
        return f.read()


def request_fhir_server(path: str, method: str, data=None):
    headers = {"Content-Type": "application/dicom"}
    response = requests.request(method, fhir_server_url + path, headers=headers, data=data)
    if response.status_code == 201:
        print("DICOMデータがFHIRサーバーに保存されました。")
    else:
        print("エラーが発生しました:", response.status_code)
        print(response.text)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <DICOM file path>")
        sys.exit(1)

    dicom_file_path = sys.argv[1]
    dicom_data = read_dicom_file(dicom_file_path)
    request_fhir_server("/Binary", "POST", data=dicom_data)
