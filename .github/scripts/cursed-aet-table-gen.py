import json
import pathlib
import sys
from py_markdown_table.markdown_table import markdown_table


GIT_RAW_URL = "https://raw.githubusercontent.com"
GIT_REPO_BRANCH = "results"
GIT_REPO = "Claudemirovsky/cursed-aet"
GIT_REPOSITORY_URL = f"{GIT_RAW_URL}/{GIT_REPO}/{GIT_REPO_BRANCH}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("where results dir????")
        exit(1)

    dir = pathlib.Path(sys.argv[1])
    if not dir.is_dir():
        print("That's not a directory.")
        exit(1)
    elif not dir.exists():
        print("This directory does not exist.")

    files = sorted(dir.glob("*.json"))

    all = 0
    passed = 0
    result_list: list[dict] = []
    table_list: list[dict] = []

    for file in files:
        all += 1
        name = file.name
        pkg = file.stem.removeprefix("results-")
        log_url = f"{GIT_REPOSITORY_URL}/{file.as_posix()}"
        with file.open() as f:
            data: list[dict] = json.load(f)
            count = len(data)
            passed_count = 0
            test_count = 0
            for item in data:
                for test in item["results"].values():
                    test_count += 1
                    if test["passed"]:
                        passed_count += 1

            status_text = "✅"
            if test_count == passed_count:
                passed += 1
            else:
                status_text = f"❌<br>{passed_count}/{test_count}"

            result_list.append(
                {"pkg": pkg, "passed": test_count == passed_count, "log": log_url}
            )
            table_list.append(
                {"Extension": pkg, "Status": status_text, "Log": f"[{name}]({log_url})"}
            )

    with open("results.json", "w+") as f:
        json.dump(result_list, f, indent=4)

    with open("README.md", "w+") as f:
        percent = (passed * 100) // all
        f.write("## Extension status\n\n")
        f.write(f"### {passed}/{all}({percent}%) are working.\n\n")
        f.write(
            markdown_table(table_list)
            .set_params(
                row_sep="markdown",
                quote=False,
            )
            .get_markdown()
        )
