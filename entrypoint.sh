#!/usr/bin/env sh

die () {
  echo "$@" >&2
  exit 1
}

usage () {
  die "Usage: docker run aldwinb/rabbitmq-kinesis-publisher "\
"[-c cli_input_json -t token_code]" \
"[-d declarator_name]" \
"[-p partitioner_name]"
}

while getopts ":c" opt; do
  case ${opt} in
    c)
      cli_input_json=$OPTARG
      ;;
    t)
      token_code=$OPTARG
      ;;
    d)
      declarator=$OPTARG
      ;;
    p)
      partitioner=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG." >&2
      usage
      ;;
    :)
      echo die "Option -$OPTARG requires an argument." >&2
      usage
      ;;
  esac
done

if [[ ! -z ${cli_input_json+x} ]] && [[ ! -z ${token_code+x} ]]; then
  $(create-aws-sts-token -c /root/.aws/${cli_input_json} -t ${token_code})
fi

if [ "$?" -eq "0" ]; then
  python -u publisher.py /usr/src/app/config/config.ini ${declarator} \
${partitioner}
fi