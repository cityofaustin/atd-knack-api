import knackpy

def knackpy_wrapper(cfg, auth, filters=None):
    """
    Fetch records which need to be processed from a pre-filtered
    Knack view which does not require authentication.
    """
    return knackpy.Knack(
        scene=cfg.get("scene"),
        view=cfg.get("view"),
        obj=cfg.get("obj"),
        app_id=auth["app_id"],
        api_key=auth["api_key"],
        page_limit=100,
        rows_per_page=1000,
        filters=filters,
    )


def knack_filter(field, value):
    return [{"field": f"{field}", "operator": "is", "value": f"{value}"}]