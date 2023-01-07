# Project

Create `creds` file

```yaml
[default]
aws_access_key_id=XXXXXXXXXXXX
aws_secret_access_key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

Create `conf` file

```yaml
[default]
region=us-east-1
```

Create an ssh key using

```bash
ssh-keygen -f terraform_ec2_key
```

Run

```bash
terraform init

terraform plan

terraform apply

terraform show
```

SSH into the machine visiting https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#Instances:sort=instanceId and copy the connect throw ssh command

```bash
# it should be like this one (make sure to remove the .pem)
ssh -i "terraform_ec2_key" ubuntu@XXXXXXXXXXXXXXXXXX.compute-1.amazonaws.com
```

Check the logs to check the crontab is working

To remove

```bash
terraform destroy

rm -rf .terraform && rm -rf .terraform.lock.hcl
```
