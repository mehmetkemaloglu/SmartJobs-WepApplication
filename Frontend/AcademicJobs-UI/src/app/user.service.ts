import { Injectable, EventEmitter } from '@angular/core';
import { Observable, BehaviorSubject } from '../../node_modules/rxjs';
import { of} from 'rxjs';
import { map } from 'rxjs/operators';
import { HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import { LoginService } from './login.service';

import url from '../assets/backendIP.json';



@Injectable({
  providedIn: 'root'
})
export class UserService {
  private searchResults: any[] = [];
  public isSearchResultsReady = new BehaviorSubject<boolean>(false);

  private quickSearchResults: any[] = [];
  public isQuickSearchResultsReady = new BehaviorSubject<boolean>(false);
 
  baseURL=url.url_;

  currentJob;
  currentSearchedJobList;

  readonly httpOptions = {
    headers: new HttpHeaders({
      'Content-Type':  'application/json',
      'Access-Control-Allow-Origin': '*',
    },

    )
  };
  
  constructor( private http: HttpClient, private loginService: LoginService) { }

  private extractData(res: Response){
    let body = res;
    return body || {};

  }

  getUserID(){
    return localStorage.getItem('userID');
  }

  getSearchedQueries(){
    return this.http.get<any>(this.baseURL+"api/query?personid="+this.getUserID());
    //return this.http.get<any>(this.baseURL+"api/query?personid=2");
  }
  getLikedJobs(){
    return this.http.get<any>(this.baseURL+"api/like?personid="+this.getUserID());
    //return this.http.get<any>(this.baseURL+"api/like?personid=2");
  }

  getSavedJobs(){
     return this.http.get<any>(this.baseURL+"api/jobs?personid="+this.getUserID());
     //return this.http.get<any>(this.baseURL+"api/jobs?personid=2");
  }
  getLabels(){
    return this.http.get<any>(this.baseURL+"api/labels?personid="+this.getUserID());
    //return this.http.get<any>(this.baseURL+"api/labels?personid=2");
  }
  getLabelsOfAJob(jid_){
    return this.http.get<any>(this.baseURL+"api/labels?personid="+this.getUserID()+"&jid="+jid_);
    //return this.http.get<any>(this.baseURL+"api/labels?personid=2&jid="+jid_);
  }

  getJobById(jid_){
    if (this.loginService.loggedIn()){
      return this.http.get<any>(this.baseURL+"api/jobs/?personid="+this.getUserID()+"&jid="+jid_); 
      //return this.http.get<any>(this.baseURL+"api/jobs/?personid=2&jid="+jid_);
    }
    return this.http.get<any>(this.baseURL+"api/jobs/?jid="+jid_);
  }

  getInbox(){
    return this.http.get<any>(this.baseURL+"api/inbox/?personid="+this.getUserID());
    //return this.http.get<any>(this.baseURL+"api/inbox/?personid=2");
  }

  getQuickSearch(){
    return this.http.get<any>(this.baseURL+"api/shquery/");
  }

  getQuickSearchResults(){
    return this.quickSearchResults;
  }

  async getQuickSearchData(id_){
    let url = this.baseURL+"api/shresult/?queryid="+id_;
    return this.http.get(url).pipe(map(this.extractData)).subscribe((result:any) =>{
      this.quickSearchResults = result;
      this.isQuickSearchResultsReady.next(true);
    }, (error) => {
      console.log(error);
    });
  }

  
  getSearchResults(){
    return this.searchResults;
  }

  async getSearchData(path){
    let url = this.baseURL+path;
    console.log(url)
    return this.http.get(url).pipe(map(this.extractData)).subscribe((result:any) =>{
      console.log(result)
      this.searchResults = result;
      this.isSearchResultsReady.next(true);
    }, (error) => {
      console.log(error);
    });
  }

  
  saveQuery(body){
    return this.http.post<any>(this.baseURL+"api/query/",body,this.httpOptions);
  }

  addLabel(job,label_){
    var addLabelBody={
      "labelname":label_,
      "personid":this.getUserID(),
      "job":job
    }
    console.log(addLabelBody);
    return this.http.post<any>(this.baseURL+"api/labels/",addLabelBody,this.httpOptions);
  }

  likeJob(job){
    var likeBody={
      "personid":this.getUserID(),
      "job":job
    }
    return this.http.post<any>(this.baseURL+"api/like/",likeBody,this.httpOptions);
  }

  removeQuery(id_){
    const options = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      }),
      body: {
        id: id_,
        personid: this.getUserID() 
      },
    };  
    return this.http.delete<any>(this.baseURL+"api/query/",options)
  }
  removeLike(jid_){
    console.log(jid_);
    
    const options2 = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      }),
      body: {
        personid:this.getUserID(),
        jid:jid_
      },
    };
    
    return this.http.delete<any>(this.baseURL+"api/like/",options2)
  }

  deleteLabelFromAll(label_){
    const options3 = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      }),
      body: {
        personid:this.getUserID(),
        label:label_
      },
    };
    return this.http.delete<any>(this.baseURL+"api/labels/",options3)
  }

  deleteLabelFromJob(label_,jid_){    
    const options4 = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      }),
      body: {
        "personid":this.getUserID(),
        jid:jid_,
        label:label_,
      },
    };
    return this.http.delete<any>(this.baseURL+"api/labels/",options4)
  }

}
