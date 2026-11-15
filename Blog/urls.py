from django.urls import path
from . import views


urlpatterns = [
    path(
        'list/',
        views.document_list,
        name='document_list'
    ),

    path(
        'contact/',
        views.contact,
        name='contact'
    ),

    path(
        'search/',
        views.search_view,
        name='search'
    ),

    path(
        'detail/<int:id>/',
        views.document_detail,
        name='document_detail'
    ),

    path(
        'rate/',
        views.save_rating,
        name='save_rating'
    ),

    path(
        'comment/',
        views.save_comment,
        name='save_comment'
    ),
    path('upload/', views.upload_document, name='upload_document'),
    path('get-courses/', views.get_courses, name='get_courses'),
    path('moderator/pending/', views.pending_documents, name='pending_documents'),
    path(
    'moderator/approve/<int:id>/',
    views.approve_document,
    name='approve_document'
),
path('moderator/reject/<int:id>/', views.reject_document, name='reject_document'),
path('report/<int:id>/', views.report_document, name='report_document'),
path('moderator/reports/', views.pending_reports, name='pending_reports'),
path(
    'moderator/reports/resolve/<int:id>/',
    views.resolve_report,
    name='resolve_report'
),
path(
    'admin/users/',
    views.user_management,
    name='user_management'
),
path(
    'admin/users/change-role/<int:id>/',
    views.change_user_role,
    name='change_user_role'
),
path('my-uploads/', views.my_uploads, name='my_uploads'),
path(
    'download/<int:id>/',
    views.download_document,
    name='download_document'
),
path('preview/<int:id>/', views.preview_document, name='preview_document'),
]