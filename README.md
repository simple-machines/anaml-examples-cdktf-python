# Readme

This repository uses [Terraform]() and the [CDKTF]() project to create Anaml
definitions from Python code.

As CDKTF uses Terraform, the definitions are compared with the Anaml database
and only differences are applied.

This setup is typically used in a CI pipeline where the definitions are kept in
a source code repository and a CI job runs CDKTF on check-in to sync the
definitions into Anaml.

This repository creates examples based on the
[TPC-DS](https://www.tpc.org/tpcds/default5.asp) dataset. This document assumes
the reader is familiar with Anaml concepts.

The 

## Setup

**Note:** On Windows we recommend using WSL, and therefore following the Linux
instructions.

1. Install Terraform: https://developer.hashicorp.com/terraform/downloads
2. Install NodeJS (required for CDKTF): https://nodejs.org/en/download/
3. Install CDKTF: https://developer.hashicorp.com/terraform/tutorials/cdktf/cdktf-install
4. Install pipenv: https://pipenv.pypa.io/en/latest/install/

## Running this repo

1. Export the following Environment variables:
   ```bash
   export ANAML_URL=https://your.anaml.host/api
   export ANAML_APIKEY=your_api_key
   export ANAML_SECRET=your_api_secret
   ```
2. Create a DataSource in Anaml called `tpcds_source`. It can be of any type and
   doesn't need to contain data unless you want to test the definitions.
3. Create a branch in Anaml called `cdktf_tpcds`. 
4. Install the Python packages:
   ```bash
   pipenv install
   ```
5. Generate the CDKTF imports:
   ```bash
   cdktf get
   ```
6. Run a Diff/Plan to see what changes would be applied to the Anaml database:
   ```bash
   cdktf plan
   ```
7. Run a Deploy/Apply to make these changes to Anaml:
   ```bash
   cdktf apply
   ```

## Error: Could not retrieve providers for locking

If you receive this error:
```bash
cd cdktf.out/stacks/terraform
rm .terraform.lock.hcl
terraform init
cd -
```
