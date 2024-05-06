import download
import preprocess
import embedding

def main():
    download.download_all(tickers=['AAPL', 'MSFT'], after_year='1995')
    preprocess.batch_preprocess()
    embedding.vdb()

if __name__ == '__main__':
    main()