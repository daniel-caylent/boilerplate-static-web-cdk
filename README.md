Although server rendered websites are coming back in fashion, client-rendered solutions are still suitable, simple, and inexpensive, solutions for many use cases. In this repository I aim to provide you with a jumping off point to build your own static S3 hosted web application that will require minimal changes to get up and running.

This repository utilizes CDK to deploy resources. It will generate an S3 bucket to host your static site, generate a Cloudfront distribution, add Route53 records to route your domain name to Cloudfront. It will also generate an auto-renewing SSL certificate, which certainly used to be the crux for this type of solution.

# Pre-Reqs
Have CDK installed. Have a domain name hosted on AWS Route53 with an existing hosted zone. Setup your AWS credentials to work with CDK. Node and NPM should be installed to develop your web application.

# Repository overview
This monolith repository is designed to contain multiple services that are individually deployable. At the root level of this project, you see three directories `web`, `infrastrucutre`, and `scripts`.

The `web` directory contains our static website. In this case, the site is React/Vite and will generate a directory `./web/dist` when the site is built for distribution. This `dist` directory is imperative to this project as it is linked to the S3 deployment.

Looking at the `infrastructure` directory, you will see three sub-directories: `web`, `env`, and `shared`. `env` contains the infrastructure for the backbone of our application. It may contain VPCs or RDS instances or whatever else your application depends on. In this case, `env` pulls in an existing Hosted Zone from Route53 and creates an SSL cert. `web` contains the infrastructure specific to serving our static site: a Cloudfront distribution, an S3 bucket and deployment, and some additional records for our hosted zone. `shared` contains code that will be shared accross CDK applications.

The last root-level directory, `scripts`, contains the executables necessary to streamline the cdk deploy/destroy commands. Because this mono-repo contains multiple CDK projects it is useful to use these scripts to manage them. 

# Setup

Install the requirements for CDK:

```
python3 -m venv .venv
source ./.venv/bin/activate
pip3 install -r requirements.txt
```

Install the requirements for the React application and make an initial build:
```
cd ./web
npm install
npm run build
```

Add your custom domain name, AWS Account number, and AWS region in `./infrastrucutre/shared/global_vars.py`.

# Deployment

Start by deploying the environment:
`./scripts/deploy_env.py`

Then the static web:
`./scripts/deploy_web.py`

# Testing

Wait a few minutes and try your custom domain in the web browser! If it doesn't work, check your Route53 Hosted Zone to ensure there aren't conflicting entries.

# Destroy

Start by destroying the static web:
`./scripts/destroy_web.py`

Then by destroying the environment:
`./scripts/destroy_env.py`
