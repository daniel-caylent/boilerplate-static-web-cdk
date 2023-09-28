#!/usr/bin/env python3

import aws_cdk as cdk

from ..shared import global_vars
from .web_stack import WebStack

app = cdk.App()
WebStack(app, "WebStack")

cdk.Tags.of(app).add("project", global_vars.DOMAIN_PREFIX)
app.synth()
