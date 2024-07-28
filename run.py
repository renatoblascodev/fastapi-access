from uvicorn import run

if __name__ == "__main__":
    run(
        "app.main:app",
        host="0.0.0.0",
        port=8011,
        workers=1,
        use_colors=True,
        log_config="app/log_conf.yaml",
    )
