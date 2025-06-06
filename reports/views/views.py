from django.shortcuts import render, redirect
from reports.forms import ReportUploadForm
from reports.models import Report
from reports.services.parser import pdf_to_json
from utils.s3 import upload_pdf_to_s3


def report_upload_view(request):
    if request.method == 'POST':
        form = ReportUploadForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user

            uploaded_file = request.FILES['pdf_file']

            # 1. S3 업로드
            s3_url = upload_pdf_to_s3(uploaded_file, request.user.id)
            report.file_url = s3_url

            # 2. PDF 파싱 (tempfile로 로컬 임시 저장)
            uploaded_file.seek(0)
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                for chunk in uploaded_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            report.parse_json = pdf_to_json(tmp_path)
            report.save()

            return redirect('analysis:report_detail', report_id=report.id)  # 분석 페이지 연결
    else:
        form = ReportUploadForm()
    return render(request, 'reports/upload.html', {'form': form})
