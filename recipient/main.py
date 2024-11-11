import requests
import sys
import os

fhir_server_url = "http://localhost:8080/fhir"
dicom_server_url = "http://localhost:8042/instances"


def get_imaging_study(study_id: str):
    response = requests.get(f"{fhir_server_url}/ImagingStudy/{study_id}")
    if response.status_code == 200:
        print("ImagingStudyメタデータを取得しました。")
        return response.json()
    else:
        print("エラーが発生しました(FHIRサーバー):", response.status_code)
        print(response.text)
        return None


def download_dicom_instance(dicom_id, save_path):
    response = requests.get(f"{dicom_server_url}/{dicom_id}/file", stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(
            f"DICOMインスタンス {dicom_id} をダウンロードしました。保存先: {save_path}"
        )
    else:
        print("エラーが発生しました(DICOMサーバー):", response.status_code)
        print(response.text)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python recipient.py <Study ID>")
        sys.exit(1)

    study_id = sys.argv[1]

    imaging_study = get_imaging_study(study_id)

    if imaging_study:
        series = imaging_study.get("series", [])
        for serie in series:
            instances = serie.get("instance", [])
            for instance in instances:
                dicom_id = instance.get("uid")
                if dicom_id:
                    save_path = os.path.join("downloads", f"{dicom_id}.dcm")
                    os.makedirs("downloads", exist_ok=True)
                    download_dicom_instance(dicom_id, save_path)
