from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST, require_safe

from movieclub.blogathons.forms import (
    BlogathonForm,
    EntryForm,
    ProposalForm,
    ProposalResponseForm,
)
from movieclub.blogathons.models import Blogathon, Proposal
from movieclub.decorators import require_auth, require_form_methods
from movieclub.htmx import render_htmx
from movieclub.pagination import render_pagination


@require_safe
def blogathon_list(request: HttpRequest) -> HttpResponse:
    """Index list of blogathons."""
    return render_pagination(
        request,
        Blogathon.objects.available(request.user).order_by("-starts"),
        "blogathons/index.html",
    )


@require_safe
def organizer_blogathon_list(request: HttpRequest) -> HttpResponse:
    """Index list of blogathons for current user."""
    return render_pagination(
        request,
        Blogathon.objects.for_organizer(request.user).order_by("-starts"),
        "blogathons/organizer.html",
        {
            "organizer": request.user,
        },
    )


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

    return render(request, "blogathons/blogathon_form.html", {"form": form})


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

    return render_pagination(
        request,
        entries,
        "blogathons/detail.html",
        {
            "blogathon": blogathon,
            "is_organizer": request.user == blogathon.organizer,
            "can_submit_entry": blogathon.can_submit_entry(request.user),
            "can_submit_proposal": blogathon.can_submit_proposal(request.user),
        },
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
        form.save()
    else:
        form = BlogathonForm(instance=blogathon)

    return render()


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

    if status := request.GET.get("status", None):
        proposals = proposals.filter(status=status)

    return render_pagination(
        request,
        proposals,
        "blogathons/proposals.html",
        {
            "blogathon": blogathon,
            "proposal_status": status,
        },
    )


@require_form_methods
@require_auth
def submit_proposal(request: HttpRequest, blogathon_id: int) -> HttpResponse:
    """Submit proposal to blogathon."""
    blogathon = get_object_or_404(
        Blogathon.objects.available(request.user).select_related("organizer"),
        starts__gt=timezone.now(),
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

            return redirect(blogathon)
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
    """Reject or accept proposal."""
    proposal = get_object_or_404(
        Proposal.objects.select_related("blogathon", "participant"),
        blogathon__organizer=request.user,
        status=Proposal.Status.SUBMITTED,
        pk=proposal_id,
    )

    target = f"proposal-{proposal.pk}"
    template_name = "blogathons/proposals.html"
    context = {"proposal": proposal}

    if request.method == "POST":
        action = request.POST.get("action", "cancel")
        is_valid = False

        if action in ("accept", "reject"):
            form = ProposalResponseForm(request.POST, instance=proposal)
            if is_valid := form.is_valid():
                proposal = form.save(commit=False)
                proposal.status = (
                    Proposal.Status.ACCEPTED
                    if action == "accept"
                    else Proposal.Status.REJECTED
                )
                proposal.status_changed_at = timezone.now()
                # TBD: email participant
                proposal.save()
                is_valid = True

        if is_valid or action == "cancel":
            return render_htmx(
                request,
                template_name,
                context,
                partial="proposal",
                target=target,
            )
    else:
        form = ProposalResponseForm(instance=proposal)

    return render_htmx(
        request,
        template_name,
        {
            **context,
            "form": form,
        },
        partial="response_form",
        target=target,
    )


@require_POST
@require_auth
def submit_entry(request: HttpRequest, blogathon_id: int) -> HttpResponse:
    """Makes ."""
    blogathon = get_object_or_404(
        Blogathon.objects.for_organizer(request.user),
        pk=blogathon_id,
    )
    if not blogathon.can_submit_entry(request.user):
        raise PermissionDenied("You cannot submit an entry")

    form = EntryForm(request.POST)
    if form.is_valid():
        entry = form.save(commit=False)
        entry.blogathon = blogathon
        entry.user = request.user
        entry.save()

    return HttpResponse()
