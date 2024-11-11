# cloudPDI

日本IHE協会のクラウド型情報交換技術仕様(cloudPDI)について調べる。
https://www.ihe-j.org/file2/docs/IHE-J-cloudPDI-ver2.0n.pdf


## 簡易構成の概要

- FHIR Server（リポジトリの役割）：患者情報や画像メタデータなど医療データの管理を行う中央リポジトリとして機能
    - 使用ツール：[HAPI FHIR](https://hapifhir.io/)（オープンソースのFHIRサーバー）
- DICOMweb Server（画像リポジトリの役割）：DICOM画像データそのものを保存し、管理する中央リポジトリとして機能
    - 使用ツール：[Orthanc](https://www.orthanc-server.com/)（オープンソースのDICOMサーバー）
- Sender：医療データを作成し、FHIRサーバーおよびDICOMwebサーバーに送信するクライアント
- Recipient：FHIRサーバーおよびDICOMwebサーバーから必要なデータを取得するクライアント
- Authorization Server：今回はシンプルなセットアップのため省略しますが、OAuth2などの仕組みでアクセス制御を実装することが可能

### 動作方法

1. Ryeのインストール:
    ```sh
    curl -sSf https://rye.astral.sh/get | bash
    ```
1. 環境のセットアップ:
    ```sh
    rye sync
    docker compose up -d
    ```
1. SenderでDICOM画像をリポジトリに送信
    ```sh
    rye run python sender/main.py <DICOMファイルのパス>
1. Recipientで情報を取得
    ```sh
    rye run python recipient/main.py <Study ID>
    ```

## 各コンポーネントのアクセス方法

- Orthanc
    - 通常: http://localhost:8042
    - OHIF Viewer: http://localhost:8042/ohif
- HAPI FHIR
    - HAPI FHIR Doc: http://localhost:8080

