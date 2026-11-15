from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import mimetypes
from django.core.paginator import Paginator
from django.http import JsonResponse, FileResponse
from django.db.models import Avg, Q, F
from User.models import CustomUser
from .models import Document, Rate, Comment, Course, Faculty, Report
import hashlib

from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from User.decorators import role_required

from .forms import DocumentForm, ReportForm


def contact(request):
    """Trang liên hệ: hiển thị form và xử lý gửi tin nhắn."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not subject or not message:
            messages.error(
                request,
                'Please fill in all fields before sending.'
            )
        else:
            # Lưu nội dung vào messages để admin thấy được trên server
            # (dự án chưa cấu hình SMTP nên không gửi mail thật).
            full_message = (
                f'New contact message\n'
                f'-------------------\n'
                f'Name:    {name}\n'
                f'Email:   {email}\n'
                f'Subject: {subject}\n\n'
                f'{message}\n'
            )
            try:
                if getattr(settings, 'EMAIL_HOST', None):
                    send_mail(
                        subject=f'[AcademicShare Contact] {subject}',
                        message=full_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[getattr(settings, 'CONTACT_EMAIL', 'admin@acadshare.local')],
                        fail_silently=True,
                    )
            except Exception:
                pass

            messages.success(
                request,
                'Thank you! Your message has been sent. '
                'We will get back to you soon.'
            )
            return redirect('contact')

    return render(request, 'Blog/contact.html')


def document_list(request):
    documents = Document.objects.filter(
        status='approved'
    ).order_by('-id')

    paginator = Paginator(documents, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'Blog/index.html',
        {
            'documents': page_obj,
            'page_obj': page_obj,
            'paginator': paginator,
        }
    )


def document_detail(request, id):

    document = get_object_or_404(
        Document,
        id=id,
        status='approved'
    )

    avg_rate = Rate.objects.filter(
        document=document
    ).aggregate(
        Avg('rate')
    )

    avg = avg_rate['rate__avg']

    if avg is None:
        avg = 0
    else:
        avg = round(avg)

    user_rate = 0

    if request.user.is_authenticated:

        rate_obj = Rate.objects.filter(
            document=document,
            user=request.user
        ).first()

        if rate_obj:
            user_rate = rate_obj.rate

    comments = Comment.objects.filter(
        document=document,
        level=0
    ).order_by('-id')

    return render(
        request,
        'Blog/blog_detail.html',
        {
            'document': document,
            'avg': avg,
            'user_rate': user_rate,
            'comment': comments,
        }
    )


def search_view(request):
    keyword = request.GET.get('name', '').strip()
    faculty_id = request.GET.get('faculty')
    course_id = request.GET.get('course')
    doc_type = request.GET.get('doc_type')

    documents = Document.objects.filter(
        status='approved'
    )

    # Tìm theo từ khóa
    if keyword:
        documents = documents.filter(
            Q(title__icontains=keyword) |
            Q(description__icontains=keyword)
        )

    # Lọc theo Faculty
    if faculty_id:
        documents = documents.filter(
            faculty_id=faculty_id
        )

    # Lọc theo Course
    if course_id:
        documents = documents.filter(
            course_id=course_id
        )

    # Lọc theo Document Type
    if doc_type:
        documents = documents.filter(
            doc_type=doc_type
        )

    paginator = Paginator(documents, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'Blog/search.html',
        {
            'documents': page_obj,
            'page_obj': page_obj,
            'keyword': keyword,
            'faculties': Faculty.objects.all(),
            'courses': Course.objects.all(),
            'selected_faculty': faculty_id,
            'selected_course': course_id,
            'selected_doc_type': doc_type,
        }
    )

def save_rating(request):

    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Invalid request'
        })

    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'error': 'Vui long dang nhap'
        })

    document_id = request.POST.get('document_id')
    rate = request.POST.get('rate')

    try:
        document = Document.objects.get(
            id=document_id,
            status='approved'
        )

        old_rate = Rate.objects.filter(
            document=document,
            user=request.user
        ).first()

        if old_rate:
            old_rate.rate = int(rate)
            old_rate.save()

        else:
            Rate.objects.create(
                document=document,
                rate=int(rate),
                user=request.user
            )

        avg = Rate.objects.filter(
            document=document
        ).aggregate(
            Avg('rate')
        )

        return JsonResponse({
            'success': True,
            'avg': round(avg['rate__avg'], 1)
        })

    except Document.DoesNotExist:

        return JsonResponse({
            'success': False,
            'error': 'Document not found'
        })


def save_comment(request):

    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Invalid request'
        })

    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'error': 'Vui long dang nhap'
        })

    document_id = request.POST.get('document_id')
    comment = request.POST.get('comment')
    level = request.POST.get('level', 0)
    parent_id = request.POST.get('parent_id')

    if not level:
        level = 0

    document = get_object_or_404(
        Document,
        id=document_id,
        status='approved'
    )

    new_comment = Comment.objects.create(
        document=document,
        comment=comment,
        user=request.user,
        level=level,
        parent_id=parent_id if parent_id else None
    )

    return JsonResponse({
        'success': True,
        'data': {
            'id': new_comment.id,
            'comment': new_comment.comment,
            'author_name': request.user.username,
            'author_id': request.user.id,
            'level': new_comment.level,
            'parent_id': parent_id,
        }
    })
@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = request.FILES['file']

            # Tính SHA-256
            sha256 = hashlib.sha256()

            for chunk in uploaded_file.chunks():
                sha256.update(chunk)

            file_hash = sha256.hexdigest()

            # Kiểm tra file trùng
            if Document.objects.filter(file_hash=file_hash).exists():
                messages.error(
                    request,
                    'This document already exists.'
                )
                return render(
                    request,
                    'Blog/upload_document.html',
                    {'form': form}
                )

            document = form.save(commit=False)

            document.uploaded_by = request.user
            document.file_hash = file_hash
            document.status = 'pending'

            document.save()

            messages.success(
                request,
                'Document uploaded successfully and is waiting for approval.'
            )

            return redirect('document_list')

    else:
        form = DocumentForm()

    return render(
        request,
        'Blog/upload_document.html',
        {'form': form}
    )
def get_courses(request):
    faculty_id = request.GET.get('faculty_id')

    courses = Course.objects.filter(faculty_id=faculty_id).values('id', 'name')

    return JsonResponse(list(courses), safe=False)
@role_required('moderator', 'admin')
def pending_documents(request):

    documents = Document.objects.filter(status='pending').order_by('-created_at')

    return render(
        request,
        'Blog/pending_documents.html',
        {'documents': documents}
    )
@role_required('moderator', 'admin')
def approve_document(request, id):

    document = get_object_or_404(Document, id=id)

    document.status = 'approved'
    document.save()

    messages.success(request, 'Document approved successfully.')

    return redirect('pending_documents')
@role_required('moderator', 'admin')
def reject_document(request, id):

    document = get_object_or_404(Document, id=id)

    if request.method == 'POST':
        review_note = request.POST.get('review_note', '').strip()

        if not review_note:
            messages.error(request, 'Please provide a feedback note.')
            return render(
                request,
                'Blog/reject_document.html',
                {'document': document}
            )

        document.status = 'rejected'
        document.review_note = review_note
        document.save()

        messages.success(request, 'Document rejected successfully.')
        return redirect('pending_documents')

    return render(
        request,
        'Blog/reject_document.html',
        {'document': document}
    )
@role_required('student', 'moderator', 'admin')
def report_document(request, id):
    document = get_object_or_404(
        Document,
        id=id,
        status='approved'
    )

    if request.method == 'POST':
        form = ReportForm(request.POST)

        if form.is_valid():
            report = form.save(commit=False)
            report.document = document
            report.user = request.user
            report.save()

            messages.success(
                request,
                'Your report has been submitted successfully.'
            )

            return redirect(
                'document_detail',
                id=document.id
            )
    else:
        form = ReportForm()

    return render(
        request,
        'Blog/report_document.html',
        {
            'form': form,
            'document': document,
        }
    )
@role_required('moderator', 'admin')
def pending_reports(request):

    reports = Report.objects.filter(
        resolved=False
    ).order_by('-created_at')

    return render(
        request,
        'Blog/pending_reports.html',
        {
            'reports': reports
        }
    )
@role_required('moderator', 'admin')
def resolve_report(request, id):

    report = get_object_or_404(Report, id=id)

    report.resolved = True
    report.save()

    messages.success(
        request,
        'Report resolved successfully.'
    )

    return redirect('pending_reports')
@role_required('admin')
def user_management(request):

    users = CustomUser.objects.all().order_by('id')

    return render(
        request,
        'Blog/user_management.html',
        {
            'users': users
        }
    )
@role_required('admin')
def change_user_role(request, id):

    user = get_object_or_404(CustomUser, id=id)

    if user == request.user:
        messages.error(
            request,
            'You cannot change your own role.'
        )
        return redirect('user_management')

    if user.role == 'student':
        user.role = 'moderator'
    else:
        user.role = 'student'

    user.save()

    messages.success(
        request,
        'User role changed successfully.'
    )

    return redirect('user_management')
@login_required
def my_uploads(request):
    documents = Document.objects.filter(
        uploaded_by=request.user
    ).order_by('-created_at')

    return render(
        request,
        'Blog/my_uploads.html',
        {'documents': documents}
    )
@login_required
def download_document(request, id):
    document = get_object_or_404(
        Document,
        id=id,
        status='approved'
    )

    if not document.file:
        messages.error(request, 'File not found.')
        return redirect('document_detail', id=document.id)

    Document.objects.filter(id=document.id).update(
        download_count=F('download_count') + 1
    )

    document.refresh_from_db()

    return FileResponse(
        document.file.open('rb'),
        as_attachment=True,
        filename=document.file.name.split('/')[-1]
    )
def preview_document(request, id):
    document = get_object_or_404(
        Document,
        id=id,
        status='approved'
    )

    if not document.file:
        messages.error(request, 'File not found.')
        return redirect('document_detail', id=document.id)

    return FileResponse(
        document.file.open('rb'),
        as_attachment=False,
        content_type='application/pdf'
    )