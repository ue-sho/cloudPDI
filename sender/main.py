import os
from pathlib import Path
import sys
import requests

fhir_server_url = "http://localhost:8080/fhir"
dicom_server_url = "http://localhost:8042/instances"


EXTENSIONS_TO_IGNORE = [
    ".bat",
    ".bpl",
    ".bmp",
    ".cfg",
    ".cmd",
    ".css",
    ".dat",
    ".db",
    ".dtd",
    ".dll",
    ".exe",
    ".gif",
    ".htm",
    ".html",
    ".ico",
    ".idx",
    ".inf",
    ".ini",
    ".jpe",
    ".jpeg",
    ".jpg",
    ".js",
    ".lut",
    ".pdf",
    ".png",
    ".thu",
    ".txt",
    ".xml",
]


def is_potential_dicom_file(file: Path) -> bool:
    return (
        file.is_file()
        and not file.name.startswith(".")
        and file.name != "DICOMDIR"
        and file.suffix.lower() not in EXTENSIONS_TO_IGNORE
    )


def read_dicom_files(file_folder: str):
    for root, _, files in os.walk(file_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if not is_potential_dicom_file(Path(file_path)):
                continue

            with open(file_path, "rb") as f:
                yield f.read()


def send_to_dicom_server(data: bytes) -> str | None:
    headers = {"Content-Type": "application/dicom"}
    response = requests.post(dicom_server_url, headers=headers, data=data)
    if response.status_code == 200:
        dicom_id = response.json()["ID"]
        print("DICOMデータがOrthancサーバーに保存されました。DICOM ID:", dicom_id)
        return dicom_id
    else:
        print("エラーが発生しました(Orthancサーバー):", response.status_code)
        print(response.text)
        return None


def send_to_fhir_server(dicom_id: str) -> str | None:
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
        imaging_study_id = response.json()["id"]
        print(
            "ImagingStudyがFHIRサーバーに保存されました。ImagingStudy ID:",
            imaging_study_id,
        )
        return imaging_study_id
    else:
        print("エラーが発生しました(FHIRサーバー):", response.status_code)
        print(response.text)
        return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <DICOM file path>")
        sys.exit(1)

    dicom_folder = sys.argv[1]

    for dicom_data in read_dicom_files(dicom_folder):
        dicom_id = send_to_dicom_server(dicom_data)
        if dicom_id:
            send_to_fhir_server(dicom_id)
