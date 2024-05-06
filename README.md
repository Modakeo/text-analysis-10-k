# text-analysis-10-k
1.1 It downloads 10-K files and only takes out the 10-K part(content within TEXT tag) by parse the txt file and clean all tags by beautifulsoup. It ignores the extra parts, e.g. EX-4.1, EX-10.16 and etc. This reduced ~50X the files size.

1.2 Split content into fixed size chucks, without breaking the sentence. Use openai embedding to create embeddings. Use Llama-index to save the vectors. 

1.3 When query, it needs to load the vectors from the disk(very slow, it needs an improvement). And pick top 20 candidates and send chatgpt-3.5.


## Visual
Please see the `key_number_tracking.ipynb`.

## Customize
By default, it downloads AAPL and MSFT. If you need more tickers, run `python download.py -ticker {your_ticker}`.