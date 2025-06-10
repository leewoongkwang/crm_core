from django.shortcuts import render, redirect
from report.forms import ReportUploadForm
from report.models import Report
from report.services.parser import pdf_to_json
from utils.s3 import upload_pdf_to_s3
from io import BytesIO

def report_upload_view(request):
    if request.method == 'POST':
        form = ReportUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['pdf_file']

            # ✅ PDF 내용을 메모리에 안전하게 복사
            original_bytes = uploaded_file.read()
            memory_file_for_s3 = BytesIO(original_bytes)
            memory_file_for_parser = BytesIO(original_bytes)

            # ✅ S3 업로드
            s3_url = upload_pdf_to_s3(memory_file_for_s3, request.user.id)

            # ✅ 파싱
            parsed_data = pdf_to_json(memory_file_for_parser)

            # ✅ 저장
            Report.objects.create(
                customer=form.cleaned_data['customer'],
                user=request.user,
                file_url=s3_url,
                parse_json=parsed_data
            )
            return redirect('report_upload')
    else:
        form = ReportUploadForm()
    return render(request, 'report/upload.html', {'form': form})