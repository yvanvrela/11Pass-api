from src.application import create_app

app = create_app()


def main() -> None:
    """Run FastApi
    """
    app


if __name__ == '__main__':
    main()
