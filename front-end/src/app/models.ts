export interface Document {
  title: string;
  author: string;
  file: string;
  id: number;
  corpus_index: number;
}

export interface Corpus {
  id: number;
  name: string;
}
