import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Document, Corpus } from './models';

@Injectable({
  providedIn: 'root',
})
export class SearchService {
  BASE_URL = 'http://127.0.0.1:8000/api/';

  constructor(private http: HttpClient) {}

  search(query: string, model: string, corpus: string) {
    let queryParams = new HttpParams();
    queryParams = queryParams.set('type', model);
    queryParams = queryParams.set('corpus', corpus);
    if (model === 'boolean') {
      query = this.processBooleanQuery(query);
    }
    queryParams = queryParams.set('query', query);

    return this.http.get<Document[]>(this.BASE_URL + 'search/', {
      params: queryParams,
    });
  }

  getCorpora() {
    return this.http.get<Corpus[]>(this.BASE_URL + 'corpus/');
  }

  processBooleanQuery(query: string) {
    const terms = query.split(' ');
    let processedQuery = '';
    for (let i = 0; i < terms.length; i++) {
      if (i !== 0) {
        processedQuery += ' and ';
      }
      processedQuery += terms[i];
    }
    return processedQuery;
  }
}
