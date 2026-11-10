
import argparse
import time
from collections.abc import Callable

from sqlmodel import Session, select

from app.database import engine, create_db_and_tables
from app.history import save_health_result
from app.models import ServiceDB
from app.monitoring import check_url, HealthResult


LOCAL_HEALTH_URL = "http://127.0.0.1:8000/health"


def run_checks(
    session: Session,
    checker: Callable[[str], HealthResult] = check_url,
) -> int:
    # Only monitor our explicitly approved local endpoint.
    services = session.exec(
        select(ServiceDB).where(
            ServiceDB.health_url == LOCAL_HEALTH_URL
        )
    ).all()

    for service in services:
        result = checker(LOCAL_HEALTH_URL)

        record = save_health_result(
            session,
            service.id,
            result,
        )

        print(
            f"{service.name}: {record.status} "
            f"(HTTP {record.http_status}, "
            f"{record.response_time_ms} ms)"
        )

    return len(services)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--interval", type=int, default=15)

    args = parser.parse_args()

    if args.interval < 5:
        parser.error("Interval must be at least 5 seconds")

    create_db_and_tables()

    try:
        while True:
            with Session(engine) as session:
                count = run_checks(session)

            if count == 0:
                print("No approved local services registered.")

            if args.once:
                break

            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\nMonitoring worker stopped.")


if __name__ == "__main__":
    main()
