# cloudPDI

日本IHE協会のクラウド型情報交換技術仕様(cloudPDI)について調べる。
https://www.ihe-j.org/file2/docs/IHE-J-cloudPDI-ver2.0n.pdf


## 簡易構成の概要

- FHIRサーバー（Repositoryの役割）：FHIR APIで医療データを保存する中央リポジトリ
    - [HAPI FHIR](https://hapifhir.io/)を使用する
- Sender：医療データを作成してFHIRサーバーに送信するクライアント
- Recipient：FHIRサーバーからデータを取得するクライアント
- Authorization Server：今回はシンプルなセットアップのために省略する

