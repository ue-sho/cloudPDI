import sys
import requests

fhir_server_url = "http://localhost:8080/fhir"
dicom_server_url = "http://localhost:8042/instances"


def read_dicom_file(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()


def send_to_dicom_server(data: bytes) -> str | None:
    headers = {"Content-Type": "application/dicom"}
    response = requests.post(dicom_server_url, headers=headers, data=data)
    if response.status_code == 200:
        print("DICOMデータがOrthancサーバーに保存されました。")
        dicom_id = response.json()["ID"]
        print("DICOM ID:", dicom_id)
        return dicom_id
    else:
        print("エラーが発生しました(Orthancサーバー):", response.status_code)
        print(response.text)
        return None


def send_to_fhir_server(dicom_id: str):
    imaging_study_data = {
        "resourceType": "ImagingStudy",
        "status": "available",
        "description": "Uploaded DICOM study",
        "series": [
            {
                "uid": dicom_id,
                "instance": [
                    {
                        "uid": dicom_id,
                        "url": f"{dicom_server_url}/{dicom_id}",
                    }
                ],
            }
        ],
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(
        f"{fhir_server_url}/ImagingStudy", headers=headers, json=imaging_study_data
    )
    if response.status_code == 201:
        print("ImagingStudyがFHIRサーバーに保存されました。")
    else:
        print("エラーが発生しました(FHIRサーバー):", response.status_code)
        print(response.text)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <DICOM file path>")
        sys.exit(1)

    dicom_file_path = sys.argv[1]
    dicom_data = read_dicom_file(dicom_file_path)

    dicom_id = send_to_dicom_server(dicom_data)

    if dicom_id:
        send_to_fhir_server(dicom_id)
