import json
import logging
import os
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.html import strip_tags
from .models import ContactMessage

logger = logging.getLogger(__name__)

PROJECTS = [
    {
        "title": "DoffRemote — Smart STB Remote",
        "category": "Software / Flutter",
        "description": "A Flutter application concept for discovering and controlling a compatible Lifestar set-top box, with remote, casting and media utility features.",
        "stack": ["Flutter", "Dart", "REST API"],
        "url": "https://github.com/doffn/Lifestar-Smart-Remote",
        "featured": True,
    },
    {
        "title": "Aviation MRO Job Tracker",
        "category": "Automation / Backend",
        "description": "A Python-based job discovery and matching workflow for international aviation MRO and engine-shop opportunities, with configurable keywords and notifications.",
        "stack": ["Python", "Web scraping", "JSON", "Telegram"],
        "url": "https://github.com/doffn",
        "featured": True,
    },
    {
        "title": "AI & Computer Vision Experiments",
        "category": "Artificial Intelligence",
        "description": "Machine-learning and computer-vision learning projects, including object detection workflows and predictive analytics experiments.",
        "stack": ["Machine Learning", "YOLOv8", "Computer Vision"],
        "url": "https://github.com/doffn",
        "featured": False,
    },
]

@ensure_csrf_cookie
def home(request):
    return render(request, "myApp/index.html", {"projects": PROJECTS})

def health(request):
    return JsonResponse({"status": "ok", "service": "Doff Neri portfolio"})

def projects_api(request):
    return JsonResponse({"projects": PROJECTS})

@require_POST
def contact_api(request):
    # Accept JSON and normal form submissions.
    try:
        if request.content_type == "application/json":
            payload = json.loads(request.body.decode("utf-8") or "{}")
        else:
            payload = request.POST
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "Invalid request body."}, status=400)

    # Honeypot field: bots often fill every input.
    if payload.get("website"):
        return JsonResponse({"ok": True, "message": "Thanks. Your message has been received."})

    name = str(payload.get("name", "")).strip()
    email = str(payload.get("email", "")).strip()
    subject = str(payload.get("subject", "")).strip()
    message = str(payload.get("message", "")).strip()

    if not name or not email or not message:
        return JsonResponse({"ok": False, "error": "Please complete your name, email and message."}, status=400)
    if len(name) > 120 or len(subject) > 180 or len(message) > 5000:
        return JsonResponse({"ok": False, "error": "One or more fields are too long."}, status=400)

    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"ok": False, "error": "Please enter a valid email address."}, status=400)

    record = ContactMessage.objects.create(
        name=name, email=email, subject=subject, message=message
    )

    # Optional email notification. Messages are still stored if email is not configured.
    if settings.DEFAULT_FROM_EMAIL and os.getenv("CONTACT_NOTIFICATION_EMAIL"):
        try:
            send_mail(
                subject=f"Portfolio contact: {subject or 'New message'}",
                message=f"From: {name} <{email}>\n\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[os.getenv("CONTACT_NOTIFICATION_EMAIL")],
                fail_silently=False,
            )
        except Exception:
            logger.exception("Contact notification email failed for message %s", record.pk)

    return JsonResponse({"ok": True, "message": "Thanks — your message has been received."}, status=201)
