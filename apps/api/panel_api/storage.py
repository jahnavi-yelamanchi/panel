from dataclasses import dataclass

import boto3

from panel_api.settings import get_settings


@dataclass(frozen=True)
class StoredObject:
    byte_size: int
    sha256: str


class AssetStorage:
    def __init__(self) -> None:
        settings = get_settings()
        self.bucket = settings.asset_bucket
        self.client = boto3.client("s3", region_name=settings.aws_region)

    def presigned_quarantine_upload(self, object_key: str, media_type: str) -> str:
        return self.client.generate_presigned_url(
            "put_object",
            Params={"Bucket": self.bucket, "Key": object_key, "ContentType": media_type},
            ExpiresIn=900,
        )

    def inspect(self, object_key: str) -> StoredObject:
        response = self.client.head_object(Bucket=self.bucket, Key=object_key)
        checksum = response.get("Metadata", {}).get("sha256")
        if not checksum:
            raise ValueError("uploaded object is missing sha256 metadata")
        return StoredObject(byte_size=response["ContentLength"], sha256=checksum)
