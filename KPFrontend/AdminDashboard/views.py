from django.shortcuts import render

def admin_dashboard(req):
    return render(req, 'AdminDashboard/admin_dashboard.html')