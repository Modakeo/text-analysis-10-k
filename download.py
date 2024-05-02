import argparse
import os
import shutil

from sec_edgar_downloader import Downloader


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Download SEC filings."
    )

    # # Required arguments
    # parser.add_argument(
    #     "-form", # Use only one dash as required in the PDF.
    #     type=str,
    #     default='10-K',
    #     help="Form type to download. e.g. 10-K.",
    # )

    parser.add_argument(
        "-ticker",
        type=str,
        help="One ticker",
    )

    parser.add_argument(
        "-after",
        type=str,
        default='1995',
        help="after date",
    )
    
    return parser.parse_args()


if __name__ == '__main__':
    edgar_fold = 'sec-edgar-filings'
    args = parse_args()
    form_type = '10-K'
    after_year = args.after
    if args.ticker:
        tickers = [args.ticker]
    else:
        tickers = ['AAPL', 'MSFT'] # ,'JPM','ADSK','IBM'
    print(tickers, after_year)

    dl = Downloader("RandomName", "RandomEmail@domain.com",'./')

    for ticker in tickers:
        for year in range(int(after_year),2024):
            print(f'Downloading {form_type} for {ticker} in {year}...')
            dl.get(form_type, ticker, after=f'{year}-01-01', before=f'{year}-12-31', download_details='8-K HTML')

            temp_f = os.path.join(edgar_fold, ticker, form_type,)
            # check if only one folder is present
            folders = [name for name in os.listdir(temp_f) if os.path.isdir(os.path.join(temp_f, name))]
            if len(folders) > 1:
                raise Exception(f'Error: {len(folders)} folders found for {ticker} in {year}')
            elif len(folders) == 0:
                print(f'No {form_type} found for {ticker} in {year}...continuing...')
                continue
            folder = folders[0]
            
            # move the file to the root folder
            target = os.path.join(temp_f, folder, 'full-submission.txt')
            destination = os.path.join(temp_f, f'{ticker}-{form_type}-{year}.txt')
            shutil.move(target, destination)
            # delete the folder
            shutil.rmtree(os.path.join(temp_f, folder))


    for ticker in tickers:
        names = [i for i in os.listdir(os.path.join(edgar_fold, ticker, form_type))]
        names.sort(key=lambda x: int(x.split('-')[1]))
        print(ticker, len(names))