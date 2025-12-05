import os
from typing import Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Sadece dosya oluşturma/yazma için gereken scope
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def _get_drive_service():
    """Google Drive servisini döndürür, yoksa OAuth akışını başlatır."""
    creds: Optional[Credentials] = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # Token yok ya da geçersiz ise yeniden login ol
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                raise RuntimeError(
                    "credentials.json bulunamadı. "
                    "Google Cloud Console üzerinden indirip proje dizinine koymalısın."
                )
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Token'ı kaydet
        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    service = build("drive", "v3", credentials=creds)
    return service


def upload_to_drive(file_path: str, mime_type: str = "application/vnd.openxmlformats-officedocument.wordprocessingml.document") -> str:
    """
    Verilen dosyayı Google Drive'a yükler.
    Drive'da oluşturulan dosyanın id'sini döner.
    """
    service = _get_drive_service()

    file_metadata = {
        "name": os.path.basename(file_path),
    }

    media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

    uploaded = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id, webViewLink")
        .execute()
    )

    file_id = uploaded.get("id")
    link = uploaded.get("webViewLink")
    return link or f"https://drive.google.com/file/d/{file_id}/view"
