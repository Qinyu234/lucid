from .is_fully_grown import is_fully_grown


def assess_job(root) -> tuple:

    def collect_issues(node, path: str = "root") -> list:
        issues = []
        status = node.get("status")
        children = node.get("children", [])
        fn = node.get("function_name") or path
        here = f"{path}/{fn}" if path != "root" else fn

        if status == "growing":
            issues.append(f"{here}: still growing")

        if status == "failed":
            issues.append(f"{here}: expand failed ({node.get('converge_reason')})")

        if status == "done" and not children:
            reason = node.get("converge_reason", "")
            if reason == "expand_failed":
                issues.append(f"{here}: leaf stopped due to expand failure")
            if node.get("code_ok") is False:
                issues.append(f"{here}: code generation failed")
            if node.get("test_ok") is False:
                issues.append(f"{here}: test generation failed")

        for child in children:
            issues.extend(collect_issues(child, here))

        return issues

    issues = collect_issues(root)

    if issues:
        return "incomplete", issues

    if not is_fully_grown(root):
        return "incomplete", ["tree growth did not converge"]

    return "done", []
