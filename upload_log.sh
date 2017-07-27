aws logs create-log-group --profile raijin-cwl --log-group-name example-run
aws logs create-log-stream --profile raijin-cwl --log-group-name example-run --log-stream-name 201707271
aws logs create-log-stream --profile raijin-cwl --log-group-name example-run --log-stream-name 201707272
aws logs create-log-stream --profile raijin-cwl --log-group-name example-run --log-stream-name 201707273

aws logs put-log-events --profile raijin-cwl --log-group-name example-run --log-stream-name 201707271 --log-events file://head.log1
aws logs put-log-events --profile raijin-cwl --log-group-name example-run --log-stream-name 201707272 --log-events file://head.log2
aws logs put-log-events --profile raijin-cwl --log-group-name example-run --log-stream-name 201707273 --log-events file://head.log3

