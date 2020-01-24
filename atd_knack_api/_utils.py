import knackpy

def knackpy_wrapper(cfg, app_id):
    """
    Fetch records which need to be processed from a pre-filtered
    Knack view which does not require authentication.
    """
    return knackpy.Knack(
        scene=cfg["scene"],
        view=cfg["view"],
        app_id=app_id,
        page_limit=100,
        rows_per_page=1000,
    )