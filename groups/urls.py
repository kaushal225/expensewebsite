from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns=[
    path('create_group',views.create_group,name="create_group"),
    path('groups',views.list_groups,name='list_groups'),
    path('add_member/<str:group>',csrf_exempt(views.add_member),name='add_member'),
    path('edit_group/<str:group>',views.edit_group,name='edit_group'),
    path('member_list',csrf_exempt(views.member_list),name='member-list'),
    path('group_details/<str:group>',views.group_details,name='group_details'),
    path('individual_details/<str:group>/<int:pk>',views.group_individual_detail,name='group_individual_details'),
    path('add_individual_expense/<str:group>/<int:pk>',views.add_group_individual_expense,name='add_group_individual_expense'),
    path('join_group',csrf_exempt(views.join_group), name='join_group'),
    path('join_request',csrf_exempt(views.join_request),name='join_request'),
    path('accept_request_user/<str:group>',views.accept_request_user,name='accept_request_user'),
    path('deny_request_user/<str:group>',views.deny_request_user,name='deny_request_user'),
    path('list_admins',views.list_admins,name='list_admins'),
    path('change_admin_status/<str:user>/<str:group>',views.change_admin_status,name='change_admin_status'),
    path('list_requests/<str:group>',views.list_requests,name='list_requests'),
    path('accept_request_group/<str:group>/<str:user>',views.accept_request_group,name='accept_request_group'),
    path('deny_request_group/<str:group>/<str:user>',views.deny_request_group,name='deny_request_group'),
    path('group_currency_list/<str:group>',views.change_currency,name='group_currency_list'),
    path('remove_user/<str:user>/<str:group>',views.remove_user,name='remove_user'),
    path('group_summary_admin/<str:group>',views.group_summary_admin,name='group_summary_admin'),
    path('group_summary_individual',views.group_summary_individual,name="group_summary_individual"),
    path('group_stat_admin/<str:group>',csrf_exempt(views.group_stat_admin),name='group_stat_admin'),
    path('group_stat_individual',csrf_exempt(views.group_stat_individual),name='group_stat_individual'),
    path('modify_currency/<str:group>',views.currency_modify,name='group_currency_modify'),
    path('exit_group/<str:group>/<str:user>',views.exit_group,name='exit_group'),
    path('list_notification',csrf_exempt(views.get_notification),name='list_notification'),
    path('delete_notification/<int:id>',views.delete_notifications,name='delete_notification'),
    path('edit_group_expense/<int:id>',views.edit_group_expense,name='edit_group_expense'),
    path('delete_individual_expense/<int:id>',views.delete_individual_expense,name='delete_individual_expense')
    
]