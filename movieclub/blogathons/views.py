from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST, require_safe

from movieclub.blogathons.forms import (
    BlogathonForm,
    EntryForm,
    ProposalForm,
    ProposalResponseForm,
)
from movieclub.blogathons.models import Blogathon, Entry, Proposal
from movieclub.decorators import require_auth, require_DELETE, require_form_methods
from movieclub.htmx import render_htmx
from movieclub.pagination import render_pagination
from movieclub.users.models import User


@require_safe
def blogathon_list(request: HttpRequest) -> HttpResponse:
    """Index list of blogathons."""
    blogathons = Blogathon.objects.available(request.user).order_by("-starts")
    if request.search:
        blogathons = blogathons.filter(name__icontains=request.search)
    return render_pagination(request, blogathons, "blogathons/index.html")


@require_form_methods
@require_auth
def add_blogathon(request: HttpRequest) -> HttpResponse:
    """Add new blogathon."""

    if request.method == "POST":
        form = BlogathonForm(request.POST)
        if form.is_valid():
            blogathon = form.save(commit=False)
            blogathon.organizer = request.user
            blogathon.save()

            messages.success(request, "Your blogathon has been added")

            return redirect("blogathons:blogathon_list")

    else:
        form = BlogathonForm()

    return render_htmx(
        request,
        "blogathons/blogathon_form.html",
        {"form": form},
        partial="form",
        target="blogathon_form",
    )


@require_safe
def blogathon_detail(
    request: HttpRequest, blogathon_id: int, slug: str
) -> HttpResponse:
    """Blogathon detail."""
    blogathon = get_object_or_404(
        Blogathon.objects.available(request.user).select_related("organizer"),
        pk=blogathon_id,
    )
    entries = blogathon.entries.order_by("-created").select_related("participant")

    if request.user.is_authenticated and request.user != blogathon.organizer:
        proposal = (
            blogathon.proposals.filter(participant=request.user).order_by("-pk").first()
        )
    else:
        proposal = None

    return render_pagination(
        request,
        entries,
        "blogathons/detail.html",
        {
            "blogathon": blogathon,
            "proposal": proposal,
            "is_organizer": request.user == blogathon.organizer,
            "can_submit_entry": blogathon.can_submit_entry(request.user),
            "can_submit_proposal": blogathon.can_submit_proposal(request.user),
        },
    )


def blogathons_for_user(request: HttpRequest, username: str) -> HttpResponse:
    """Blogathons user has organized or participated in."""
    user = get_object_or_404(User, is_active=True, username=username)
    return render_pagination(
        request,
        Blogathon.objects.available(request.user)
        .filter(Q(organizer=user) | Q(entries__participant=user))
        .distinct()
        .order_by("-starts"),
        "blogathons/blogathon_user_list.html",
        {"current_user": user},
    )


@require_form_methods
@require_auth
def edit_blogathon(request: HttpRequest, blogathon_id: int) -> HttpResponse:
    """Edit blogathon detail."""
    blogathon = get_object_or_404(
        Blogathon.objects.for_organizer(request.user), pk=blogathon_id
    )
    if request.method == "POST":
        form = BlogathonForm(request.POST, instance=blogathon)
        if form.is_valid():
            messages.success(request, "Your blogathon has been updated")
            form.save()
            return redirect(blogathon)
    else:
        form = BlogathonForm(instance=blogathon)

    return render_htmx(
        request,
        "blogathons/blogathon_form.html",
        {
            "blogathon": blogathon,
            "form": form,
        },
        partial="form",
        target="blogathon_form",
    )


@require_POST
@require_auth
def publish_blogathon(request: HttpRequest, blogathon_id: int) -> HttpResponse:
    """Makes blogathon public."""
    blogathon = get_object_or_404(
        Blogathon.objects.for_organizer(request.user),
        published__isnull=True,
        pk=blogathon_id,
    )
    blogathon.published = timezone.now()
    blogathon.save()

    messages.success(request, "Blogathon is published")

    return redirect(blogathon)


@require_safe
@require_auth
def blogathon_proposals(request: HttpRequest, blogathon_id: int) -> HttpResponse:
    """Return all proposals."""
    blogathon = get_object_or_404(
        Blogathon.objects.for_organizer(request.user), pk=blogathon_id
    )
    proposals = blogathon.proposals.order_by("-created").select_related("participant")

    return render_pagination(
        request,
        proposals,
        "blogathons/proposals.html",
        {
            "blogathon": blogathon,
        },
    )


@require_safe
@require_auth
def proposal_detail(request: HttpRequest, proposal_id: int) -> HttpResponse:
    """Return all proposals."""
    proposal = get_object_or_404(
        Proposal.objects.filter(
            Q(
                blogathon__organizer=request.user,
            )
            | Q(participant=request.user)
        ).select_related(
            "blogathon",
            "blogathon__organizer",
            "participant",
        ),
        pk=proposal_id,
    )

    return render(
        request,
        "blogathons/proposal.html",
        {
            "blogathon": proposal.blogathon,
            "proposal": proposal,
            "is_organizer": proposal.blogathon.organizer == request.user,
        },
    )


