import { Injectable } from '@angular/core';
import { HttpHeaders, HttpClient } from '@angular/common/http';

import url from '../assets/backendIP.json';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  

  readonly httpOptions = {
    headers: new HttpHeaders({
      'Content-Type':  'application/json',
      'Access-Control-Allow-Origin': '*',
    },

    )
  };
  baseURL=url.url_;
  
  constructor(
    private http: HttpClient
  ) { }

  loginUser(body){
    return this.http.post<any>(this.baseURL+"api/signin/",body,this.httpOptions);
  }
  loggedIn(){
    return !!localStorage.getItem('userID');
  }
  logOut(){
    localStorage.removeItem('userID');
  }
  signUp(body){
    return this.http.post<any>(this.baseURL+"api/signup/",body,this.httpOptions);
  }
  
}
