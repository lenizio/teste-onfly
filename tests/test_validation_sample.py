"""Regressão da amostra de validação documentada no README."""

import json
import os
import subprocess
import sys

from helpers import PROJECT_ROOT, SRC_DIR


def test_cli_matches_readme_validation_sample(tmp_path):
    """Confere o relatório da amostra real, incluindo a ordem dos meses e hotéis."""
    output_path = tmp_path / "exemplo.json"
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(SRC_DIR) + os.pathsep + environment.get("PYTHONPATH", "")
    environment["PYTHONDONTWRITEBYTECODE"] = "1"

    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "onfly_report",
            "--input",
            str(PROJECT_ROOT / "data" / "exemplo-validacao.csv"),
            "--rates",
            str(PROJECT_ROOT / "data" / "taxas_cambio.csv"),
            "--output",
            str(output_path),
        ],
        cwd=str(PROJECT_ROOT),
        env=environment,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert process.returncode == 0, process.stderr
    report = json.loads(output_path.read_text(encoding="utf-8"))
    report.pop("generated_at", None)

    assert report == {
        "report_version": "1.0",
        "summary": {
            "total_reservations": 12,
            "confirmed_reservations": 9,
            "cancelled_reservations": 2,
            "no_show_reservations": 1,
            "total_room_nights": 28,
            "total_amount_brl": "7566.00",
            "average_nightly_rate_brl": "270.21",
        },
        "by_month": [
            {"month": "2025-01", "reservations": 8, "room_nights": 25, "total_brl": "6684.00"},
            {"month": "2025-02", "reservations": 1, "room_nights": 3, "total_brl": "882.00"},
        ],
        "top_hotels": [
            {"hotel_id": "H01", "hotel_name": "Hotel Aurora Paulista", "room_nights": 3, "total_brl": "1200.00"},
            {"hotel_id": "H02", "hotel_name": "Hotel Mirante", "room_nights": 2, "total_brl": "1084.00"},
            {"hotel_id": "H12", "hotel_name": "Hotel Miami Beach", "room_nights": 1, "total_brl": "1000.00"},
            {"hotel_id": "H10", "hotel_name": "Hotel Madrid, Gran Vía", "room_nights": 4, "total_brl": "900.00"},
            {"hotel_id": "H09", "hotel_name": "Hotel Lisboa, Centro", "room_nights": 3, "total_brl": "882.00"},
        ],
    }
