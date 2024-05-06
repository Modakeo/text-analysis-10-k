import argparse
import os

from bs4 import BeautifulSoup


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Preprocess SEC filings."
    )

    parser.add_argument(
        "-input_dir",
        type=str,
        default='sec-edgar-filings',
        help="input directory",
    )

    parser.add_argument(
        "-output_dir",
        type=str,
        default='preprocessed',
        help="output directory",
    )
    
    return parser.parse_args()


def preprocess(file_path):
    # download
    # dl = Downloader("RandomName", "
    with open(file_path, 'r') as f:
        valid_section = ''
        hit_10_k = False
        hit_text = False
        i = 0
        total_char = 0
        for line in f.readlines():
            total_char += len(line)
            if line.strip() == '<TYPE>10-K':
                hit_10_k = True
            if line[:6] == '<TEXT>' and hit_10_k:
                hit_text = True
            if line[:7] == '</TEXT>' and hit_text:
                hit_10_k = False
                hit_text = False
            # if it is in 10-K and text section
            if hit_10_k and hit_text:
                valid_section += line
            i+=1
    
    soup = BeautifulSoup(valid_section, 'html.parser')
    text = soup.get_text('<div>').replace('<div>','\n')
    print(f'compression ratio: {len(text)/total_char * 100:.2f}%')

    return text


def batch_preprocess(input_dir='sec-edgar-filings', output_dir='preprocessed'):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.txt'):
                print(f'Preprocessing {file}...')
                file_path = os.path.join(root, file)
                text = preprocess(file_path)
                output_file = os.path.join(output_dir, file)
                if not os.path.exists(os.path.dirname(output_file)):
                    os.makedirs(os.path.dirname(output_file))
                with open(output_file, 'w') as f:
                    f.write(text)


if __name__ == '__main__':
    args = parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir

    batch_preprocess(input_dir, output_dir)