import os

import urllib3
from minio import Minio, S3Error
from config.config import Config


class LoadData:
    def __init__(self, file_path, bucket_name):
        self.file_path = file_path
        self.bucket_name = bucket_name

    def load_data(self):
        file_path = self.file_path
        bucket_name = self.bucket_name

        url = Config.minio_server.url
        client = Minio(
            url,
            access_key=Config.minio_server.access_key,
            secret_key=Config.minio_server.secret_key,
            secure=False,
            http_client=urllib3.PoolManager(
                timeout=urllib3.Timeout.DEFAULT_TIMEOUT,
                retries=urllib3.Retry(
                    total=1,
                    backoff_factor=0.2,
                    status_forcelist=()
                )
            )
        )

        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)

        if isinstance(file_path, list):
            minio_file_path = []
            file_size = []
            for path in file_path:
                file_name = os.path.basename(path)
                try:
                    client.fput_object(bucket_name, file_name + ".txt", path)
                except S3Error as e:
                    print(f"{file_name} txt 파일 업로드 중 에러가 발생했습니다: {e}")
                try:
                    client.fput_object(bucket_name, file_name+".key", path + ".key")
                except S3Error as e:
                    print(f"{file_name} keyword 파일 업로드 중 에러가 발생했습니다: {e}")

                minio_path = "http://" + url + "/" + bucket_name + "/" + file_name + ".txt"
                size = os.path.getsize(path)

                minio_file_path.append(minio_path)
                file_size.append(size)
        else:
            file_name = os.path.basename(file_path)
            try:
                client.fput_object(bucket_name, file_name, file_path)
                print(f"'{file_name}' 파일이 '{bucket_name}' 버킷에 업로드되었습니다.")
            except S3Error as e:
                print(f"파일 업로드 중 에러가 발생했습니다: {e}")

            minio_file_path = "http://" + url + "/" + bucket_name + "/" + file_name
            file_size = os.path.getsize(file_path)
            return minio_file_path, file_size
        return minio_file_path, file_size, bucket_name