@require_form_methods
@require_auth
def submit_proposal(request: HttpRequest, blogathon_id: int) -> HttpResponse:
    """Submit proposal to blogathon."""
    blogathon = get_object_or_404(
        Blogathon.objects.available(request.user).select_related("organizer"),
        pk=blogathon_id,
    )
    if not blogathon.can_submit_proposal(request.user):
        raise PermissionDenied("You cannot submit a proposal at this time.")

    if request.method == "POST":
        form = ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.blogathon = blogathon
            proposal.participant = request.user
            proposal.save()

            # TBD send email to organizer

            messages.success(request, "Your proposal has been submitted")

            return redirect(proposal.get_absolute_url())
    else:
        form = ProposalForm()

    return render_htmx(
        request,
        "blogathons/proposal_form.html",
        {"blogathon": blogathon, "form": form},
        partial="form",
        target="proposal_form",
    )


@require_form_methods
@require_auth
def respond_to_proposal(request: HttpRequest, proposal_id: int) -> HttpResponse:
    """Render proposal response form."""
    proposal = get_object_or_404(
        Proposal.objects.select_related("blogathon", "participant"),
        blogathon__organizer=request.user,
        status=Proposal.Status.SUBMITTED,
        pk=proposal_id,
    )
    if request.method == "POST":
        form = ProposalResponseForm(request.POST, instance=proposal)

        if form.is_valid():
            match request.POST.get("action"):
                case "accept":
                    status = Proposal.Status.ACCEPTED

                case "reject":
                    status = Proposal.Status.REJECTED

                case _:
                    return HttpResponseBadRequest("Invalid action")

            proposal = form.save(commit=False)
            proposal.status = status
            proposal.status_changed_at = timezone.now()

            proposal.save()

            messages.success(
                request,
                f"Proposal has been {proposal.get_status_display()}",
            )

            return redirect(proposal.get_absolute_url())
    else:
        form = ProposalResponseForm(instance=proposal)

    return render_htmx(
        request,
        "blogathons/proposal_response_form.html",
        {
            "form": form,
            "blogathon": proposal.blogathon,
            "proposal": proposal,
        },
        partial="form",
        target="proposal-response-form",
    )


@require_form_methods
@require_auth
def submit_entry(request: HttpRequest, blogathon_id: int) -> HttpResponse:
    """Submit an entry."""
    blogathon = get_object_or_404(
        Blogathon.objects.available(request.user),
        pk=blogathon_id,
    )
    if not blogathon.can_submit_entry(request.user):
        raise PermissionDenied("You cannot submit an entry")

    if request.method == "POST":
        form = EntryForm(request.POST)

        if form.is_valid():
            entry = form.save(commit=False)
            entry.blogathon = blogathon
            entry.participant = request.user
            entry.save()

            messages.success(request, "Your entry has been submitted!")
            return redirect(blogathon)
    else:
        form = EntryForm()

    return render_htmx(
        request,
        "blogathons/entry_form.html",
        {
            "blogathon": blogathon,
            "form": form,
        },
        partial="form",
        target="entry-form",
    )


@require_safe
def entry_detail(request: HttpRequest, entry_id: int) -> HttpResponse:
    """Render entry details."""

    entry = get_object_or_404(
        Entry.objects.select_related(
            "blogathon", "blogathon__organizer", "participant"
        ),
        pk=entry_id,
    )

    return render(
        request,
        "blogathons/entry.html",
        {
            "entry": entry,
            "blogathon": entry.blogathon,
        },
    )


@require_form_methods
@require_auth
def edit_entry(request: HttpRequest, entry_id: int) -> HttpResponse:
    """Update an entry."""
    entry = get_object_or_404(
        Entry.objects.select_related(
            "blogathon",
            "blogathon__organizer",
            "participant",
        ),
        participant=request.user,
        pk=entry_id,
    )

    if request.method == "POST":
        form = EntryForm(request.POST, instance=entry)

        if form.is_valid():
            form.save()
            messages.success(request, "Your entry has been updated")
            return redirect(entry)

    else:
        form = EntryForm(instance=entry)

    return render_htmx(
        request,
        "blogathons/entry_form.html",
        {
            "blogathon": entry.blogathon,
            "entry": entry,
            "form": form,
        },
        partial="form",
        target="entry-form",
    )


@require_DELETE
def delete_entry(request: HttpRequest, entry_id: int) -> HttpResponse:
    """Delete an entry."""
    entry = get_object_or_404(
        Entry.objects.select_related(
            "blogathon",
        ),
        participant=request.user,
        pk=entry_id,
    )

    entry.delete()

    messages.info(request, "Your entry has been deleted")
    return redirect(entry.blogathon)
