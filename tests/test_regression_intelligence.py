from ci.check_regression_intelligence import run_check


def test_regression_detected(tmp_path):
    # prepare directories
    (tmp_path / "ci").mkdir()
    (tmp_path / "logs").mkdir()

    diff = tmp_path / "build_metrics_diff.md"
    diff.write_text(
        "Execution Time: 100 -> 130\n"
        "Success Rate: 0.9 -> 0.7\n"
        "Retries: 1 -> 3\n"
    )

    log = tmp_path / "logs" / "bot_engine.log"
    log.write_text("normal run")

    classification = run_check(tmp_path)
    assert classification == "Regressao Critica"
    report = tmp_path / "ci" / "regression_intelligence_report.md"
    assert report.exists()
