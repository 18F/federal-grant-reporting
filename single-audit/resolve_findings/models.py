from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# @todo:
#   - Tweak STATUS_TYPE_CHOICES and FINDING_TYPE_CHOICES.
#   - Think through how to handle 'assignee'; what'll you do when the findings
#     have been resolved? Just have it okay for this to be null/unassigned? Or
#     have the resolved findings be 'assigned' to someone?
#         - Also: should 'status' + 'assignee' + 'due date of next action' be
#           bundled together?
#   - Think through how best to incorporate 'watchers'. (Not yet represented.)
#   - Decide how to handle/generate URLs. (Which fields would it make sense to
#     string together without getting too verbose?)
class Finding(models.Model):
    STATUS_TYPE_CHOICES = (
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('resolved', 'Resolved'),
    )
    FINDING_TYPE_CHOICES = (
        ('material_weakness', 'Material Weakness'),
        ('noncompliance', 'Noncompliance'),
        ('significant_deficiency', 'Significant Deficiency'),
    )
    name = models.CharField(max_length=250)
    number = models.CharField(max_length=35)
    condition = models.TextField()
    cause = models.TextField()
    criteria = models.TextField()
    effect = models.TextField()
    recommendation = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=35,
                              choices=STATUS_TYPE_CHOICES,
                              default='new')

    # @todo: Add the remainder!
    #
    # grantee = models.ForeignKey(Grantee, related_name='findings')
    # agencies_affected = models.ManyToManyField(Agency)
    # assignee = models.ForeignKey(User, related_name='active_findings')
    #
    # due_date_for_next_action
    # due_date_for_resolution (? is that a real thing?)
    # prior_year_findings  # @todo: Find out whether "related findings" is
    #                      # A Thing, outside of prior year findings. Or leave
    #                      # that question, for the moment, and focus on what
    #                      # you already know they need. Which is: prior year.
    #
    # corrective action plan (i.e., next action?)
    #   - what
    #   - by whom
    #   - by when
    # corrective_action_plan = models.TextField()
    # corrective_action_owner = models.ForeignKey(User, related_name='corrective_actions')
    # corrective_action_due_date = models.DateTimeField()
    #
    # comments
    #
    # grant [associated with this finding]? -- check how this is currently
    # represented.
    #
    # (@todo: Decide whether to include fiscal year or derive it from the
    # finding number. Might be easier to pull findings by fiscal year if `fiscal
    # year` is its own field, but hey.)

    class Meta:
        ordering = ('-status',)

    def __str__(self):
        return self.name
