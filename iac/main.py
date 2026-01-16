from __future__ import annotations

from pathlib import Path

from config.env_updater import EnvUpdater
from config.logging_config import get_logger
from config.main import Config, State
from iac.aws_factory import AWSClientFactory
from iac.base import ResourceResult
from iac.bucket import Bucket
from iac.configs import (
    BucketConfig,
    FirehoseConfig,
    LambdaConfig,
    RoleConfig,
)
from iac.firehose import FireHose
from iac.lambda_fn import LambdaProcessor
from iac.orchestrator import InfrastructureOrchestrator
from iac.role import Role

logger = get_logger(__name__)


def ensure_infra(update_env: bool = False, env_path: Path = Path(".env")) -> dict:
    cfg = Config.from_env()
    region = cfg.REGION_NAME

    factory = AWSClientFactory(region=region)
    s3 = factory.create_s3_client()
    iam = factory.create_iam_client()
    lam = factory.create_lambda_client()
    firehose = factory.create_firehose_client()

    orchestrator = InfrastructureOrchestrator()

    bucket_config = BucketConfig.from_config(cfg, region)
    bucket_resource = Bucket(bucket_config, s3)
    orchestrator.register("bucket", bucket_resource)

    lambda_config = LambdaConfig.from_config(cfg, role_arn=None)
    lambda_resource = LambdaProcessor(lambda_config, lam, iam_client=iam)
    orchestrator.register("lambda", lambda_resource)

    def create_role(results: dict[str, ResourceResult]) -> Role:
        bucket_res = results["bucket"]
        lambda_res = results["lambda"]
        role_config = RoleConfig.from_config(
            cfg, bucket_res.bucket_arn, lambda_res.lambda_arn
        )
        return Role(role_config, iam)

    orchestrator.register("role", depends_on=["bucket", "lambda"], factory=create_role)

    def create_firehose(results: dict[str, ResourceResult]) -> FireHose:
        firehose_config = FirehoseConfig.from_config(
            cfg,
            role_arn=results["role"].role_arn,
            bucket_arn=results["bucket"].bucket_arn,
            lambda_arn=results["lambda"].lambda_arn,
        )
        firehose_resource = FireHose(firehose_config, firehose)
        firehose_resource._timeout_s = 100
        return firehose_resource

    orchestrator.register(
        "firehose", depends_on=["role", "bucket", "lambda"], factory=create_firehose
    )

    results = orchestrator.ensure_all()
    bucket_res = results["bucket"]
    lambda_res = results["lambda"]
    role_res = results["role"]
    results["firehose"]

    new_state = State(
        ROLE_ARN=role_res.role_arn,
        BUCKET_ARN=bucket_res.bucket_arn,
        LAMBDA_ARN=lambda_res.lambda_arn,
    )
    new_state.save()

    if update_env:
        updater = EnvUpdater(env_path=env_path)
        updater.update(
            role_arn=new_state.ROLE_ARN,
            bucket_arn=new_state.BUCKET_ARN,
            lambda_arn=new_state.LAMBDA_ARN,
        )

    logger.info("Infrastructure setup complete")
    return {
        "region": region,
        "delivery_stream_name": cfg.DELIVERY_STREAM_NAME,
        "role_arn": new_state.ROLE_ARN,
        "bucket_arn": new_state.BUCKET_ARN,
        "lambda_arn": new_state.LAMBDA_ARN,
    }
