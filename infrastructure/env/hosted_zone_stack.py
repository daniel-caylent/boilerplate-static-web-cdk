from aws_cdk import (
    aws_route53 as route53,
    aws_certificatemanager as acm,
    aws_ssm as ssm,
    RemovalPolicy
)
from constructs import Construct

from ..shared.base_stack import BaseStack
from ..shared import global_vars

class HostedZoneStack(BaseStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        zone = route53.HostedZone.from_lookup(
            self, 
            'hosted-zone',
            domain_name=global_vars.DOMAIN_NAME
        )

        cert = acm.Certificate(self, 'certificate',
            domain_name=global_vars.DOMAIN_NAME,
            subject_alternative_names=[f"*.{global_vars.DOMAIN_NAME}"],
            certificate_name= global_vars.DOMAIN_PREFIX,
            validation=acm.CertificateValidation.from_dns(zone)
        )
        cert.apply_removal_policy(RemovalPolicy.DESTROY)

        hz_param = ssm.StringParameter(
            self, "hosted-zone-param",
            string_value=zone.hosted_zone_id,
            parameter_name=f"{global_vars.DOMAIN_PREFIX}-hosted-zone-id"
        )
        cert_param = ssm.StringParameter(
            self, "cert-param",
            string_value=cert.certificate_arn,
            parameter_name=f"{global_vars.DOMAIN_PREFIX}-ssl-cert"
        )
