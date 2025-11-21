# backend/equipment/views.py
import io
import pandas as pd
import magic
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.files.base import ContentFile
from .models import Upload
from .serializers import UploadSerializer
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class CSVUploadView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        file_obj = request.FILES.get("file")
        if not file_obj:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        file_bytes = file_obj.read()
        # optional mime check; if python-magic is not available, skip this block
        try:
            mime = magic.from_buffer(file_bytes, mime=True)
            if "csv" not in mime and "text" not in mime:
                return JsonResponse({"error": "Uploaded file is not a CSV"}, status=400)
        except Exception:
            pass

        upload = Upload()
        upload.original_filename = file_obj.name
        upload.csv_file.save(file_obj.name, ContentFile(file_bytes))

        # parse CSV with pandas
        df = pd.read_csv(io.BytesIO(file_bytes))

        expected_cols = ["Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"]
        missing = [c for c in expected_cols if c not in df.columns]
        if missing:
            upload.delete()
            return JsonResponse({"error": f"Missing columns: {missing}"}, status=400)

        total_count = len(df)
        averages = df[["Flowrate", "Pressure", "Temperature"]].apply(pd.to_numeric, errors="coerce").mean().to_dict()
        type_distribution = df["Type"].value_counts().to_dict()

        summary = {
            "total_count": int(total_count),
            "averages": {k: (float(round(v, 4)) if pd.notna(v) else None) for k, v in averages.items()},
            "type_distribution": {str(k): int(v) for k, v in type_distribution.items()},
        }

        upload.summary_json = summary
        upload.save()

        # keep last 5 uploads
        uploads = Upload.objects.order_by("-uploaded_at")
        for old in uploads[5:]:
            try:
                old.csv_file.delete(save=False)
            except Exception:
                pass
            old.delete()

        return JsonResponse({"upload": UploadSerializer(upload).data}, status=201)

class SummaryListView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        uploads = Upload.objects.order_by("-uploaded_at")[:5]
        data = [UploadSerializer(u).data for u in uploads]
        return JsonResponse({"history": data})

class GeneratePDFView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        try:
            upload = Upload.objects.get(pk=pk)
        except Upload.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setFont("Helvetica", 12)
        p.drawString(50, 750, f"Report for: {upload.original_filename}")
        p.drawString(50, 730, f"Uploaded at: {upload.uploaded_at}")

        y = 700
        summary = upload.summary_json or {}
        p.drawString(50, y, f"Total Count: {summary.get('total_count')}")
        y -= 20
        p.drawString(50, y, "Averages:")
        y -= 20
        for k, v in (summary.get("averages") or {}).items():
            p.drawString(70, y, f"{k}: {v}")
            y -= 18

        y -= 10
        p.drawString(50, y, "Type distribution:")
        y -= 20
        for k, v in (summary.get("type_distribution") or {}).items():
            p.drawString(70, y, f"{k}: {v}")
            y -= 18

        p.showPage()
        p.save()
        buffer.seek(0)
        return HttpResponse(buffer, content_type="application/pdf")


@csrf_exempt
def auth_check(request):
    """Authenticate desktop app using basic auth"""
    auth_header = request.META.get("HTTP_AUTHORIZATION")

    if not auth_header:
        return JsonResponse({"authenticated": False}, status=401)

    try:
        method, encoded = auth_header.split()
        import base64
        username, password = base64.b64decode(encoded).decode().split(":")
    except:
        return JsonResponse({"authenticated": False}, status=401)

    user = authenticate(username=username, password=password)

    if user is not None:
        return JsonResponse({"authenticated": True})
    else:
        return JsonResponse({"authenticated": False}, status=401)
