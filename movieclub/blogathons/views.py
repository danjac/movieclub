from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.db.models import Q, QuerySet
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
from movieclub.pagination import render_pagination
from movieclub.users.models import User


@require_safe
def blogathon_list(request: HttpRequest) -> HttpResponse:
    """Index list of blogathons."""
    return render_pagination(
        request,
        _get_available_blogathons(request.user).order_by("-start_date"),
        "blogathons/index.html",
    )


@require_safe
def organizer_blogathon_list(request: HttpRequest) -> HttpResponse:
    """Index list of blogathons for current user."""
    return render_pagination(
        request,
        Blogathon.objects.filter(user=request.user).order_by("-start_date"),
        "blogathons/organizer_blogathon_list.html",
        {
            "organizer": request.user,
        },
    )


@require_safe
@require_auth
def proposals(request: HttpRequest, blogathon_id: int) -> HttpResponse:
    """Return all proposals."""
    blogathon = get_object_or_404(
        _get_available_blogathons(request.user), pk=blogathon_id
    )
    proposals = blogathon.proposals.order_by("-created").select_related("participant")

    if request.user != blogathon.organizer:
        proposals = proposals.filter(participant=request.user)

    if status := request.GET.get("status", None):
        proposals = proposals.filter(status=status)

    return render_pagination(
        request,
        "blogathons/proposals.html",
        proposals,
        {
            "blogathon": blogathon,
            "proposal_status": status,
            "can_respond": timezone.now().date() > blogathon.start_date,
        },
    )


@require_POST
@require_auth
def respond_to_proposal(request: HttpRequest, proposal_id: int) -> HttpResponse:
    """Reject proposal."""
    proposal = get_object_or_404(
        Proposal,
        blogathon__organizer=request.user,
        status=Proposal.Status.SUBMITTED,
        pk=proposal_id,
    )

    form = ProposalResponseForm(request.POST, instance=proposal)
    if form.is_valid():
        proposal = form.save()
        # TBD: send relevant emails etc

        return redirect()
    return HttpResponse()


@require_safe
def blogathon_detail(
    request: HttpRequest, blogathon_id: int, slug: str
) -> HttpResponse:
    """Blogathon detail."""
    blogathon = get_object_or_404(Blogathon, _get_available_blogathons(request.user))
    entries = blogathon.entries.order_by("-created").select_related("participant")

    return render_pagination(
        request,
        "blogathons/detail.html",
        entries,
        {
            "blogathon": blogathon,
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

            return redirect(blogathon)

    else:
        form = BlogathonForm()

    return render()


@require_form_methods
@require_auth
def edit_blogathon(request: HttpRequest, blogathon_id: int) -> HttpResponse:
    """Edit blogathon detail."""
    blogathon = get_object_or_404(
        _get_blogathons_for_organizer(request.user), pk=blogathon_id
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
    """Makes ."""
    blogathon = get_object_or_404(
        _get_blogathons_for_organizer(request.user), pk=blogathon_id
    )
    blogathon.submitted = timezone.now()
    blogathon.save()
    return HttpResponse()


@require_POST
@require_auth
def submit_proposal(request: HttpRequest, blogathon_id: int) -> HttpResponse:
    """Makes ."""
    blogathon = get_object_or_404(
        _get_available_blogathons(request.user),
        start_date__gt=timezone.now(),
        pk=blogathon_id,
    )
    if not blogathon.can_submit_proposal(request.user):
        raise PermissionDenied("You have already submitted a proposal")

    form = ProposalForm(request.POST)
    if form.is_valid():
        proposal = form.save(commit=False)
        proposal.blogathon = blogathon
        proposal.user = request.user
        proposal.save()

    return HttpResponse()


@require_POST
@require_auth
def submit_entry(request: HttpRequest, blogathon_id: int) -> HttpResponse:
    """Makes ."""
    blogathon = get_object_or_404(
        _get_available_blogathons(request.user),
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


def _get_blogathons_for_organizer(user: User) -> QuerySet[Blogathon]:
    return Blogathon.objects.filter(organizer=user)


def _get_available_blogathons(user: User | AnonymousUser) -> QuerySet[Blogathon]:
    qs = Blogathon.objects.select_related("organizer")

    if user.is_authenticated:
        qs = qs.filter(Q(organizer=user) | Q(submitted__isnull=False))

    else:
        qs = qs.filter(submitted__isnull=False)

    return qs
