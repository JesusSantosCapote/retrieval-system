import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { Document, Corpus } from '../models';
import { SearchService } from '../search.service';

@Component({
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss'],
})
export class MainComponent implements OnInit {
  constructor(private searchService: SearchService) {}

  ngOnInit(): void {}

  searchText: string = '';
  corpora$: Observable<Corpus[]> = this.searchService.getCorpora();
  corpus: string = 'cranfield';
  booleanResults!: Observable<Document[]>;
  vectorialResults!: Observable<Document[]>;
  lsiResults!: Observable<Document[]>;

  search() {
    this.booleanResults = this.searchService.search(
      this.searchText,
      'boolean',
      this.corpus
    );
    this.vectorialResults = this.searchService.search(
      this.searchText,
      'vectorial',
      this.corpus
    );
    this.lsiResults = this.searchService.search(
      this.searchText,
      'lsi',
      this.corpus
    );
  }
}
