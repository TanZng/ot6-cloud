# Practical Session 4 : Introduction to Terraform

Create `creds` file

```yaml
[default]
aws_access_key_id=XXXXXXXXXXXX
aws_secret_access_key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```


Create `conf` file

```yaml
[default]
region=us-west-2
```

Run

```bash
terraform init

terraform plan

terraform apply

terraform show
```

To remove

```bash
terraform destroy

rm -rf .terraform && rm -rf .terraform.lock.hcl
```