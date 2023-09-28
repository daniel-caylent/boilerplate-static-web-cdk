from aws_cdk import (
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_ssm as ssm,
    RemovalPolicy,
)
from constructs import Construct

from ..shared.base_stack import BaseStack
from ..shared.paths import WEB_DIST_PATH
from ..shared import global_vars


class WebStack(BaseStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a bucket to host the static pages
        bucket = s3.Bucket(
            self, "web-bucket", bucket_name=f"www-{global_vars.DOMAIN_PREFIX}",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # Populate the bucket with static pages
        bucket_deployment = s3_deployment.BucketDeployment(
            self, "bucket-deployment", destination_bucket=bucket,
            sources=[s3_deployment.Source.asset(WEB_DIST_PATH)]
        )

        # Select the EXISTING SSL certificate
        cert_arn = ssm.StringParameter.value_for_string_parameter(self, f"{global_vars.DOMAIN_PREFIX}-ssl-cert")
        cert = acm.Certificate.from_certificate_arn(self, "ssl-cert", cert_arn)

        # Create a cloudfront distribution
        cf = cloudfront.Distribution(
            self, "cf-distribution",
            default_root_object="index.html",
            certificate=cert,
            domain_names=[global_vars.DOMAIN_NAME, f"www.{global_vars.DOMAIN_NAME}"],
            default_behavior={
                "origin": origins.S3Origin(bucket),
                "viewer_protocol_policy": cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            }
        )

        # Select the EXISTING Hosted zone
        zone_id = ssm.StringParameter.value_for_string_parameter(self, f"{global_vars.DOMAIN_PREFIX}-hosted-zone-id")
        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self, "hosted-zone",
            hosted_zone_id=zone_id,
            zone_name=global_vars.DOMAIN_NAME
        )
        
        # Add A records to fordward traffic to cloudfront
        www_record = route53.ARecord(
            self, "www-a-record", zone=hosted_zone,
            record_name=f"www.{global_vars.DOMAIN_NAME}",
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(cf))
        )
        record = route53.ARecord(
            self, "a-record", zone=hosted_zone,
            record_name=global_vars.DOMAIN_NAME,
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(cf))
        )