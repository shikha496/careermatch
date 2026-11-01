
def generate_star_answer(
    situation,
    task,
    action,
    result
):
    fields = {
        "Situation": situation,
        "Task": task,
        "Action": action,
        "Result": result
    }

    missing = [
        key for key, value in fields.items()
        if not value or not value.strip()
    ]

    if missing:
        raise ValueError(
            "Complete these sections: " + ", ".join(missing)
        )

    answer = (
        f"Situation: {situation.strip()}\n\n"
        f"Task: {task.strip()}\n\n"
        f"Action: {action.strip()}\n\n"
        f"Result: {result.strip()}"
    )

    return {
        "answer": answer,
        "sections": fields,
        "word_count": len(answer.split()),
        "quality_checks": {
            "situation_present": bool(situation.strip()),
            "task_present": bool(task.strip()),
            "action_present": bool(action.strip()),
            "result_present": bool(result.strip())
        }
    }
