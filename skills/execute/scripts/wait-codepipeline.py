"""Read-only AWS CodePipeline waiter for one execution and its expected source revision."""
import argparse
import json
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pipeline", required=True)
    parser.add_argument("--execution", required=True)
    parser.add_argument("--revision", required=True, help="Expected full source revision, not a branch name")
    parser.add_argument("--profile", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--timeout", type=float, default=600, help="Maximum wait in seconds")
    parser.add_argument("--interval", type=float, default=15, help="Seconds between status reads")
    args = parser.parse_args()
    if not (0 < args.timeout < float("inf") and 0 < args.interval < float("inf")):
        parser.error("timeout and interval must be finite positive numbers")
    command = ["aws", "codepipeline", "get-pipeline-execution", "--pipeline-name", args.pipeline,
               "--pipeline-execution-id", args.execution, "--profile", args.profile,
               "--region", args.region, "--output", "json", "--no-cli-pager"]
    deadline = time.monotonic() + args.timeout
    previous = None
    while time.monotonic() < deadline:
        result = subprocess.run(command, capture_output=True, text=True,
                                timeout=min(30, deadline - time.monotonic()))
        if result.returncode:
            raise RuntimeError(result.stderr.strip() or "AWS status read failed")
        execution = json.loads(result.stdout)["pipelineExecution"]
        if execution.get("pipelineExecutionId") != args.execution:
            raise RuntimeError("AWS returned a different pipeline execution")
        revisions = [item.get("revisionId") for item in execution.get("artifactRevisions", [])]
        if args.revision not in revisions:
            raise RuntimeError("Expected source revision is absent from this execution")
        status = execution["status"]
        if status != previous:
            print(json.dumps({"execution": args.execution, "revision": args.revision,
                              "status": status}), flush=True)
            previous = status
        if status == "Succeeded":
            return
        if status not in {"InProgress", "Stopping"}:
            raise RuntimeError(f"Pipeline execution ended with {status}")
        time.sleep(min(args.interval, max(0, deadline - time.monotonic())))
    raise RuntimeError("Pipeline execution timed out; no deployment action was taken")


if __name__ == "__main__":
    try:
        main()
    except subprocess.TimeoutExpired:
        sys.exit("Pipeline status read timed out; no deployment action was taken")
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
        sys.exit(str(error))
