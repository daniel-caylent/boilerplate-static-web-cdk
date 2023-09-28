#!/usr/bin/env python3

import aws_cdk as cdk

from .hosted_zone_stack import HostedZoneStack
from ..shared import global_vars

app = cdk.App()
HostedZoneStack(app, "hosted-zone-stack")

cdk.Tags.of(app).add("project", global_vars.DOMAIN_PREFIX)
app.synth()
