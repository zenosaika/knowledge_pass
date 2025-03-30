from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(req):
    return render(req, 'AdminDashboard/new_admin_dashboard.html')