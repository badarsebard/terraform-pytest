from python_terraform import Terraform


def test_bucket_created(tfenv: Terraform):
    resources = tfenv.tfstate.resources
    bucket_instances = [r for r in resources if r.get("type") == "aws_s3_bucket"]
    assert len(bucket_instances) == 1
    bucket = bucket_instances[0].get('instances')[0]
    assert bucket.get('attributes').get('bucket') == 'my_test_bucket'
