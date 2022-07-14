import re
from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from mrjob.step import MRStep
import pandas as pd
WORD_RE = re.compile(r"[\w']+")
word1=list()
count1 =list()
class MapReduceReviews(MRJob):
    FILES = ['stop_words.txt']
    OUTPUT_PROTOCOL = JSONValueProtocol
    def configure_args(self):
        super(MapReduceReviews, self).configure_args()
        self.add_file_arg(
            '--stop-words-file',
            dest='stop_words_file',
            default=None,
            help='alternate stop words file. lowercase words, one per line',
        )

    def mapper_init(self):
        stop_words_path = self.options.stop_words_file or 'stop_words.txt'
        with open(stop_words_path) as f:
            self.stop_words = set(line.strip() for line in f)

    def mapper_get_words(self, _, line):
        for word in WORD_RE.findall(line):
            word = word.lower()
            if word not in self.stop_words:
                yield (word, 1)

    def combiner_count_words(self, word, counts):
        yield (word, sum(counts))
        

    def reducer_count_words(self, word, counts):
        word1.append( word)
        count1.append(sum(counts))
        yield None, (sum(counts), word)

    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_init,
                   mapper=self.mapper_get_words,
                   combiner=self.combiner_count_words,
                   reducer=self.reducer_count_words)
            ]
            #this is a comment

if __name__ == '__main__':
    MapReduceReviews.run()
    zipped = list(zip(word1,count1,))
    df = pd.DataFrame(zipped, columns=['Word', 'Count'])
    df.to_csv ('export_df.csv', index = None, header=True)