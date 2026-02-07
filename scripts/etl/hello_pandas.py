import pandas as pd


def main() -> None:
    df = pd.DataFrame(
        {
            "message": ["hello", "world"],
            "value": [1, 2],
        }
    )
    print("pandas version:", pd.__version__)
    print(df)


if __name__ == "__main__":
    main()
