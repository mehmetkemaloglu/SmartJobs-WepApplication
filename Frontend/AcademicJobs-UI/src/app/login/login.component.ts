import { Component, OnInit } from '@angular/core';
import { LoginService } from '../login.service';
import { Router } from '@angular/router';

import tooltipData from '../../assets/tooltipDescription.json';
import { EventEmitterService } from '../event-emitter.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  username;
  password;

  message;
  tooltip;

  constructor(
    private loginService: LoginService ,
    private router: Router,
    private eventEmitterService: EventEmitterService
  ) {
    this.username="";
    this.password="";
    this.tooltip=tooltipData.login;
   }

  ngOnInit() {
    this.message="";
    if(this.loginService.loggedIn()){
      this.message="You have already logged in."
    }
  }

  login(){

    //make the controlls
    this.loginService.loginUser(this.getLoginBody())
      .subscribe(
        (res)=>{
          if(this.loginService.loggedIn()){
            this.loginService.logOut();
          }
          localStorage.setItem('userID', res);
          this.eventEmitterService.onFirstComponentButtonClick(); 
          this.router.navigate(['/inbox']);
        },
        err =>{ 
          console.log(err);
          this.message="Wrong username or password";
          this.password="";
        }   
    )
  }

  getLoginBody(){
    var loginBody={
      "name":this.username,
      "password":this.password,
    }
    return loginBody;
  }
}
