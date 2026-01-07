# core/emails.py
"""
Email notification utilities for AccessAdvisr.

Sends emails for:
- Review submission confirmation
- Review approval notification
- New user welcome
- Venue claim status updates
"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_review_submitted_email(review):
    """
    Send confirmation email when a user submits a review.
    Only sends if the user provided an email address.
    """
    if not review.author_email:
        return False
    
    try:
        subject = f"Thank you for reviewing {review.listing.name} on AccessAdvisr"
        
        context = {
            'review': review,
            'listing': review.listing,
            'site_url': settings.SITE_URL,
        }
        
        html_content = render_to_string('emails/review_submitted.html', context)
        text_content = strip_tags(html_content)
        
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[review.author_email],
            html_message=html_content,
            fail_silently=False,
        )
        
        logger.info(f"Review submitted email sent to {review.author_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send review submitted email: {e}")
        return False


def send_review_approved_email(review):
    """
    Send notification when a review is approved by moderators.
    """
    if not review.author_email:
        return False
    
    try:
        subject = f"Your review of {review.listing.name} has been published!"
        
        context = {
            'review': review,
            'listing': review.listing,
            'site_url': settings.SITE_URL,
            'listing_url': f"{settings.SITE_URL}/listing/{review.listing.pk}/",
        }
        
        html_content = render_to_string('emails/review_approved.html', context)
        text_content = strip_tags(html_content)
        
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[review.author_email],
            html_message=html_content,
            fail_silently=False,
        )
        
        logger.info(f"Review approved email sent to {review.author_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send review approved email: {e}")
        return False


def send_welcome_email(user):
    """
    Send welcome email to newly registered users.
    """
    if not user.email:
        return False
    
    try:
        subject = "Welcome to AccessAdvisr! 🎉"
        
        context = {
            'user': user,
            'site_url': settings.SITE_URL,
        }
        
        html_content = render_to_string('emails/welcome.html', context)
        text_content = strip_tags(html_content)
        
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_content,
            fail_silently=False,
        )
        
        logger.info(f"Welcome email sent to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send welcome email: {e}")
        return False


def send_listing_submitted_email(listing, submitter_email=None):
    """
    Send confirmation when a user submits a new venue listing.
    """
    if not submitter_email:
        return False
    
    try:
        subject = f"Your venue submission '{listing.name}' is under review"
        
        context = {
            'listing': listing,
            'site_url': settings.SITE_URL,
        }
        
        html_content = render_to_string('emails/listing_submitted.html', context)
        text_content = strip_tags(html_content)
        
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[submitter_email],
            html_message=html_content,
            fail_silently=False,
        )
        
        logger.info(f"Listing submitted email sent to {submitter_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send listing submitted email: {e}")
        return False


def send_listing_approved_email(listing, submitter_email=None):
    """
    Send notification when a venue listing is approved.
    """
    if not submitter_email:
        return False
    
    try:
        subject = f"Great news! '{listing.name}' is now live on AccessAdvisr!"
        
        context = {
            'listing': listing,
            'site_url': settings.SITE_URL,
            'listing_url': f"{settings.SITE_URL}/listing/{listing.pk}/",
        }
        
        html_content = render_to_string('emails/listing_approved.html', context)
        text_content = strip_tags(html_content)
        
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[submitter_email],
            html_message=html_content,
            fail_silently=False,
        )
        
        logger.info(f"Listing approved email sent to {submitter_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send listing approved email: {e}")
        return False


def notify_admin_new_submission(item_type, item):
    """
    Notify admin users about new submissions requiring moderation.
    In production, this could email a list of admins.
    """
    # This is a stub - in production, you'd email admins
    logger.info(f"New {item_type} submission: {item}")
    return True
