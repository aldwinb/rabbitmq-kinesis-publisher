#!/usr/bin/env sh

die () {
  echo "$@" >&2
  exit 1
}

usage () {
  die "Usage: create-aws-sts-token "\
"-c cli_input_json "\
"-t token_code"
}

while getopts "c:t:" opt; do
  case ${opt} in
    c)
      cli_input_json=$OPTARG
      ;;
    t)
      token_code=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG." >&2
      usage
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      usage
      ;;
  esac
done

if [[ -z ${cli_input_json} ]] || [[ -z ${token_code} ]]
then
   usage
fi

unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
unset AWS_SESSION_TOKEN

aws sts get-session-token \
--cli-input-json file://${cli_input_json} \
--token-code ${token_code} | \
jq -r '.Credentials | "export AWS_ACCESS_KEY_ID="+.AccessKeyId,"export AWS_SECRET_ACCESS_KEY="+.SecretAccessKey,"export AWS_SESSION_TOKEN="+.SessionToken'