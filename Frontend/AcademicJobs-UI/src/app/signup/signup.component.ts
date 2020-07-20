import { Component, OnInit } from '@angular/core';
import { LoginService } from '../login.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
export class SignupComponent implements OnInit {

  username;
  password;
  password2;

  message;

  constructor(
    private loginService: LoginService ,
    private router: Router
  ) {
    this.username="";
    this.password="";
   }

  ngOnInit() {
    this.message="";
  }

  signUp(){
    //make the controlls
    if(this.password2!==this.password){
      this.message="Those passwords didn't match. Try again."
      return;
    }
    this.loginService.signUp(this.getSignUpBody())
      .subscribe(
        (res)=>{
          console.log(res)
          window.alert("You have successfully signed up.");
          this.router.navigate(['/login']);
        },
        err =>{
          console.log(err);
          this.message="Try again with another username."
          this.username="";
          this.password="";
        }    
    )
  }

  getSignUpBody(){
    var signUpBody={
      "name":this.username,
      "password":this.password,
    }
    return signUpBody;
  }

}
