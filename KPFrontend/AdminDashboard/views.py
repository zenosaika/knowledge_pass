from django.shortcuts import render

def admin_dashboard(req):
    return render(req, 'AdminDashboard/new_admin_dashboard.html.html')