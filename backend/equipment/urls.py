from django.urls import path
from .views import CSVUploadView, SummaryListView, GeneratePDFView, auth_check

urlpatterns = [
    path("upload-csv/", CSVUploadView.as_view(), name="upload_csv"),
    path("history/", SummaryListView.as_view(), name="history"),
    path("report/<int:pk>/", GeneratePDFView.as_view(), name="generate_pdf"),
    path("auth-check/", auth_check, name="auth_check"),  # ⭐ REQUIRED for desktop login
]
