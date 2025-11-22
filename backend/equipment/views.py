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
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter


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

        summary = upload.summary_json or {}

        buffer = io.BytesIO()
        pdf = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            title="Chemical Equipment Report",
            leftMargin=40,
            rightMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()
        normal = styles["Normal"]

        title_style = ParagraphStyle(
            "title",
            parent=styles["Title"],
            fontSize=22,
            textColor=colors.HexColor("#2C3E50"),
            alignment=1,
            spaceAfter=20
        )

        header_style = ParagraphStyle(
            "header",
            parent=styles["Heading2"],
            fontSize=16,
            textColor=colors.HexColor("#34495E"),
            spaceAfter=10
        )

        elements = []

        # ---------------------------
        # Title
        # ---------------------------
        elements.append(Paragraph("📘 Chemical Equipment Summary Report", title_style))
        elements.append(Paragraph(f"File: <b>{upload.original_filename}</b>", normal))
        elements.append(Paragraph(f"Uploaded At: {upload.uploaded_at}", normal))
        elements.append(Spacer(1, 20))

        # ---------------------------
        # Summary Table
        # ---------------------------
        elements.append(Paragraph("Summary Overview", header_style))

        table_data = [
            ["Parameter", "Value"],
            ["Total Equipment", summary.get("total_count")],
            ["Average Flowrate", summary["averages"].get("Flowrate")],
            ["Average Pressure", summary["averages"].get("Pressure")],
            ["Average Temperature", summary["averages"].get("Temperature")],
        ]

        table = Table(table_data, colWidths=[200, 200])
        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F618D")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#EBF5FB")),
                ("BOX", (0, 0), (-1, -1), 1, colors.gray),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.gray),
            ])
        )

        elements.append(table)
        elements.append(Spacer(1, 25))

        # ---------------------------
        # PIE CHART (Type Distribution)
        # ---------------------------
        type_dist = summary["type_distribution"]

        if type_dist:
            pie_buffer = io.BytesIO()
            labels = list(type_dist.keys())
            values = list(type_dist.values())

            plt.figure(figsize=(5, 5))
            plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
            plt.title("Equipment Type Distribution")
            plt.tight_layout()
            plt.savefig(pie_buffer, format="png")
            plt.close()

            pie_buffer.seek(0)
            elements.append(Paragraph("Equipment Type Distribution", header_style))
            elements.append(Image(pie_buffer, width=350, height=350))
            elements.append(Spacer(1, 20))

        # ---------------------------
        # BAR CHART (Counts)
        # ---------------------------
        bar_buffer = io.BytesIO()
        plt.figure(figsize=(6, 4))
        plt.bar(labels, values)
        plt.title("Count by Equipment Type")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(bar_buffer, format="png")
        plt.close()

        bar_buffer.seek(0)
        elements.append(Paragraph("Equipment Count Chart", header_style))
        elements.append(Image(bar_buffer, width=400, height=300))
        elements.append(Spacer(1, 20))

        # ---------------------------
        # Build PDF
        # ---------------------------
        pdf.build(elements)
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
